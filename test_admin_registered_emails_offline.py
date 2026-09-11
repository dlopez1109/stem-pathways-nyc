"""Offline tests for Admin Dashboard Registered Account Emails.

Run: python3 test_admin_registered_emails_offline.py
Does not touch secrets, network, or live Auth.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.py"
SOURCE = APP.read_text(encoding="utf-8")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def test_source_contracts() -> None:
    required = [
        'Registered Account Emails',
        "def paginate_auth_admin_list_users(",
        "def build_admin_registered_account_emails(",
        "def list_all_auth_users_admin(",
        "admin_registered_emails_search",
        "admin_registered_emails_page",
        "Total Authentication accounts:",
        "Sign-in provider",
        "Email confirmation",
        "Do not export or download these student records.",
    ]
    for item in required:
        if item not in SOURCE:
            fail(f"missing required symbol/text: {item}")

    # Must stay behind the existing admin gate on the Admin Dashboard page.
    admin_page = SOURCE[
        SOURCE.index('elif page == "Admin Dashboard":') : SOURCE.index(
            'elif page == "Feedback":'
        )
    ]
    if "is_admin_user(" not in admin_page:
        fail("Admin Dashboard missing is_admin_user authorization check")
    if "Registered Account Emails" not in admin_page:
        fail("Registered Account Emails section not inside Admin Dashboard")
    if admin_page.index("is_admin_user(") > admin_page.index(
        "Registered Account Emails"
    ):
        fail("Registered Account Emails appears before admin authorization check")

    forbidden_ui = [
        "st.download_button",
        "to_csv(",
        "application/octet-stream",
    ]
    emails_section = admin_page[
        admin_page.index("Registered Account Emails") : admin_page.index(
            "COMPACT FEEDBACK SUMMARY"
        )
    ]
    for item in forbidden_ui:
        if item in emails_section:
            fail(f"export/download helper present in emails section: {item}")


def _load_admin_email_helpers():
    fake_st = MagicMock()
    fake_st.cache_data = lambda **kw: (lambda f: f)
    fake_st.session_state = {}
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
        "is_canonical_auth_uuid": lambda value: bool(
            re.fullmatch(
                r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
                r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                str(value or "").strip(),
            )
        ),
    }

    exec(
        SOURCE[
            SOURCE.index("def _google_identity_provider_subs_from_auth_user(") : SOURCE.index(
                "def supabase_google_oauth_redirect_to("
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
            SOURCE.index("def _admin_safe_display_name(") : SOURCE.index(
                "@st.cache_data(show_spinner=False, ttl=300, max_entries=2)\n"
                "def list_all_auth_users_admin"
            )
        ],
        ns,
    )
    return ns


def test_paginate_auth_admin_list_users_loads_multiple_pages() -> None:
    ns = _load_admin_email_helpers()

    page1 = [
        SimpleNamespace(
            id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            email="newer@example.com",
            created_at="2026-03-01T12:00:00+00:00",
            user_metadata={"full_name": "Newer"},
            app_metadata={"provider": "google", "providers": ["google"]},
            identities=[SimpleNamespace(provider="google", id="g-sub-1", identity_data={})],
            email_confirmed_at="2026-03-01T12:00:01+00:00",
            confirmed_at=None,
        ),
        SimpleNamespace(
            id="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            email="mid@example.com",
            created_at="2026-02-01T12:00:00+00:00",
            user_metadata={},
            app_metadata={"provider": "email", "providers": ["email"]},
            identities=[SimpleNamespace(provider="email", id="e-1", identity_data={})],
            email_confirmed_at=None,
            confirmed_at=None,
        ),
    ]
    page2 = [
        SimpleNamespace(
            id="cccccccc-cccc-cccc-cccc-cccccccccccc",
            email="older@example.com",
            created_at="2026-01-01T12:00:00+00:00",
            user_metadata={},
            app_metadata={"providers": ["email", "google"]},
            identities=[
                SimpleNamespace(provider="email", id="e-2", identity_data={}),
                SimpleNamespace(provider="google", id="g-sub-2", identity_data={}),
            ],
            email_confirmed_at="2026-01-02T00:00:00+00:00",
            confirmed_at=None,
        ),
    ]

    calls = []

    def list_users(page=1, per_page=100):
        calls.append({"page": page, "per_page": per_page})
        if page == 1:
            return page1
        if page == 2:
            return page2
        return []

    admin_api = SimpleNamespace(list_users=list_users)
    users = ns["paginate_auth_admin_list_users"](admin_api, per_page=2, max_pages=10)

    if len(calls) < 2:
        fail(f"expected multiple Auth Admin list_users pages, got calls={calls}")
    if calls[0]["page"] != 1 or calls[1]["page"] != 2:
        fail(f"unexpected page order: {calls}")
    if len(users) != 3:
        fail(f"expected 3 users across pages, got {len(users)}")
    if [u["email"] for u in users] != [
        "newer@example.com",
        "mid@example.com",
        "older@example.com",
    ]:
        fail(f"users not sorted newest-first: {[u['email'] for u in users]}")

    newer = users[0]
    if newer["sign_in_provider"] != "Google":
        fail(f"expected Google provider, got {newer['sign_in_provider']!r}")
    if newer["email_confirmed"] is not True:
        fail("expected newer account email_confirmed True")
    if users[1]["email_confirmed"] is not False:
        fail("expected mid account email_confirmed False")
    if users[2]["sign_in_provider"] != "Email + Google":
        fail(f"expected Email + Google, got {users[2]['sign_in_provider']!r}")

    # Safe fields only in the display-oriented keys.
    for user in users:
        for banned in (
            "password",
            "access_token",
            "refresh_token",
            "provider_token",
            "provider_id",
            "identity_id",
        ):
            if banned in user:
                fail(f"banned credential field leaked into auth user row: {banned}")


def test_build_registered_account_emails_joins_by_uuid_not_email() -> None:
    ns = _load_admin_email_helpers()

    auth_users = [
        {
            "user_sub": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "email": "matched@example.com",
            "created_at": "2026-02-01T00:00:00Z",
            "sign_in_provider": "Google",
            "email_confirmed": True,
        },
        {
            "user_sub": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "email": "noprofile@example.com",
            "created_at": "2026-03-01T00:00:00Z",
            "sign_in_provider": "Email",
            "email_confirmed": False,
        },
    ]
    admin_data = {
        "profiles": [
            {
                # Same email as the incomplete Auth user, but owned by UUID A.
                # Join must use UUID, so only A is profile-complete.
                "user_sub": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "email": "noprofile@example.com",
                "first_name": "A",
            },
            {
                "user_sub": "orphan-owner",
                "email": "matched@example.com",
                "first_name": "Orphan",
            },
        ],
        "identity_links": [],
        "profile_owner_column": "user_sub",
    }

    rows = ns["build_admin_registered_account_emails"](auth_users, admin_data)
    if len(rows) != 2:
        fail(f"expected both Auth accounts, got {len(rows)}")
    if [r["email"] for r in rows] != [
        "noprofile@example.com",
        "matched@example.com",
    ]:
        fail(f"expected newest-first emails, got {[r['email'] for r in rows]}")

    by_sub = {r["user_sub"]: r for r in rows}
    if by_sub["aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"]["profile_complete"] is not True:
        fail("UUID-matched profile should mark profile_complete True")
    if by_sub["bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"]["profile_complete"] is not False:
        fail("email-only profile match must not mark profile_complete True")


def main() -> None:
    test_source_contracts()
    test_paginate_auth_admin_list_users_loads_multiple_pages()
    test_build_registered_account_emails_joins_by_uuid_not_email()
    print("PASS: admin registered emails offline tests")


if __name__ == "__main__":
    main()
