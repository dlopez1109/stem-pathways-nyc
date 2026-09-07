"""Offline tests for hiding saved opportunities/colleges from discovery lists."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parent
SOURCE = (ROOT / "app.py").read_text(encoding="utf-8")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def test_source_contracts() -> None:
    required = [
        "def opportunity_catalog_id(",
        "def college_catalog_id(",
        "def user_saved_opportunity_catalog_ids(",
        "def user_favorite_college_catalog_ids(",
        "def invalidate_user_discovery_hide_caches(",
        "saved_opportunity_catalog_ids = user_saved_opportunity_catalog_ids",
        "favorite_college_catalog_ids = user_favorite_college_catalog_ids",
        "search_hidden_saved",
        "college_hidden_favorited",
        "You've already saved every opportunity that matches these filters",
        "You've already saved every college that matches these filters",
    ]
    for item in required:
        if item not in SOURCE:
            fail(f"missing: {item}")

    # Save/remove paths must invalidate caches so lists update immediately.
    for marker in (
        "invalidate_user_discovery_hide_caches(user_sub)",
        "st.rerun()",
    ):
        if SOURCE.count(marker) < 2:
            fail(f"expected multiple uses of {marker}")


def _slice_between(start_name: str, end_name: str) -> str:
    start = SOURCE.index(f"def {start_name}(")
    end = SOURCE.index(f"def {end_name}(")
    return SOURCE[start:end]


def _load_helpers():
    fake_st = MagicMock()
    fake_st.session_state = {}
    ns = {
        "re": re,
        "st": fake_st,
        "canonical_opportunity_name": lambda name: str(name or "").strip(),
        "normalize_college_name_key": lambda name: re.sub(
            r"[^a-z0-9]+", " ", str(name or "").strip().lower()
        ).strip(),
        "load_stem_college_catalog": lambda: [
            {
                "name": "MIT",
                "unitid": 166683,
                "official_name": "Massachusetts Institute of Technology",
            },
            {"name": "Stanford University", "unitid": 243744},
        ],
        "require_user_sub": lambda v: bool(
            re.fullmatch(
                r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
                r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                str(v or ""),
            )
        ),
        "load_saved_opportunities": lambda user_sub: [
            {"opportunity_name": "Regeneron Science Talent Search", "id": 1},
            {"opportunity_name": "Other Program", "id": 2},
        ],
        "load_favorite_colleges": lambda user_sub: [
            {"college_name": "MIT", "id": 11},
            {"college_name": "Stanford University", "id": 12},
        ],
    }
    # Pure helpers only — stop before load_favorite_colleges (needs supabase).
    exec(_slice_between("opportunity_catalog_id", "load_favorite_colleges"), ns)
    return ns, fake_st


def test_catalog_ids_and_user_sets() -> None:
    ns, fake_st = _load_helpers()
    opp_id = ns["opportunity_catalog_id"]({"name": "Regeneron Science Talent Search"})
    if not opp_id.startswith("opp:"):
        fail(f"bad opportunity id: {opp_id}")
    if opp_id != ns["opportunity_catalog_id"]("Regeneron Science Talent Search"):
        fail("opportunity id not stable across dict/string")

    mit = ns["college_catalog_id"]({"name": "MIT", "unitid": 166683})
    if mit != "unitid:166683":
        fail(f"expected unitid:166683, got {mit}")
    idx = ns["_college_unitid_by_name_index"]()
    if ns["college_catalog_id"]("MIT", unitid_by_name=idx) != "unitid:166683":
        fail("name index did not resolve MIT unitid")

    user = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    saved_ids = ns["user_saved_opportunity_catalog_ids"](user)
    if ns["opportunity_catalog_id"]("Regeneron Science Talent Search") not in saved_ids:
        fail("saved opportunity catalog id missing")
    fav_ids = ns["user_favorite_college_catalog_ids"](user)
    if "unitid:166683" not in fav_ids or "unitid:243744" not in fav_ids:
        fail(f"favorite college ids incomplete: {fav_ids}")

    if not fake_st.session_state:
        fail("expected session cache after load")
    ns["invalidate_user_discovery_hide_caches"](user)
    if f"_sp_saved_opp_catalog_ids_{user}" in fake_st.session_state:
        fail("cache not cleared after invalidate")


def test_filtering_logic() -> None:
    ns, _ = _load_helpers()
    user = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    saved = ns["user_saved_opportunity_catalog_ids"](user)
    rows = [
        {"name": "Regeneron Science Talent Search"},
        {"name": "Brand New Internship"},
    ]
    visible = [row for row in rows if ns["opportunity_catalog_id"](row) not in saved]
    if [r["name"] for r in visible] != ["Brand New Internship"]:
        fail(f"opportunity filter wrong: {visible}")

    fav = ns["user_favorite_college_catalog_ids"](user)
    colleges = [
        {"name": "MIT", "unitid": 166683},
        {"name": "Georgia Tech", "unitid": 139755},
    ]
    visible_c = [c for c in colleges if ns["college_catalog_id"](c) not in fav]
    if [c["name"] for c in visible_c] != ["Georgia Tech"]:
        fail(f"college filter wrong: {visible_c}")

    # Unsigned / invalid user must not hide anything.
    if ns["user_saved_opportunity_catalog_ids"]("not-a-uuid"):
        fail("invalid user should return empty saved set")
    if ns["user_favorite_college_catalog_ids"](""):
        fail("empty user should return empty favorite set")


if __name__ == "__main__":
    test_source_contracts()
    test_catalog_ids_and_user_sets()
    test_filtering_logic()
    print("ALL DISCOVERY HIDE TESTS PASSED")
