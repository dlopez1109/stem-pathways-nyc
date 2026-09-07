"""Secure Supabase session persistence for STEM Pathways NYC.

Design:
- Browser cookie `sp_sid` holds only an opaque random session ID
  (Secure + HttpOnly + SameSite=Lax).
- Access/refresh tokens live encrypted in Supabase `auth_sessions`
  (service_role only). They are never written to cookies, query params,
  localStorage, or visible HTML.
- Cookie writes happen only via ASGI `/auth/*` routes in asgi_app.py
  after consuming a short-lived server-side `auth_cookie_tickets` row.
- In-memory ticket maps are intentionally NOT used (multi-worker unsafe).

Requires: `streamlit run asgi_app.py` on Render (not bare `streamlit run app.py`).
"""

from __future__ import annotations

import base64
import hashlib
import os
import re
import secrets
import time
from datetime import datetime, timezone
from typing import Any, Callable
from urllib.parse import quote

COOKIE_NAME = "sp_sid"
SESSIONS_TABLE = "auth_sessions"
COOKIE_TICKETS_TABLE = "auth_cookie_tickets"
PERSIST_MAX_AGE_SECONDS = 30 * 24 * 60 * 60  # absolute lifetime
IDLE_MAX_AGE_SECONDS = 7 * 24 * 60 * 60  # idle timeout
COOKIE_TICKET_TTL_SECONDS = 120
PROD_HOST_MARKER = "stempathwaysnyc.com"
_SESSION_ID_RE = re.compile(r"^[A-Za-z0-9_-]{20,128}$")

