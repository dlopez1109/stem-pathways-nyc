"""Focused offline tests for Supabase Google OAuth callback + UUID ownership.

Run: python3 test_oauth_ownership_offline.py
Does not touch secrets, network, or live Auth.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse, quote_plus

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.py"
SOURCE = APP.read_text(encoding="utf-8")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def test_source_contracts() -> None:
    required = [
        "def start_supabase_google_oauth(",
        "def process_supabase_auth_callback(",
        "def _store_oauth_pkce_ticket(",
        "def _consume_oauth_pkce_ticket(",
        "exchange_code_for_session",
        "sign_in_with_oauth",
        'SUPABASE_GOOGLE_OAUTH_REDIRECT_PROD = "https://stempathwaysnyc.com"',
        "OAUTH_PKCE_TICKET_TTL_SECONDS = 10 * 60",
        "oauth_pkce_tickets",
        "google_oauth_ticket_missing",
        "google_oauth_ticket_expired",
        "google_oauth_ticket_reused",
        "google_oauth_ticket_invalid",
        "def is_canonical_auth_uuid(",
        "def require_user_sub(",
    ]
    for item in required:
        if item not in SOURCE:
            fail(f"missing required symbol/text: {item}")

    forbidden = [
        "sign_in_with_id_token",
        'st.login("google")',
        "def resolve_google_supabase_auth_user(",
        "def _get_streamlit_google_id_token(",
        "auth.expose_tokens",
        "Passed nonce and nonce in id_token",
    ]
    for item in forbidden:
        if item in SOURCE:
            fail(f"forbidden leftover present: {item}")

    # Verifier must not be kept as the redirect persistence mechanism.
    if "st.session_state[SP_OAUTH_CODE_VERIFIER_KEY] = str(verifier)" in SOURCE:
        fail("raw verifier still written into session_state for redirect persistence")


def _load_ownership_helpers():
    fake_st = MagicMock()
    fake_st.cache_data = lambda **kw: (lambda f: f)
    fake_st.session_state = {}
    fake_st.query_params = {}
    sys.modules["streamlit"] = fake_st

    ns = {
        "re": re,
        "st": fake_st,
        "html_module": __import__("html"),
        "datetime": datetime,
        "timezone": timezone,
        "ZoneInfo": __import__("zoneinfo").ZoneInfo,
        "logger": MagicMock(),
        "supabase": MagicMock(),
        "supabase_connected": True,
        "log_supabase_exception": lambda *a, **k: None,
        "log_auth_event": lambda *a, **k: None,
        "text_to_list": lambda v: (
            [x.strip() for x in str(v or "").split(";") if x.strip()]
            if not isinstance(v, list)
            else [str(x).strip() for x in v if str(x).strip()]
        ),
        "personalized_stem_major_explanation": lambda field, profile=None, **k: f"Reason for {field}",
        "canonicalize_stem_field": lambda x: str(x or "").strip(),
        "ClientOptions": MagicMock(),
        "create_client": MagicMock(),
        "secrets": __import__("secrets"),
        "parse_qs": parse_qs,
        "urlencode": urlencode,
        "urlparse": urlparse,
        "urlunparse": urlunparse,
        "quote_plus": quote_plus,
    }

    exec(
        SOURCE[
            SOURCE.index("_AUTH_UUID_RE = re.compile(") : SOURCE.index(
                "def log_supabase_exception"
            )
        ],
        ns,
    )
    exec(
        SOURCE[
            SOURCE.index("ADMIN_OWNER_ID_CANDIDATES = (") : SOURCE.index(
                "def clear_admin_accounts_caches():"
            )
        ],
        ns,
    )
    exec(
        SOURCE[
            SOURCE.index("def _admin_format_created_at") : SOURCE.index(
                "@st.cache_data(show_spinner=False, ttl=300, max_entries=2)\n"
                "def list_all_auth_users_admin"
            )
        ],
        ns,
    )
    exec(
        SOURCE[
            SOURCE.index("def admin_reproducible_major_recommendations") : SOURCE.index(
                "\ndef parse_confirmed_deadline"
            )
        ],
        ns,
    )

    ns["SUPABASE_GOOGLE_OAUTH_REDIRECT_PROD"] = "https://stempathwaysnyc.com"
    ns["SUPABASE_AUTH_STORAGE_KEY"] = "supabase.auth.token"
    ns["SP_OAUTH_TICKET_QUERY_KEY"] = "sp_oauth"
    ns["OAUTH_PKCE_TICKET_TTL_SECONDS"] = 10 * 60
    ns["OAUTH_PKCE_TICKETS_TABLE"] = "oauth_pkce_tickets"
    ns["_OAUTH_TICKET_ID_RE"] = re.compile(r"^[A-Za-z0-9_-]{20,128}$")

    exec(
        SOURCE[
            SOURCE.index("def supabase_google_oauth_redirect_to(") : SOURCE.index(
                "def _clear_oauth_query_params("
            )
        ],
        ns,
    )
    exec(
        SOURCE[
            SOURCE.index("def _clear_oauth_query_params(") : SOURCE.index(
                "def _redirect_browser_to("
            )
        ],
        ns,
    )
    return ns, fake_st


def test_uuid_ownership_and_no_email_join() -> None:
    ns, _ = _load_ownership_helpers()
    assert ns["require_user_sub"]("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
    assert not ns["require_user_sub"]("google-oidc-sub-123")
    assert not ns["require_user_sub"]("student@example.com")

    auth_users = [
        {
            "user_sub": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "email": "student@example.com",
            "created_at": "2026-01-01T00:00:00Z",
            "display_name": "Student",
            "google_provider_subs": ["legacy-google-sub"],
        }
    ]
    admin_data = {
        "profiles": [
            {
                "user_sub": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "first_name": "A",
                "last_name": "B",
                "interests": "Robotics",
                "grade": "10",
                "borough": "Bronx",
            },
            {
                "user_sub": "orphan-google-sub",
                "first_name": "Old",
                "last_name": "Google",
                "interests": "Biology",
            },
        ],
        "saved_opportunities": [
            {
                "user_sub": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "opportunity_name": "Prog A",
                "status": "Saved",
            },
            {
                "user_sub": "orphan-google-sub",
                "opportunity_name": "Legacy Prog",
                "status": "Applying",
            },
        ],
        "favorite_colleges": [
            {
                "user_sub": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "college_name": "MIT",
            }
        ],
        "feedback": [],
        "identity_links": [],
        "profile_owner_column": "user_sub",
        "saved_owner_column": "user_sub",
        "favorite_owner_column": "user_sub",
    }

    pathways = ns["build_admin_student_pathways"](auth_users, admin_data)
    assert pathways[0]["profile_complete"]
    assert all(p["name"] != "Legacy Prog" for p in pathways[0]["saved_programs"])
    assert "orphan-google-sub" in {
        r["owner_id"]
        for r in ns["build_admin_unmatched_legacy_ownership_report"](
            auth_users, admin_data
        )
    }


def test_callback_query_clear_and_redirect_constant() -> None:
    ns, fake_st = _load_ownership_helpers()

    class _Params(dict):
        def keys(self):
            return dict.keys(self)

    fake_st.query_params = _Params(
        {
            "code": "AUTH_CODE_SHOULD_NOT_BE_LOGGED",
            "state": "STATE_SHOULD_NOT_BE_LOGGED",
            "sp_oauth": "TICKET_SHOULD_NOT_BE_LOGGED",
            "auth": "signin",
        }
    )
    ns["_clear_oauth_query_params"]()
    assert "code" not in fake_st.query_params
    assert "state" not in fake_st.query_params
    assert "sp_oauth" not in fake_st.query_params
    assert fake_st.query_params.get("auth") == "signin"

    fake_st.context.headers = {"Host": "stempathwaysnyc.com"}
    assert ns["supabase_google_oauth_redirect_to"]() == "https://stempathwaysnyc.com"


def test_ticket_redirect_contains_only_opaque_ticket() -> None:
    ns, _ = _load_ownership_helpers()
    exec(
        SOURCE[
            SOURCE.index("def _oauth_ticket_id_is_valid(") : SOURCE.index(
                "def _store_oauth_pkce_ticket("
            )
        ],
        ns,
    )
    ticket = "A" * 32
    redirect = ns["_append_oauth_ticket_to_redirect"](
        "https://stempathwaysnyc.com", ticket
    )
    assert redirect.startswith("https://stempathwaysnyc.com/?sp_oauth=")
    assert "code_verifier" not in redirect
    assert "access_token" not in redirect
    qs = parse_qs(urlparse(redirect).query)
    assert qs["sp_oauth"] == [ticket]


def test_consume_ticket_rejects_expired_and_reused() -> None:
    ns, _ = _load_ownership_helpers()
    events = []
    ns["log_auth_event"] = lambda action, error=None: events.append(action)
    ns["supabase_connected"] = True

    class FakeTable:
        def __init__(self):
            self._op = "select"
            self.row = None

        def update(self, *_a, **_k):
            self._op = "update"
            return self

        def select(self, *_a, **_k):
            if self._op != "update":
                self._op = "select"
            return self

        def eq(self, *_a, **_k):
            return self

        def is_(self, *_a, **_k):
            return self

        def gt(self, *_a, **_k):
            return self

        def limit(self, *_a, **_k):
            return self

        def insert(self, *_a, **_k):
            self._op = "insert"
            return self

        def execute(self):
            if self._op == "update":
                # atomic consume misses for these negative cases
                self._op = "select"
                return MagicMock(data=[])
            return MagicMock(data=[self.row] if self.row else [])

    table = FakeTable()
    ns["supabase"] = MagicMock()
    ns["supabase"].table.return_value = table
    ns["OAUTH_PKCE_TICKETS_TABLE"] = "oauth_pkce_tickets"
    ns["_OAUTH_TICKET_ID_RE"] = re.compile(r"^[A-Za-z0-9_-]{20,128}$")

    exec(
        SOURCE[
            SOURCE.index("def _oauth_ticket_id_is_valid(") : SOURCE.index(
                "def _oauth_authorize_url_with_ticket("
            )
            if "def _oauth_authorize_url_with_ticket(" in SOURCE
            else SOURCE.index("def start_supabase_google_oauth(")
        ],
        ns,
    )

    # Reused
    events.clear()
    table.row = {
        "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat(),
        "consumed_at": datetime.now(timezone.utc).isoformat(),
    }
    assert ns["_consume_oauth_pkce_ticket"]("B" * 32) is None
    assert "google_oauth_ticket_reused" in events

    # Expired
    events.clear()
    table.row = {
        "expires_at": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(),
        "consumed_at": None,
    }
    assert ns["_consume_oauth_pkce_ticket"]("C" * 32) is None
    assert "google_oauth_ticket_expired" in events

    # Missing
    events.clear()
    table.row = None
    assert ns["_consume_oauth_pkce_ticket"]("D" * 32) is None
    assert "google_oauth_ticket_missing" in events

    # Invalid format
    events.clear()
    assert ns["_consume_oauth_pkce_ticket"]("short") is None
    assert "google_oauth_ticket_invalid" in events


def test_process_callback_uses_ticket_not_session_verifier() -> None:
    ns, fake_st = _load_ownership_helpers()

    for name, value in (
        ("SP_EMAIL_AUTH_STATE_KEY", "sp_email_auth"),
        ("SP_OAUTH_CODE_VERIFIER_KEY", "_sp_oauth_code_verifier"),
        ("SP_OAUTH_CALLBACK_ERROR_KEY", "_sp_oauth_callback_error"),
        ("SP_AUTH_STORAGE_KEY", "_sp_supabase_auth_storage"),
        ("SP_APP_USER_CACHE_KEY", "_sp_app_user_cache"),
        ("SP_APP_USER_RUN_KEY", "_sp_app_user_run_id"),
        ("SP_OAUTH_TICKET_QUERY_KEY", "sp_oauth"),
        ("SUPABASE_AUTH_STORAGE_KEY", "supabase.auth.token"),
        ("AUTH_MSG_GOOGLE_CALLBACK", "Google sign-in could not be completed. Please try again."),
        ("OAUTH_PKCE_TICKETS_TABLE", "oauth_pkce_tickets"),
        ("OAUTH_PKCE_TICKET_TTL_SECONDS", 600),
    ):
        ns[name] = value
    ns["_OAUTH_TICKET_ID_RE"] = re.compile(r"^[A-Za-z0-9_-]{20,128}$")

    exec(
        SOURCE[
            SOURCE.index("def _session_auth_storage(") : SOURCE.index(
                "def create_supabase_auth_client("
            )
        ],
        ns,
    )
    exec(
        SOURCE[
            SOURCE.index("def clear_email_auth_session(") : SOURCE.index(
                "def _current_script_run_id("
            )
        ],
        ns,
    )
    # Durable cookie persistence helpers (mocked — no DB / cryptography).
    fake_auth_persist = MagicMock()
    fake_auth_persist.session_id_is_valid = lambda value: bool(
        value and len(str(value)) >= 20
    )
    fake_auth_persist.persist_secret_configured = lambda: True
    fake_auth_persist.create_cookie_ticket = lambda *a, **k: "T" * 32
    fake_auth_persist.create_server_session = lambda **k: "S" * 32
    fake_auth_persist.rotate_server_session = lambda *a, **k: "S" * 32
    fake_auth_persist.revoke_server_session = lambda *a, **k: True
    fake_auth_persist.load_server_session = lambda *a, **k: None
    fake_auth_persist.touch_server_session = lambda *a, **k: True
    fake_auth_persist.access_token_expired = lambda *a, **k: False
    fake_auth_persist.read_session_id_from_cookies = lambda *a, **k: None
    ns["auth_persist"] = fake_auth_persist
    ns["time"] = __import__("time")
    ns["SP_AUTH_SESSION_ID_KEY"] = "_sp_auth_session_id"
    ns["SP_AUTH_COOKIE_NAV_KEY"] = "_sp_auth_cookie_nav"
    ns["SP_AUTH_VALIDATED_AT_KEY"] = "_sp_auth_validated_at"
    ns["SP_AUTH_TOUCHED_AT_KEY"] = "_sp_auth_idle_touched_at"
    ns["PAGE_TO_PATH"] = {"Dashboard": "/dashboard"}
    ns["urlencode"] = __import__("urllib.parse", fromlist=["urlencode"]).urlencode
    ns["AUTH_REVALIDATE_SECONDS"] = 10 * 60
    ns["AUTH_IDLE_TOUCH_SECONDS"] = 30 * 60
    ns["SP_EMAIL_AUTH_STATE_KEY"] = "sp_email_auth"
    ns["SP_APP_USER_CACHE_KEY"] = "_sp_app_user_cache"
    ns["SP_APP_USER_RUN_KEY"] = "_sp_app_user_run_id"
    ns["_auth_timing_log"] = lambda *a, **k: None
    ns["is_canonical_auth_uuid"] = ns.get(
        "is_canonical_auth_uuid",
        lambda value: bool(
            re.fullmatch(
                r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
                r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                str(value or ""),
            )
        ),
    )

    exec(
        SOURCE[
            SOURCE.index("def _auth_user_display_name(") : SOURCE.index(
                "def password_meets_requirements("
            )
        ],
        ns,
    )
    exec(
        SOURCE[
            SOURCE.index("def _oauth_ticket_id_is_valid(") : SOURCE.index(
                "def start_supabase_google_oauth("
            )
        ],
        ns,
    )
    exec(
        SOURCE[
            SOURCE.index("def process_supabase_auth_callback(") : SOURCE.index(
                "def get_app_user("
            )
        ],
        ns,
    )

    class FakeUser:
        def __init__(self):
            self.id = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
            self.email = "google.user@example.com"
            self.user_metadata = {"full_name": "Google User"}

    class FakeSession:
        access_token = "access-token-value"
        refresh_token = "refresh-token-value"

    class FakeAuth:
        def exchange_code_for_session(self, payload):
            assert payload.get("code_verifier") == "server-ticket-verifier"
            assert "email" not in payload
            return MagicMock(user=FakeUser(), session=FakeSession())

    class FakeClient:
        auth = FakeAuth()

    ns["supabase_auth_configured"] = lambda: True
    ns["create_supabase_auth_client"] = lambda flow_type="pkce": FakeClient()
    ns["_consume_oauth_pkce_ticket"] = (
        lambda ticket_id: "server-ticket-verifier" if ticket_id == ("E" * 32) else None
    )
    ns["log_auth_event"] = lambda *a, **k: None

    fake_st.session_state = {ns["SP_AUTH_STORAGE_KEY"]: {}}
    fake_st.query_params = {
        "code": "one-time-auth-code",
        "sp_oauth": "E" * 32,
    }

    ok = ns["process_supabase_auth_callback"]()
    assert ok is True
    stored = fake_st.session_state.get(ns["SP_EMAIL_AUTH_STATE_KEY"])
    assert stored["user_id"] == "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
    assert stored["provider"] == "google"
    assert "code" not in fake_st.query_params
    assert "sp_oauth" not in fake_st.query_params


if __name__ == "__main__":
    test_source_contracts()
    test_uuid_ownership_and_no_email_join()
    test_callback_query_clear_and_redirect_constant()
    test_ticket_redirect_contains_only_opaque_ticket()
    test_consume_ticket_rejects_expired_and_reused()
    test_process_callback_uses_ticket_not_session_verifier()
    print("ALL_OFFLINE_OAUTH_TESTS_PASSED")
