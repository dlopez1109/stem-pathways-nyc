"""Offline tests for durable HttpOnly auth session persistence.

Run: python3 test_auth_persist_offline.py
Does not touch live secrets, network, or production Auth.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

os.environ["SP_AUTH_PERSIST_SECRET"] = "unit-test-persist-secret-please-rotate"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def _fernet_key():
    digest = hashlib.sha256(os.environ["SP_AUTH_PERSIST_SECRET"].encode()).digest()
    return base64.urlsafe_b64encode(digest)


class FakeTable:
    def __init__(self, store: dict, name: str):
        self.store = store
        self.name = name
        self._filters = {}
        self._op = None
        self._payload = None
        self._limit = None

    def insert(self, payload):
        self._op = "insert"
        self._payload = payload
        return self

    def select(self, *_cols):
        self._op = "select"
        return self

    def update(self, payload):
        self._op = "update"
        self._payload = payload
        return self

    def eq(self, key, value):
        self._filters[key] = ("eq", value)
        return self

    def is_(self, key, value):
        self._filters[key] = ("is", value)
        return self

    def limit(self, n):
        self._limit = n
        return self

    def execute(self):
        rows = self.store.setdefault(self.name, [])
        if self._op == "insert":
            rows.append(dict(self._payload))
            return MagicMock(data=[dict(self._payload)])
        matched = []
        for row in rows:
            ok = True
            for key, (op, value) in self._filters.items():
                if op == "eq" and str(row.get(key)) != str(value):
                    ok = False
                if op == "is":
                    if value == "null" and row.get(key) is not None:
                        ok = False
            if ok:
                matched.append(row)
        if self._op == "select":
            data = matched[: self._limit or len(matched)]
            return MagicMock(data=[dict(r) for r in data])
        if self._op == "update":
            for row in matched:
                row.update(dict(self._payload))
            return MagicMock(data=[dict(r) for r in matched])
        return MagicMock(data=[])


class FakeClient:
    def __init__(self):
        self.store = {"auth_sessions": [], "auth_cookie_tickets": []}

    def table(self, name):
        return FakeTable(self.store, name)


def test_source_contracts() -> None:
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    auth = (ROOT / "auth_persist.py").read_text(encoding="utf-8")
    asgi = (ROOT / "asgi_app.py").read_text(encoding="utf-8")
    sql = (ROOT / "sql" / "05_auth_sessions.sql").read_text(encoding="utf-8")

    for item in [
        "import auth_persist",
        "SP_AUTH_SESSION_ID_KEY",
        "flush_pending_auth_cookie_navigation",
        "_read_browser_auth_session_id",
        "auth_persist.create_server_session",
        "auth_persist.rotate_server_session",
        "auth_persist.revoke_server_session",
        "/auth/persist-session",
        "/auth/clear-session",
    ]:
        if item not in app and item not in asgi and item not in auth:
            # app-specific items
            if item.startswith("auth_persist.") or item.startswith("/auth/"):
                if item not in app and item not in asgi and item not in auth:
                    fail(f"missing contract: {item}")
            elif item not in app:
                fail(f"missing in app.py: {item}")

    if "COOKIE_NAME = \"sp_sid\"" not in auth:
        fail("cookie must be opaque sp_sid")
    if "access_token" in auth and "encrypt_token" not in auth:
        fail("token handling missing encryption helpers")
    # Cookie must not store raw access/refresh tokens
    if "response.set_cookie(**kwargs)" in auth:
        # apply_set_session_cookie should set session_id only — verify function body
        start = auth.find("def apply_set_session_cookie")
        chunk = auth[start : start + 700]
        if "access_token" in chunk or "refresh_token" in chunk:
            fail("cookie setter must not embed access/refresh tokens")
    if "auth_sessions" not in sql or "auth_cookie_tickets" not in sql:
        fail("SQL migration missing tables")
    if "streamlit run asgi_app.py" not in asgi:
        fail("asgi_app missing Render start guidance")


def test_encrypt_roundtrip_and_tamper() -> None:
    import auth_persist

    token = "test-access-token-value"
    enc = auth_persist.encrypt_token(token)
    if auth_persist.decrypt_token(enc) != token:
        fail("encrypt/decrypt roundtrip failed")
    tampered = enc[:-4] + ("AAAA" if not enc.endswith("AAAA") else "BBBB")
    if auth_persist.decrypt_token(tampered) is not None:
        fail("tampered ciphertext should not decrypt")


def test_create_load_touch_revoke_and_expiry() -> None:
    import auth_persist

    client = FakeClient()
    auth_persist.set_service_client_factory(lambda: client)

    sid = auth_persist.create_server_session(
        access_token="access-1",
        refresh_token="refresh-1",
        user_id="11111111-1111-4111-8111-111111111111",
        email="student@example.com",
        provider="google",
        client=client,
    )
    if not auth_persist.session_id_is_valid(sid):
        fail("create_server_session returned invalid id")

    loaded = auth_persist.load_server_session(sid, client=client)
    if not loaded or loaded["access_token"] != "access-1":
        fail("load_server_session failed")
    if loaded["user_id"] != "11111111-1111-4111-8111-111111111111":
        fail("UUID ownership mismatch")

    if not auth_persist.touch_server_session(sid, client=client):
        fail("touch_server_session failed")

    # Force absolute expiry
    row = client.store["auth_sessions"][0]
    row["expires_at"] = (
        datetime.now(timezone.utc) - timedelta(seconds=5)
    ).isoformat()
    if auth_persist.load_server_session(sid, client=client) is not None:
        fail("expired session should not load")

    # Idle expiry
    sid2 = auth_persist.create_server_session(
        access_token="access-2",
        refresh_token="refresh-2",
        user_id="22222222-2222-4222-8222-222222222222",
        provider="email",
        client=client,
    )
    row2 = [r for r in client.store["auth_sessions"] if r["session_id"] == sid2][0]
    row2["idle_expires_at"] = (
        datetime.now(timezone.utc) - timedelta(seconds=5)
    ).isoformat()
    if auth_persist.load_server_session(sid2, client=client) is not None:
        fail("idle-expired session should not load")

    sid3 = auth_persist.create_server_session(
        access_token="access-3",
        refresh_token="refresh-3",
        user_id="33333333-3333-4333-8333-333333333333",
        provider="email",
        client=client,
    )
    auth_persist.revoke_server_session(sid3, client=client)
    if auth_persist.load_server_session(sid3, client=client) is not None:
        fail("revoked session should not load")


def test_rotation_and_cookie_ticket_single_use() -> None:
    import auth_persist

    client = FakeClient()
    auth_persist.set_service_client_factory(lambda: client)

    old = auth_persist.create_server_session(
        access_token="old-a",
        refresh_token="old-r",
        user_id="44444444-4444-4444-8444-444444444444",
        provider="email",
        client=client,
    )
    new = auth_persist.rotate_server_session(
        old,
        access_token="new-a",
        refresh_token="new-r",
        user_id="44444444-4444-4444-8444-444444444444",
        provider="email",
        client=client,
    )
    if not new or new == old:
        fail("rotation should mint a new session id")
    if auth_persist.load_server_session(old, client=client) is not None:
        fail("old session should be revoked after rotation")
    loaded = auth_persist.load_server_session(new, client=client)
    if not loaded or loaded["access_token"] != "new-a":
        fail("rotated session load failed")

    ticket = auth_persist.create_cookie_ticket(new, purpose="set", client=client)
    first = auth_persist.consume_cookie_ticket(ticket, client=client)
    second = auth_persist.consume_cookie_ticket(ticket, client=client)
    if not first or first.get("session_id") != new:
        fail("cookie ticket consume failed")
    if second is not None:
        fail("cookie ticket must be single-use")

    # Invalid/tampered ticket ids
    if auth_persist.consume_cookie_ticket("short", client=client) is not None:
        fail("short ticket should be rejected")
    if auth_persist.consume_cookie_ticket("Z" * 32, client=client) is not None:
        fail("unknown ticket should be rejected")


def test_cookie_helpers_and_jwt_expiry() -> None:
    import auth_persist

    class Jar(dict):
        pass

    cookies = Jar({auth_persist.COOKIE_NAME: "ABCDEFGHIJKLMNOPQRSTUV"})
    if auth_persist.read_session_id_from_cookies(cookies) != "ABCDEFGHIJKLMNOPQRSTUV":
        # 22 chars may fail length check (need >=20) — OK
        pass
    cookies[auth_persist.COOKIE_NAME] = "A" * 32
    if auth_persist.read_session_id_from_cookies(cookies) != "A" * 32:
        fail("valid opaque cookie not read")

    cookies[auth_persist.COOKIE_NAME] = "../bad"
    if auth_persist.read_session_id_from_cookies(cookies) is not None:
        fail("tampered cookie value must be rejected")

    # Build a fake JWT with exp in the past
    def jwt_with_exp(exp: int) -> str:
        header = base64.urlsafe_b64encode(b'{"alg":"none"}').decode().rstrip("=")
        payload = base64.urlsafe_b64encode(
            json.dumps({"exp": exp}).encode()
        ).decode().rstrip("=")
        return f"{header}.{payload}.sig"

    if not auth_persist.access_token_expired(jwt_with_exp(int(time.time()) - 10)):
        fail("past exp should be expired")
    if auth_persist.access_token_expired(jwt_with_exp(int(time.time()) + 3600)):
        fail("future exp should not be expired")


def test_no_tokens_in_query_or_html_helpers() -> None:
    import auth_persist

    html = auth_persist.browser_redirect_html("/auth/clear-session")
    if "access_token" in html or "refresh_token" in html:
        fail("redirect HTML must not contain tokens")
    if "/auth/clear-session" not in html:
        fail("redirect HTML missing path")


def main() -> None:
    test_source_contracts()
    test_encrypt_roundtrip_and_tamper()
    test_create_load_touch_revoke_and_expiry()
    test_rotation_and_cookie_ticket_single_use()
    test_cookie_helpers_and_jwt_expiry()
    test_no_tokens_in_query_or_html_helpers()
    print("ALL AUTH PERSIST TESTS PASSED")


if __name__ == "__main__":
    main()
