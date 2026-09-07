"""Focused offline tests for Supabase Google OAuth callback + UUID ownership.

Run: python3 test_oauth_ownership_offline.py
Does not touch secrets, network, or live Auth.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest.mock import MagicMock

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
        "exchange_code_for_session",
        'sign_in_with_oauth',
        'SUPABASE_GOOGLE_OAUTH_REDIRECT_PROD = "https://stempathwaysnyc.com"',
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


def _load_ownership_helpers():
    fake_st = MagicMock()
    fake_st.cache_data = lambda **kw: (lambda f: f)
    fake_st.session_state = {}
    fake_st.query_params = {}
    sys.modules["streamlit"] = fake_st
    import streamlit as st  # noqa: F401

    ns = {
        "re": re,
        "st": fake_st,
        "html_module": __import__("html"),
        "datetime": __import__("datetime").datetime,
        "timezone": __import__("datetime").timezone,
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
                "@st.cache_data(show_spinner=False)\ndef list_all_auth_users_admin"
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

    # Callback helpers (pure functions + query clearing)
    ns["SUPABASE_GOOGLE_OAUTH_REDIRECT_PROD"] = "https://stempathwaysnyc.com"
    ns["SUPABASE_AUTH_STORAGE_KEY"] = "supabase.auth.token"
    exec(
        SOURCE[
            SOURCE.index("def supabase_google_oauth_redirect_to(") : SOURCE.index(
                "def start_supabase_google_oauth("
            )
        ],
        ns,
    )
    # Include process + clear helpers used by tests via exec of clear + process pieces
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

    # Matching email alone must never attach orphan rows.
    assert "orphan-google-sub" in {
        r["owner_id"]
        for r in ns["build_admin_unmatched_legacy_ownership_report"](
            auth_users, admin_data
        )
    }

    admin_data2 = dict(admin_data)
    admin_data2["identity_links"] = [
        {
            "google_user_sub": "orphan-google-sub",
            "auth_user_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "status": "approved",
        }
    ]
    names = {
        p["name"]
        for p in ns["build_admin_student_pathways"](auth_users, admin_data2)[0][
            "saved_programs"
        ]
    }
    assert "Legacy Prog" in names


def test_callback_query_clear_and_redirect_constant() -> None:
    ns, fake_st = _load_ownership_helpers()

    class _Params(dict):
        def keys(self):
            return dict.keys(self)

    fake_st.query_params = _Params(
        {
            "code": "AUTH_CODE_SHOULD_NOT_BE_LOGGED",
            "state": "STATE_SHOULD_NOT_BE_LOGGED",
            "auth": "signin",
        }
    )
    ns["_clear_oauth_query_params"]()
    assert "code" not in fake_st.query_params
    assert "state" not in fake_st.query_params
    assert fake_st.query_params.get("auth") == "signin"

    # Production host forces production redirect.
    fake_st.context.headers = {"Host": "stempathwaysnyc.com"}
    assert (
        ns["supabase_google_oauth_redirect_to"]()
        == "https://stempathwaysnyc.com"
    )


def test_process_callback_stores_uuid_owner() -> None:
    ns, fake_st = _load_ownership_helpers()

    # Load process_supabase_auth_callback + dependencies into ns
    exec(
        SOURCE[
            SOURCE.index("def _session_auth_storage(") : SOURCE.index(
                "def create_supabase_auth_client("
            )
        ],
        ns,
    )
    # constants already needed
    for name, value in (
        ("SP_EMAIL_AUTH_STATE_KEY", "sp_email_auth"),
        ("SP_OAUTH_CODE_VERIFIER_KEY", "_sp_oauth_code_verifier"),
        ("SP_OAUTH_CALLBACK_ERROR_KEY", "_sp_oauth_callback_error"),
        ("SP_AUTH_STORAGE_KEY", "_sp_supabase_auth_storage"),
        ("SP_APP_USER_CACHE_KEY", "_sp_app_user_cache"),
        ("SP_APP_USER_RUN_KEY", "_sp_app_user_run_id"),
        ("SUPABASE_AUTH_STORAGE_KEY", "supabase.auth.token"),
        ("AUTH_MSG_GOOGLE_CALLBACK", "Google sign-in could not be completed. Please try again."),
    ):
        ns[name] = value

    exec(
        SOURCE[
            SOURCE.index("def clear_email_auth_session(") : SOURCE.index(
                "def _current_script_run_id("
            )
        ],
        ns,
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
            assert "auth_code" in payload
            assert payload.get("code_verifier") == "test-verifier"
            # Ensure we never require email matching.
            assert "email" not in payload
            return MagicMock(user=FakeUser(), session=FakeSession())

    class FakeClient:
        auth = FakeAuth()

    ns["supabase_auth_configured"] = lambda: True
    ns["create_supabase_auth_client"] = lambda flow_type="pkce": FakeClient()
    ns["log_auth_event"] = lambda *a, **k: None

    fake_st.session_state = {
        ns["SP_OAUTH_CODE_VERIFIER_KEY"]: "test-verifier",
        ns["SP_AUTH_STORAGE_KEY"]: {},
    }
    fake_st.query_params = {"code": "one-time-auth-code"}

    ok = ns["process_supabase_auth_callback"]()
    assert ok is True
    stored = fake_st.session_state.get(ns["SP_EMAIL_AUTH_STATE_KEY"])
    assert stored["user_id"] == "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
    assert stored["provider"] == "google"
    assert "code" not in fake_st.query_params
    assert ns["SP_OAUTH_CODE_VERIFIER_KEY"] not in fake_st.session_state


if __name__ == "__main__":
    test_source_contracts()
    test_uuid_ownership_and_no_email_join()
    test_callback_query_clear_and_redirect_constant()
    test_process_callback_stores_uuid_owner()
    print("ALL_OFFLINE_OAUTH_TESTS_PASSED")