ServiceClientFactory = Callable[[], Any]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def _parse_iso(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except Exception:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _get_secret() -> str:
    env = (
        os.environ.get("SP_AUTH_PERSIST_SECRET")
        or os.environ.get("AUTH_PERSIST_SECRET")
        or ""
    ).strip()
    if env:
        return env
    try:
        import streamlit as st

        auth = st.secrets.get("auth", {})
        for key in ("persist_secret", "cookie_secret"):
            value = str(auth.get(key, "") or "").strip()
            if value:
                return value
    except Exception:
        pass
    return ""


def persist_secret_configured() -> bool:
    return bool(_get_secret())


def _fernet():
    secret = _get_secret()
    if not secret:
        raise RuntimeError("Auth persist secret is not configured.")
    from cryptography.fernet import Fernet

    digest = hashlib.sha256(secret.encode("utf-8")).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


def encrypt_token(token: str) -> str:
    return _fernet().encrypt(str(token).encode("utf-8")).decode("utf-8")


def decrypt_token(token_enc: str) -> str | None:
    if not token_enc or not persist_secret_configured():
        return None
    try:
        from cryptography.fernet import InvalidToken

        return _fernet().decrypt(str(token_enc).encode("utf-8")).decode("utf-8")
    except Exception:
        return None


def new_session_id() -> str:
    return secrets.token_urlsafe(32)


def session_id_is_valid(session_id: str | None) -> bool:
    return bool(_SESSION_ID_RE.fullmatch(str(session_id or "").strip()))


def cookie_secure_for_host(host: str | None) -> bool:
    host = (host or "").split(":")[0].strip().lower()
    if not host or host in {"localhost", "127.0.0.1", "::1"}:
        return False
    return True


def cookie_domain_for_host(host: str | None) -> str | None:
    host = (host or "").split(":")[0].strip().lower()
    if host == PROD_HOST_MARKER or host.endswith("." + PROD_HOST_MARKER):
        return PROD_HOST_MARKER
    return None


def _service_client_from_env():
    url = (
        os.environ.get("SUPABASE_URL")
        or os.environ.get("SP_SUPABASE_URL")
        or ""
    ).strip()
    key = (
        os.environ.get("SUPABASE_SERVICE_KEY")
        or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        or os.environ.get("SP_SUPABASE_SERVICE_KEY")
        or ""
    ).strip()
    if not url or not key:
        try:
            import streamlit as st

            url = url or str(st.secrets["supabase"].get("url", "") or "").strip()
            key = key or str(
                st.secrets["supabase"].get("service_key", "") or ""
            ).strip()
        except Exception:
            pass
    if not url or not key:
        return None
    from supabase import create_client

    return create_client(url, key)


_client_factory: ServiceClientFactory | None = None


def set_service_client_factory(factory: ServiceClientFactory | None) -> None:
    global _client_factory
    _client_factory = factory


def get_service_client():
    if _client_factory is not None:
        try:
            return _client_factory()
        except Exception:
            return None
    return _service_client_from_env()


def create_server_session(
    *,
    access_token: str,
    refresh_token: str,
    user_id: str,
    email: str = "",
    provider: str = "email",
    rotated_from: str | None = None,
    client=None,
) -> str | None:
    """Insert a new auth_sessions row. Returns opaque session_id or None."""

    access_token = str(access_token or "").strip()
    refresh_token = str(refresh_token or "").strip()
    user_id = str(user_id or "").strip()
    provider = str(provider or "email").strip().lower() or "email"
    if provider not in {"email", "google"}:
        provider = "email"
    if not access_token or not refresh_token or not user_id:
        return None
    if not persist_secret_configured():
        return None

    client = client or get_service_client()
    if client is None:
        return None

    session_id = new_session_id()
    if not session_id_is_valid(session_id):
        return None

    now = _utc_now()
    try:
        access_enc = encrypt_token(access_token)
        refresh_enc = encrypt_token(refresh_token)
        (
            client.table(SESSIONS_TABLE)
            .insert(
                {
                    "session_id": session_id,
                    "user_id": user_id,
                    "provider": provider,
                    "access_token_enc": access_enc,
                    "refresh_token_enc": refresh_enc,
                    "email": str(email or "") or None,
                    "created_at": _iso(now),
                    "expires_at": _iso(
                        datetime.fromtimestamp(
                            now.timestamp() + PERSIST_MAX_AGE_SECONDS,
                            tz=timezone.utc,
                        )
                    ),
                    "last_seen_at": _iso(now),
                    "idle_expires_at": _iso(
                        datetime.fromtimestamp(
                            now.timestamp() + IDLE_MAX_AGE_SECONDS,
                            tz=timezone.utc,
                        )
                    ),
                    "revoked_at": None,
                    "rotated_from": (
                        str(rotated_from)
                        if session_id_is_valid(rotated_from)
                        else None
                    ),
                }
            )
            .execute()
        )
        return session_id
    except Exception:
        return None


def _row_is_active(row: dict[str, Any], *, now: datetime | None = None) -> bool:
    if not isinstance(row, dict):
        return False
    if row.get("revoked_at"):
        return False
    now = now or _utc_now()
    expires_at = _parse_iso(row.get("expires_at"))
    idle_expires_at = _parse_iso(row.get("idle_expires_at"))
    if expires_at is None or idle_expires_at is None:
        return False
    if expires_at <= now or idle_expires_at <= now:
        return False
    return True


def load_server_session(session_id: str, *, client=None) -> dict[str, Any] | None:
    session_id = str(session_id or "").strip()
    if not session_id_is_valid(session_id):
        return None
    client = client or get_service_client()
    if client is None:
        return None
    try:
        response = (
            client.table(SESSIONS_TABLE)
            .select(
                "session_id,user_id,provider,access_token_enc,refresh_token_enc,"
                "email,created_at,expires_at,last_seen_at,idle_expires_at,"
                "revoked_at,rotated_from"
            )
            .eq("session_id", session_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        if not rows or not isinstance(rows[0], dict):
            return None
        row = rows[0]
        if not _row_is_active(row):
            return None
        access = decrypt_token(row.get("access_token_enc"))
        refresh = decrypt_token(row.get("refresh_token_enc"))
        if not access or not refresh:
            return None
        return {
            "session_id": str(row.get("session_id") or ""),
            "user_id": str(row.get("user_id") or ""),
            "provider": str(row.get("provider") or "email"),
            "access_token": access,
            "refresh_token": refresh,
            "email": str(row.get("email") or ""),
            "expires_at": row.get("expires_at"),
            "idle_expires_at": row.get("idle_expires_at"),
            "created_at": row.get("created_at"),
        }
    except Exception:
        return None


def touch_server_session(session_id: str, *, client=None) -> bool:
    session_id = str(session_id or "").strip()
    if not session_id_is_valid(session_id):
        return False
    client = client or get_service_client()
    if client is None:
        return False
    now = _utc_now()
    try:
        (
            client.table(SESSIONS_TABLE)
            .update(
                {
                    "last_seen_at": _iso(now),
                    "idle_expires_at": _iso(
                        datetime.fromtimestamp(
                            now.timestamp() + IDLE_MAX_AGE_SECONDS,
                            tz=timezone.utc,
                        )
                    ),
                }
            )
            .eq("session_id", session_id)
            .is_("revoked_at", "null")
            .execute()
        )
        return True
    except Exception:
        return False


def update_server_session_tokens(
    session_id: str,
    *,
    access_token: str,
    refresh_token: str,
    client=None,
) -> bool:
    """Update tokens in-place (prefer rotate_server_session after refresh)."""

    session_id = str(session_id or "").strip()
    access_token = str(access_token or "").strip()
    refresh_token = str(refresh_token or "").strip()
    if not session_id_is_valid(session_id) or not access_token or not refresh_token:
        return False
    if not persist_secret_configured():
        return False
    client = client or get_service_client()
    if client is None:
        return False
    now = _utc_now()
    try:
        (
            client.table(SESSIONS_TABLE)
            .update(
                {
                    "access_token_enc": encrypt_token(access_token),
                    "refresh_token_enc": encrypt_token(refresh_token),
                    "last_seen_at": _iso(now),
                    "idle_expires_at": _iso(
                        datetime.fromtimestamp(
                            now.timestamp() + IDLE_MAX_AGE_SECONDS,
                            tz=timezone.utc,
                        )
                    ),
                }
            )
            .eq("session_id", session_id)
            .is_("revoked_at", "null")
            .execute()
        )
        return True
    except Exception:
        return False


def revoke_server_session(session_id: str, *, client=None) -> bool:
    session_id = str(session_id or "").strip()
    if not session_id_is_valid(session_id):
        return False
    client = client or get_service_client()
    if client is None:
        return False
    try:
        (
            client.table(SESSIONS_TABLE)
            .update({"revoked_at": _iso(_utc_now())})
            .eq("session_id", session_id)
            .is_("revoked_at", "null")
            .execute()
        )
        return True
    except Exception:
        return False


def rotate_server_session(
    old_session_id: str,
    *,
    access_token: str,
    refresh_token: str,
    user_id: str,
    email: str = "",
    provider: str = "email",
    client=None,
) -> str | None:
    """Revoke old session and create a new session_id (login/refresh rotation)."""

    client = client or get_service_client()
    new_id = create_server_session(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user_id,
        email=email,
        provider=provider,
        rotated_from=old_session_id,
        client=client,
    )
    if not new_id:
        return None
    if session_id_is_valid(old_session_id):
        revoke_server_session(old_session_id, client=client)
    return new_id


def create_cookie_ticket(
    session_id: str,
    *,
    purpose: str = "set",
    client=None,
) -> str | None:
    session_id = str(session_id or "").strip()
    purpose = str(purpose or "set").strip().lower() or "set"
    if purpose not in {"set", "clear"}:
        purpose = "set"
    if purpose == "set" and not session_id_is_valid(session_id):
        return None
    client = client or get_service_client()
    if client is None:
        return None
    ticket_id = secrets.token_urlsafe(24)
    if not session_id_is_valid(ticket_id):
        ticket_id = secrets.token_urlsafe(32)
    now = _utc_now()
    try:
        (
            client.table(COOKIE_TICKETS_TABLE)
            .insert(
                {
                    "ticket_id": ticket_id,
                    "session_id": session_id if purpose == "set" else "",
                    "purpose": purpose,
                    "created_at": _iso(now),
                    "expires_at": _iso(
                        datetime.fromtimestamp(
                            now.timestamp() + COOKIE_TICKET_TTL_SECONDS,
                            tz=timezone.utc,
                        )
                    ),
                    "consumed_at": None,
                }
            )
            .execute()
        )
        return ticket_id
    except Exception:
        return None


def consume_cookie_ticket(ticket_id: str, *, client=None) -> dict[str, Any] | None:
    """Atomically consume a one-time cookie ticket. Returns {purpose, session_id}."""

    ticket_id = str(ticket_id or "").strip()
    if not session_id_is_valid(ticket_id):
        return None
    client = client or get_service_client()
    if client is None:
        return None
    now = _utc_now()
    try:
        response = (
            client.table(COOKIE_TICKETS_TABLE)
            .select("ticket_id,session_id,purpose,expires_at,consumed_at")
            .eq("ticket_id", ticket_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        if not rows or not isinstance(rows[0], dict):
            return None
        row = rows[0]
        if row.get("consumed_at"):
            return None
        expires_at = _parse_iso(row.get("expires_at"))
        if expires_at is None or expires_at <= now:
            return None
        purpose = str(row.get("purpose") or "").strip().lower()
        session_id = str(row.get("session_id") or "").strip()
        if purpose == "set" and not session_id_is_valid(session_id):
            return None
        if purpose not in {"set", "clear"}:
            return None
        (
            client.table(COOKIE_TICKETS_TABLE)
            .update({"consumed_at": _iso(now)})
            .eq("ticket_id", ticket_id)
            .is_("consumed_at", "null")
            .execute()
        )
        return {"purpose": purpose, "session_id": session_id}
    except Exception:
        return None


def apply_set_session_cookie(response, session_id: str, *, host: str | None) -> None:
    session_id = str(session_id or "").strip()
    if not session_id_is_valid(session_id):
        raise ValueError("invalid session id")
    secure = cookie_secure_for_host(host)
    domain = cookie_domain_for_host(host)
    kwargs = {
        "key": COOKIE_NAME,
        "value": session_id,
        "path": "/",
        "secure": secure,
        "httponly": True,
        "samesite": "lax",
        "max_age": PERSIST_MAX_AGE_SECONDS,
    }
    if domain:
        kwargs["domain"] = domain
    response.set_cookie(**kwargs)


def apply_clear_session_cookie(response, *, host: str | None) -> None:
    domain = cookie_domain_for_host(host)
    kwargs = {"path": "/"}
    if domain:
        kwargs["domain"] = domain
    response.delete_cookie(COOKIE_NAME, **kwargs)
    for name in (
        "sp_supabase_session",
        "sp_supabase_session_0",
        "sp_supabase_session_1",
        "sp_supabase_session_2",
        "sp_supabase_session_3",
    ):
        response.delete_cookie(name, **kwargs)


def read_session_id_from_cookies(cookies: Any) -> str | None:
    if cookies is None:
        return None
    try:
        value = cookies.get(COOKIE_NAME)
    except Exception:
        value = None
    value = str(value or "").strip()
    if session_id_is_valid(value):
        return value
    return None


def browser_redirect_html(path: str) -> str:
    """Full-page navigation; path must be a relative /auth/* route only."""

    safe = quote(path, safe="/?=&")
    return (
        "<!DOCTYPE html><html><head>"
        f'<meta http-equiv="refresh" content="0;url={safe}">'
        f"<script>window.location.replace({path!r});</script>"
        "</head><body></body></html>"
    )


def access_token_expired(access_token: str, *, skew_seconds: int = 60) -> bool:
    """Best-effort JWT exp check without verification (expiry gate only)."""

    token = str(access_token or "").strip()
    parts = token.split(".")
    if len(parts) != 3:
        return True
    try:
        pad = "=" * (-len(parts[1]) % 4)
        raw = base64.urlsafe_b64decode(parts[1] + pad)
        import json

        payload = json.loads(raw.decode("utf-8"))
        exp = int(payload.get("exp") or 0)
    except Exception:
        return True
    return exp <= int(time.time()) + max(0, int(skew_seconds))
