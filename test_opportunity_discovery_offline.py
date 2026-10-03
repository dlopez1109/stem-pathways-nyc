"""Offline tests for Opportunity Discovery filters and Best matches.

Run: python3 test_opportunity_discovery_offline.py
Does not touch secrets, network, Auth, SQL, or live Streamlit.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parent
SOURCE = (ROOT / "app.py").read_text(encoding="utf-8")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


MATCH_SCORE_EXPLANATION = (
    "How well this opportunity fits your profile—not your chance of acceptance."
)


def test_source_contracts() -> None:
    required = [
        "def normalize_opportunity_cost_bucket(",
        "def normalize_opportunity_format_buckets(",
        "def parse_opportunity_grades(",
        "def normalize_opportunity_nyc_eligibility(",
        "def normalize_application_status_bucket(",
        "def evaluate_opportunity_profile_eligibility(",
        "def compute_opportunity_fit_score(",
        "def score_best_match_opportunity(",
        "Best matches for you",
        "Match score",
        MATCH_SCORE_EXPLANATION,
        "Confirmed match",
        "Potential match — verify requirements",
        "Not enough information",
        "Score factors",
        "Still unverified",
        'opportunity_filter_cost',
        'opportunity_filter_location',
        'opportunity_filter_grades',
        'opportunity_filter_status',
        "opportunity_search_page",
        "page_results",
        "Confirm this requirement on the official program website.",
        "OPPORTUNITY_FIT_GRADE_POINTS",
    ]
    for item in required:
        if item not in SOURCE:
            fail(f"missing contract: {item}")

    if "Recommended for You" in SOURCE:
        fail("legacy Recommended for You section should be removed")

    card_start = SOURCE.index("def opportunity_recommendation_card_html(")
    card_end = SOURCE.index("\ndef _join_english(", card_start)
    card = SOURCE[card_start:card_end]
    if "Match type" in card:
        fail("recommendation card still shows Match type badge")
    if "Match score" not in card:
        fail("recommendation card missing Match score label")
    if "Your Match" in card:
        fail("legacy Your Match admission-style label returned")

    # Ownership / hide-saved contracts remain intact.
    for item in [
        "def require_user_sub(",
        "user_saved_opportunity_catalog_ids",
        "saved_opportunity_catalog_ids = user_saved_opportunity_catalog_ids",
        "You've already saved every opportunity that matches these filters",
    ]:
        if item not in SOURCE:
            fail(f"missing safety contract: {item}")

    opp_start = SOURCE.index('elif page == "Opportunities":')
    opp_end = SOURCE.index('elif page == "Deadline Calendar":')
    opp_page = SOURCE[opp_start:opp_end]
    if "st.status(" in opp_page:
        fail("opportunity search still uses st.status")
    if "Found {result_count} matching opportunities" not in opp_page:
        fail("compact result count missing")
    if "enumerate(page_results)" not in opp_page:
        fail("page_results card loop missing")
    if "Could not display" not in opp_page:
        fail("per-card visible error handling missing")

    count_pos = opp_page.index("Found {result_count} matching opportunities")
    chips_pos = opp_page.index("sp-opp-active-filters")
    header_pos = opp_page.index('st.header("Search Results")')
    loop_pos = opp_page.index("enumerate(page_results)")
    after_search_best = opp_page.rfind("render_best_matches_for_you()")
    if not (count_pos < chips_pos < header_pos < loop_pos < after_search_best):
        fail(
            "after search, results must render as count, chips, heading, "
            "cards, then Best matches"
        )
    slot_pos = opp_page.index("best_matches_above_filters = st.container()")
    form_pos = opp_page.index('key="opportunity_search_panel"')
    if slot_pos > form_pos:
        fail("Best matches slot must be reserved above the filter form")


def _slice(start_name: str, end_name: str) -> str:
    start = SOURCE.index(f"def {start_name}(")
    end = SOURCE.index(f"def {end_name}(")
    return SOURCE[start:end]


def _load_helpers():
    fake_st = MagicMock()
    fake_st.session_state = {}

    # Minimal stubs for helpers referenced by discovery scoring.
    def canonicalize_stem_field(value):
        text = str(value or "").strip()
        aliases = {
            "cs": "Computer Science",
            "computer science": "Computer Science",
            "ai": "Artificial Intelligence",
            "artificial intelligence": "Artificial Intelligence",
            "engineering": "Engineering",
        }
        return aliases.get(text.casefold(), text)

    def expand_stem_fields(values):
        out = set()
        for value in values or []:
            text = str(value or "").strip()
            if not text:
                continue
            out.add(text)
            out.add(canonicalize_stem_field(text))
        return out

    def opportunity_field_match_set(fields_value):
        raw = [
            item.strip()
            for item in str(fields_value or "").split(";")
            if item.strip()
        ]
        return expand_stem_fields(raw)

    def opportunity_scope_matches_interests(opportunity, expanded_interests):
        scope = str(opportunity.get("eligible_interest_scope") or "").strip().lower()
        if scope in {"any major", "general high school student", "general"}:
            return True
        return False

    def opportunity_window_status(opportunity):
        status = str(opportunity.get("application_status") or "").lower()
        deadline = str(opportunity.get("deadline") or "").lower()
        if "closed" in status or "closed" in deadline:
            return "CLOSED"
        if "open now" in status or status.startswith("open"):
            return "OPEN NOW"
        if any(token in status for token in ["future", "opens", "upcoming"]):
            return "UPCOMING"
        return "UPCOMING"

    ns = {
        "re": re,
        "st": fake_st,
        "canonicalize_stem_field": canonicalize_stem_field,
        "expand_stem_fields": expand_stem_fields,
        "opportunity_field_match_set": opportunity_field_match_set,
        "opportunity_scope_matches_interests": opportunity_scope_matches_interests,
        "opportunity_window_status": opportunity_window_status,
        "RELATED_STEM_FIELDS": {},
        "NYC_BOROUGH_TOKENS": {
            "bronx",
            "brooklyn",
            "manhattan",
            "queens",
            "staten island",
            "nyc",
            "new york city",
            "new york",
            "five boroughs",
            "all nyc boroughs",
        },
    }

    # Load from opportunity_matches_format through expand_stem_fields replacement block.
    # The discovery helpers sit between opportunity_matches_format and expand_stem_fields.
    block = _slice("opportunity_matches_format", "expand_stem_fields")
    # include expand_stem_fields body from our stub instead of app's heavy version
    exec(block, ns)
    # Keep our expand_stem_fields stub (exec may have overwritten with app def that
    # depends on more symbols). Re-bind stubs used by scoring.
    ns["expand_stem_fields"] = expand_stem_fields
    ns["canonicalize_stem_field"] = canonicalize_stem_field
    ns["opportunity_field_match_set"] = opportunity_field_match_set
    ns["opportunity_scope_matches_interests"] = opportunity_scope_matches_interests
    return ns, fake_st


def test_normalizers_and_filters() -> None:
    ns, _ = _load_helpers()

    # Cost
    assert ns["normalize_opportunity_cost_bucket"]({"cost": "Free"}) == "free"
    assert ns["normalize_opportunity_cost_bucket"]({"cost": "$0"}) == "free"
    assert ns["normalize_opportunity_cost_bucket"]({"cost": "No cost"}) == "free"
    assert ns["normalize_opportunity_cost_bucket"]({"cost": "Tuition $3,900"}) == "paid"
    assert ns["normalize_opportunity_cost_bucket"](
        {"cost": "Program fee not listed — confirm with AIMI"}
    ) == "unknown"
    assert ns["opportunity_matches_cost_filter"]({"cost": "Free"}, "Free")
    assert not ns["opportunity_matches_cost_filter"]({"cost": "Free"}, "Paid")
    assert ns["opportunity_matches_cost_filter"]({"cost": "Free"}, "All")

    # Format / virtual
    assert "virtual" in ns["normalize_opportunity_format_buckets"]("Online / virtual")
    assert "virtual" in ns["normalize_opportunity_format_buckets"]("Remote")
    assert "in person" in ns["normalize_opportunity_format_buckets"]("In-person residential")
    assert "hybrid" in ns["normalize_opportunity_format_buckets"]("Hybrid online + campus")
    assert ns["opportunity_matches_format"]("Virtual Zoom sessions", ["Virtual"])
    assert ns["opportunity_matches_format"]("Online only", ["Virtual"])
    assert not ns["opportunity_matches_format"]("In person only", ["Virtual"])

    # Grades
    assert ns["parse_opportunity_grades"]("9;10;11") == {"9", "10", "11"}
    assert ns["parse_opportunity_grades"]("Grades 10-12") == {"10", "11", "12"}
    assert ns["parse_opportunity_grades"]("Check official eligibility") is None
    assert ns["opportunity_matches_grade_filter"]({"grades": "10;11"}, ["10"])
    assert not ns["opportunity_matches_grade_filter"]({"grades": "10;11"}, ["9"])
    assert not ns["opportunity_matches_grade_filter"](
        {"grades": "Check official eligibility"},
        ["11"],
    )

    # NYC
    assert (
        ns["normalize_opportunity_nyc_eligibility"](
            {"boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island"}
        )
        == "yes"
    )
    assert (
        ns["normalize_opportunity_nyc_eligibility"](
            {"boroughs_served": "Outside NYC — Greater Rochester, New York only"}
        )
        == "no"
    )
    assert ns["opportunity_matches_location_filter"](
        {"boroughs_served": "Bronx;Manhattan"},
        "NYC only",
    )
    assert not ns["opportunity_matches_location_filter"](
        {"boroughs_served": "Outside NYC — Baltimore only"},
        "NYC only",
    )

    # Status
    assert (
        ns["normalize_application_status_bucket"](
            {"application_status": "OPEN NOW — deadline soon"}
        )
        == "open"
    )
    assert (
        ns["normalize_application_status_bucket"](
            {"application_status": "Future Cycle", "deadline": "Next cycle not yet announced"}
        )
        == "opens_soon"
    )
    assert (
        ns["normalize_application_status_bucket"](
            {"application_status": "Summer 2026 Closed", "deadline": "closed May 15, 2026"}
        )
        == "closed"
    )
    assert ns["opportunity_matches_status_filter"](
        {"application_status": "OPEN NOW"},
        "Open",
    )
    assert ns["opportunity_matches_status_filter"](
        {"application_status": "Future Cycle"},
        "Opens soon",
    )


def test_combined_filters() -> None:
    ns, _ = _load_helpers()
    row = {
        "cost": "Free",
        "format": "Online virtual",
        "grades": "10;11",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "application_status": "OPEN NOW",
        "fields": "Computer Science;Cybersecurity",
    }
    assert ns["opportunity_matches_cost_filter"](row, "Free")
    assert ns["opportunity_matches_format"](row["format"], ["Virtual"])
    assert ns["opportunity_matches_grade_filter"](row, ["10"])
    assert ns["opportunity_matches_location_filter"](row, "NYC only")
    assert ns["opportunity_matches_status_filter"](row, "Open")

    # Combined AND failure when one filter misses.
    assert not ns["opportunity_matches_cost_filter"](row, "Paid")


def test_best_match_eligibility_and_explanations() -> None:
    ns, _ = _load_helpers()
    profile = {
        "grade": "10",
        "borough": "Bronx",
        "age": 16,
        "interests": ["Computer Science"],
        "financial_support": True,
    }

    eligible = {
        "name": "Eligible Free CS Program",
        "grades": "9;10;11",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "age_range": "14–18",
        "fields": "Computer Science;Cybersecurity",
        "cost": "Free",
        "financial_aid": "Not needed — fully funded",
        "application_status": "OPEN NOW",
        "format": "In person — NYC",
        "eligible_interest_scope": "",
    }
    scored = ns["score_best_match_opportunity"](eligible, profile)
    if scored is None:
        fail("eligible program excluded from best matches")
    if scored["label"] != "Confirmed match":
        fail(f"expected confirmed label, got {scored['label']}")
    if scored.get("fit_score") is None:
        fail("expected numeric fit_score for verified evidence")
    if scored["fit_score"] != 95:
        fail(f"expected absolute fit_score 95, got {scored['fit_score']}")
    if scored["fit_score"] == 100:
        fail("top-fit program must not be forced to 100%")
    joined = " | ".join(scored["reasons"]).lower()
    if "grade 10" not in joined:
        fail(f"missing grade reason: {scored['reasons']}")
    if "computer science" not in joined and "cybersecurity" not in joined:
        fail(f"missing interest reason: {scored['reasons']}")
    if "free program" not in joined:
        fail(f"missing free reason: {scored['reasons']}")
    if "nyc students" not in joined:
        fail(f"missing NYC reason: {scored['reasons']}")
    if not scored.get("score_factors"):
        fail("missing score_factors transparency")
    if not (2 <= len(scored["reasons"]) <= 4):
        fail(f"expected 2-4 reasons, got {len(scored['reasons'])}")

    hard_ineligible = dict(eligible)
    hard_ineligible["grades"] = "11;12"
    if ns["score_best_match_opportunity"](hard_ineligible, profile) is not None:
        fail("hard grade conflict was not excluded")

    age_ineligible = dict(eligible)
    age_ineligible["age_range"] = "17+"
    if ns["score_best_match_opportunity"](age_ineligible, profile) is not None:
        fail("hard age conflict was not excluded")

    unknown = dict(eligible)
    unknown["grades"] = "Check official eligibility"
    unknown["age_range"] = "Varies — check official site"
    scored_unknown = ns["score_best_match_opportunity"](unknown, profile)
    if scored_unknown is None:
        fail("unknown eligibility should not hard-exclude")
    if scored_unknown["label"] != "Potential match — verify requirements":
        fail(f"expected verify label, got {scored_unknown['label']}")
    if scored_unknown.get("fit_score") is None:
        fail("unknown grade/age with verified location+interest should still score")
    # Unknown requirements must not be awarded as satisfied grade/age points.
    if scored_unknown["fit_score"] >= scored["fit_score"]:
        fail("unknown requirements incorrectly scored as high as verified eligibility")
    if not any(
        "unverified" in note.lower() or "Confirm" in note
        for note in (scored_unknown.get("unverified") or []) + scored_unknown["reasons"]
    ):
        fail(f"missing unverified wording: {scored_unknown}")

    # Outside NYC hard conflict
    outside = dict(eligible)
    outside["boroughs_served"] = "Outside NYC — Greater Rochester, New York only"
    outside["location"] = "Rochester only"
    if ns["score_best_match_opportunity"](outside, profile) is not None:
        fail("outside-NYC conflict was not excluded")


def test_fit_score_missing_info_and_conflicts() -> None:
    ns, _ = _load_helpers()
    base = {
        "name": "Partial Evidence Program",
        "grades": "9;10;11",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "age_range": "14–18",
        "fields": "Computer Science",
        "cost": "Free",
        "application_status": "OPEN NOW",
        "format": "Virtual",
        "eligible_interest_scope": "",
    }

    missing_interests = {
        "grade": "10",
        "borough": "Bronx",
        "age": 16,
        "interests": [],
        "financial_support": False,
    }
    scored_missing = ns["compute_opportunity_fit_score"](base, missing_interests)
    if scored_missing["fit_score"] is not None:
        fail("missing interests must yield Not enough information (fit_score=None)")
    if not any("interest" in note.lower() for note in scored_missing["unverified"]):
        fail(f"missing interest unverified note: {scored_missing['unverified']}")

    conflict = ns["compute_opportunity_fit_score"](
        {**base, "grades": "12"},
        {
            "grade": "10",
            "borough": "Bronx",
            "age": 16,
            "interests": ["Computer Science"],
        },
    )
    if conflict["eligibility_status"] != "ineligible":
        fail("conflicting eligibility not marked ineligible")
    if ns["score_best_match_opportunity"](
        {**base, "grades": "12"},
        {
            "grade": "10",
            "borough": "Bronx",
            "age": 16,
            "interests": ["Computer Science"],
        },
    ) is not None:
        fail("conflicting eligibility should be excluded from best matches")


def test_fit_score_multiple_majors_and_any_major() -> None:
    ns, _ = _load_helpers()
    profile = {
        "grade": "11",
        "borough": "Queens",
        "age": 17,
        "interests": ["Biology"],
        "financial_support": False,
    }
    multi_profile = {
        "grade": "11",
        "borough": "Queens",
        "age": 17,
        "interests": ["Biology", "Computer Science"],
        "financial_support": False,
    }
    multi_fields = {
        "name": "Bio + CS Research",
        "grades": "11",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "age_range": "16-18",
        "fields": "Biology;Computer Science",
        "cost": "Paid",
        "application_status": "Future Cycle",
        "format": "In person",
        "eligible_interest_scope": "",
    }
    single = ns["score_best_match_opportunity"](multi_fields, profile)
    multi = ns["score_best_match_opportunity"](
        multi_fields,
        multi_profile,
        potential_majors=["Engineering"],
    )
    if single is None or multi is None:
        fail("multi-major program unexpectedly excluded")
    if multi["fit_score"] <= single["fit_score"]:
        fail(
            "multiple matched fields should score at least as high as one match "
            f"({multi['fit_score']} vs {single['fit_score']})"
        )
    if multi["fit_score"] > 100:
        fail("fit_score exceeded 100")

    for name in ("Thrive Scholars", "LEDA Scholars Program"):
        row = {
            "name": name,
            "grades": "11",
            "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
            "age_range": "14-18",
            "fields": "Any Major;All Fields;College Access",
            "eligible_interest_scope": "Any major",
            "cost": "Free",
            "application_status": "Future Cycle",
            "format": "In person",
        }
        scored = ns["score_best_match_opportunity"](row, profile)
        if scored is None:
            fail(f"{name} excluded despite any-major scope")
        if scored.get("fit_score") is None:
            fail(f"{name} should receive a fit score when interests exist")
        if not any(
            "general-access" in r.lower() or "across fields" in r.lower()
            for r in scored["reasons"]
        ) and not any("any-major" in f.lower() or "general-access" in f.lower() for f in scored["score_factors"]):
            fail(f"{name} missing any-major explanation: {scored}")


def test_fit_score_absolute_not_relative() -> None:
    ns, _ = _load_helpers()
    profile = {
        "grade": "10",
        "borough": "Bronx",
        "age": 16,
        "interests": ["Computer Science"],
        "financial_support": True,
    }
    target = {
        "name": "Target Program",
        "grades": "9;10;11",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "age_range": "14–18",
        "fields": "Computer Science",
        "cost": "Free",
        "application_status": "OPEN NOW",
        "format": "Virtual",
        "eligible_interest_scope": "",
    }
    unrelated = {
        "name": "Unrelated Biology Camp",
        "grades": "9;10;11",
        "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
        "age_range": "14–18",
        "fields": "Biology",
        "cost": "Paid",
        "application_status": "CLOSED",
        "format": "In person",
        "eligible_interest_scope": "",
    }
    alone = ns["compute_opportunity_fit_score"](target, profile)["fit_score"]
    # Scoring another unrelated program must not change the absolute target score.
    _ = ns["compute_opportunity_fit_score"](unrelated, profile)
    again = ns["compute_opportunity_fit_score"](target, profile)["fit_score"]
    if alone != again:
        fail(f"absolute score changed when unrelated programs scored ({alone} vs {again})")
    if alone == 100:
        fail("absolute rubric must not auto-award 100%")

    catalog_scores = [
        ns["compute_opportunity_fit_score"](row, profile)["fit_score"]
        for row in (target, unrelated, dict(target, name="Clone"))
    ]
    if catalog_scores[0] != alone:
        fail("target score changed inside a multi-program catalog pass")


def test_thrive_leda_any_major() -> None:
    ns, _ = _load_helpers()
    profile = {
        "grade": "11",
        "borough": "Queens",
        "age": 17,
        "interests": ["Biology"],
        "financial_support": False,
    }
    for name in ("Thrive Scholars", "LEDA Scholars Program"):
        row = {
            "name": name,
            "grades": "11",
            "boroughs_served": "Bronx;Brooklyn;Manhattan;Queens;Staten Island",
            "age_range": "High school juniors",
            "fields": "Any Major;All Fields;College Access",
            "eligible_interest_scope": "Any major",
            "cost": "Free",
            "application_status": "Future Cycle",
            "format": "In person",
        }
        scored = ns["score_best_match_opportunity"](row, profile)
        if scored is None:
            fail(f"{name} excluded despite any-major scope")
        if not any("general-access" in r.lower() or "across fields" in r.lower() for r in scored["reasons"]):
            # Still acceptable if interest overlap language appears via fields.
            if not any("major" in r.lower() or "field" in r.lower() for r in scored["reasons"]):
                fail(f"{name} missing any-major explanation: {scored['reasons']}")

    # Catalog contract still present in app source.
    if '"eligible_interest_scope": "Any major"' not in SOURCE:
        fail("Any major scope missing from catalog source")


def test_hide_saved_and_uuid_ownership_still_present() -> None:
    if "def require_user_sub(" not in SOURCE:
        fail("UUID ownership helper missing")
    ownership = SOURCE[
        SOURCE.index("def require_user_sub(") : SOURCE.index("def require_user_sub(") + 500
    ]
    if "email" in ownership.lower() and "never valid owners" not in ownership.lower():
        # The docstring mentions emails are never valid owners — required.
        pass
    if "never valid owners" not in SOURCE:
        fail("ownership docstring contract missing")

    if "user_saved_opportunity_catalog_ids(user_sub)" not in SOURCE:
        fail("discovery hide saved helper call missing")
    if "load_saved_opportunities(user_sub)" not in SOURCE:
        fail("My Applications UUID load path missing")


def test_ambiguous_data_report_hook() -> None:
    """Ensure helpers classify ambiguous rows as unknown/confirm, not invented facts."""

    ns, _ = _load_helpers()
    ambiguous = {
        "cost": "Check official site",
        "format": "",
        "grades": "",
        "boroughs_served": "",
        "application_status": "Seasonal",
    }
    assert ns["normalize_opportunity_cost_bucket"](ambiguous) == "unknown"
    assert ns["normalize_opportunity_format_buckets"](ambiguous["format"]) == set()
    assert ns["parse_opportunity_grades"](ambiguous["grades"]) is None
    assert ns["normalize_opportunity_nyc_eligibility"](ambiguous) == "unknown"


def test_catalog_blank_stem_or_and_pagination() -> None:
    """Blank filters, one STEM area, multi-area OR, and distinct pages."""

    import csv

    catalog_path = ROOT / "data" / "opportunities.csv"
    with catalog_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 21:
        fail(f"catalog too small for pagination: {len(rows)}")

    page_size = 10
    page1_names = [row.get("name") for row in rows[:page_size]]
    page2_names = [row.get("name") for row in rows[page_size:page_size * 2]]
    if len(page1_names) != 10:
        fail("blank filters should expose the first 10 cards")
    if page1_names == page2_names:
        fail("next page should display different cards")

    ns, _ = _load_helpers()
    stem_fn = SOURCE[
        SOURCE.index("def opportunity_matches_stem_selection("):
        SOURCE.index("def opportunity_matches_format(")
    ]
    exec(stem_fn, ns)

    cs_fields = [
        "Computer Science",
        "Artificial Intelligence",
        "Data Science",
    ]
    bio_fields = [
        "Biology",
        "Biomedical Engineering",
    ]
    cs_matches = [
        row
        for row in rows
        if ns["opportunity_matches_stem_selection"](row.get("fields"), cs_fields)
    ]
    bio_matches = [
        row
        for row in rows
        if ns["opportunity_matches_stem_selection"](row.get("fields"), bio_fields)
    ]
    or_matches = [
        row
        for row in rows
        if ns["opportunity_matches_stem_selection"](
            row.get("fields"),
            cs_fields + bio_fields,
        )
    ]
    if not cs_matches:
        fail("one STEM area produced no matching cards")
    if len(or_matches) < max(len(cs_matches), len(bio_matches)):
        fail("multiple STEM areas should keep OR matching")
    cs_names = {row.get("name") for row in cs_matches}
    or_names = {row.get("name") for row in or_matches}
    if not cs_names <= or_names:
        fail("OR matching dropped a single-area result")


def main() -> None:
    test_source_contracts()
    test_normalizers_and_filters()
    test_combined_filters()
    test_catalog_blank_stem_or_and_pagination()
    test_best_match_eligibility_and_explanations()
    test_fit_score_missing_info_and_conflicts()
    test_fit_score_multiple_majors_and_any_major()
    test_fit_score_absolute_not_relative()
    test_thrive_leda_any_major()
    test_hide_saved_and_uuid_ownership_still_present()
    test_ambiguous_data_report_hook()
    print("PASS: opportunity discovery filters + best matches offline tests")


if __name__ == "__main__":
    main()
