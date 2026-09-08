"""Offline source contracts for student profile/privacy/account controls."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent
APP = (ROOT / "app.py").read_text(encoding="utf-8")
SQL = (ROOT / "sql/06_student_account_deletion.sql").read_text(encoding="utf-8")


def require(text, source, message):
    if text not in source:
        raise AssertionError(message)


def main():
    require("def clear_student_recommendation_state", APP, "missing reset helper")
    require("Regenerate Recommendations", APP, "missing regeneration control")
    require("clear_student_recommendation_state()", APP, "profile save does not clear stale results")
    require("Your information and privacy", APP, "missing privacy explanation")
    require("Type DELETE to confirm", APP, "missing typed delete confirmation")
    require("delete_account_acknowledged", APP, "missing deletion acknowledgement")
    require('supabase\n            .rpc("delete_student_account"', APP, "deletion must use server RPC")
    require("security definer", SQL.lower(), "deletion RPC must be security definer")
    require("set search_path = ''", SQL.lower(), "deletion RPC needs fixed search path")
    for table in (
        "saved_opportunities",
        "favorite_colleges",
        "user_feedback",
        "student_profiles",
        "account_identity_links",
        "auth_cookie_tickets",
        "auth_sessions",
        "auth.users",
    ):
        unqualified = f"delete from {table}"
        qualified = f"delete from public.{table}"
        if unqualified not in SQL.lower() and qualified not in SQL.lower():
            raise AssertionError(f"missing deletion for {table}")
    require("revoke all on function", SQL.lower(), "RPC access not revoked")
    require("to service_role", SQL.lower(), "RPC not restricted to service role")
    print("ALL STUDENT CONTROLS TESTS PASSED")


if __name__ == "__main__":
    main()
