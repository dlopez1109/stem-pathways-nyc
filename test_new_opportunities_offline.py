"""Offline audit for the nine verified opportunity additions (Sep 2026).

Run: python3 test_new_opportunities_offline.py
Does not touch secrets, network, Auth, SQL, or live Streamlit.
"""

from __future__ import annotations

import ast
import csv
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.py"
CSV_PATH = ROOT / "data" / "opportunities.csv"
TODAY = date(2026, 9, 8)

REQUESTED = [
    "NYU Tandon Computer Science for Cyber Security (CS4CS)",
    "Stanford AIMI Summer Research Internship",
    "Stanford AIMI Summer Health AI Bootcamp",
    "Johns Hopkins Explore Engineering Innovation",
    "Johns Hopkins Engineering Innovation Research Program",
    "CDC Museum Public Health Academy Online Summer Course",
    "Economics for Leaders",
    "Yale Young Global Scholars — Innovations in Science & Technology",
    "Columbia Climate School Pre-College Programs",
]

REQUIRED_FIELDS = [
    "name",
    "organization",
    "description",
    "opportunity_type",
    "fields",
    "grades",
    "age_range",
    "boroughs_served",
    "cost",
    "financial_aid",
    "application_status",
    "deadline",
    "url",
    "last_verified",
]

OFFICIAL_HOST_HINTS = {
    "NYU Tandon Computer Science for Cyber Security (CS4CS)": (
        "engineering.nyu.edu",
        "k12stem.engineering.nyu.edu",
    ),
    "Stanford AIMI Summer Research Internship": ("aimi.stanford.edu",),
    "Stanford AIMI Summer Health AI Bootcamp": ("aimi.stanford.edu",),
    "Johns Hopkins Explore Engineering Innovation": ("ei.jhu.edu",),
    "Johns Hopkins Engineering Innovation Research Program": ("ei.jhu.edu",),
    "CDC Museum Public Health Academy Online Summer Course": ("cdc.gov",),
    "Economics for Leaders": ("fte.org",),
    "Yale Young Global Scholars — Innovations in Science & Technology": (
        "globalscholars.yale.edu",
    ),
    "Columbia Climate School Pre-College Programs": ("climate.columbia.edu",),
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def normalize_name(name: str) -> str:
    text = str(name or "").casefold()
    text = text.replace("—", "-").replace("–", "-")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_extra_opportunities(source: str) -> list[dict]:
    marker = "extra_opportunities"
    start = source.find(marker)
    if start < 0:
        fail("extra_opportunities not found in app.py")
    bracket = source.find("[", start)
    if bracket < 0:
        fail("extra_opportunities list start not found")

    depth = 0
    end = None
    for idx in range(bracket, len(source)):
        ch = source[idx]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                end = idx + 1
                break
    if end is None:
        fail("could not close extra_opportunities list")

    try:
        data = ast.literal_eval(source[bracket:end])
    except Exception as exc:  # noqa: BLE001
        fail(f"ast.literal_eval(extra_opportunities) failed: {exc}")
    if not isinstance(data, list):
        fail("extra_opportunities is not a list")
    return data


def load_csv_names() -> list[str]:
    if not CSV_PATH.exists():
        fail(f"missing {CSV_PATH}")
    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [row.get("name", "") for row in reader if row.get("name")]


def first_month_day_year(text: str):
    match = re.search(
        r"(January|February|March|April|May|June|July|August|September|"
        r"October|November|December)\s+(\d{1,2}),\s+(\d{4})",
        text,
        flags=re.I,
    )
    if not match:
        return None
    months = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12,
    }
    month = months[match.group(1).lower()]
    return date(int(match.group(3)), month, int(match.group(2)))


def main() -> None:
    source = APP.read_text(encoding="utf-8")
    extras = extract_extra_opportunities(source)
    csv_names = load_csv_names()

    by_name = {row.get("name"): row for row in extras if isinstance(row, dict)}
    evaluated = []
    added = []

    for name in REQUESTED:
        evaluated.append(name)
        if name not in by_name:
            fail(f"requested program missing from extra_opportunities: {name}")
        added.append(name)

    if len(evaluated) != 9:
        fail(f"expected 9 evaluated names, got {len(evaluated)}")

    # Canonical source only: must not also appear in CSV.
    csv_norm = {normalize_name(n) for n in csv_names}
    for name in added:
        if normalize_name(name) in csv_norm:
            fail(f"duplicate across CSV and extra_opportunities: {name}")

    # Official URL + required fields for added rows.
    for name in added:
        row = by_name[name]
        for field in REQUIRED_FIELDS:
            value = row.get(field)
            if value is None or str(value).strip() == "":
                fail(f"{name}: missing required field {field}")
        url = str(row["url"]).strip()
        if not url.startswith("https://"):
            fail(f"{name}: url must be https official link, got {url!r}")
        hints = OFFICIAL_HOST_HINTS[name]
        if not any(hint in url for hint in hints):
            fail(f"{name}: url host not recognized as official ({url})")

    # No normalized duplicate names across catalog.
    all_names = list(csv_names) + [
        row.get("name", "") for row in extras if isinstance(row, dict)
    ]
    seen = {}
    for name in all_names:
        key = normalize_name(name)
        if not key:
            continue
        if key in seen and seen[key] != name:
            fail(f"normalized duplicate names: {seen[key]!r} vs {name!r}")
        if key in seen and seen[key] == name and name in added:
            # Same exact name twice in extras is also a failure.
            counts = sum(1 for n in all_names if n == name)
            if counts > 1:
                fail(f"exact duplicate name appears {counts} times: {name}")
        seen[key] = name

    # Expired dates must not be presented as upcoming for closed programs.
    for name in added:
        row = by_name[name]
        status = str(row.get("application_status", "")).lower()
        deadline = str(row.get("deadline", ""))
        deadline_l = deadline.lower()
        parsed = first_month_day_year(deadline)

        if "closed" in status or "closed" in deadline_l:
            if parsed is not None and parsed >= TODAY and "closed" not in deadline_l:
                fail(
                    f"{name}: closed program has future date without closed wording: "
                    f"{deadline}"
                )
            # Calendar helper treats strings containing "closed" as non-events.
            if "closed" not in deadline_l and "not yet announced" not in deadline_l:
                # Allow future-cycle language without a parseable past date.
                if parsed is not None and parsed < TODAY:
                    fail(
                        f"{name}: past deadline date without 'closed' marker: {deadline}"
                    )
            continue

        # Open/future programs: if a concrete deadline date is present, it must
        # not be in the past relative to the audit date.
        if parsed is not None and parsed < TODAY:
            fail(f"{name}: expired date shown as current/upcoming: {deadline}")

    # Field tags sanity for filter relevance.
    expected_tokens = {
        "NYU Tandon Computer Science for Cyber Security (CS4CS)": (
            "Computer Science",
            "Cybersecurity",
        ),
        "Stanford AIMI Summer Research Internship": (
            "Artificial Intelligence",
            "Healthcare",
            "Research",
        ),
        "Stanford AIMI Summer Health AI Bootcamp": (
            "Artificial Intelligence",
            "Healthcare",
        ),
        "Johns Hopkins Explore Engineering Innovation": ("Engineering",),
        "Johns Hopkins Engineering Innovation Research Program": (
            "Engineering",
            "Research",
        ),
        "CDC Museum Public Health Academy Online Summer Course": ("Public Health",),
        "Economics for Leaders": ("Economics", "Finance"),
        "Yale Young Global Scholars — Innovations in Science & Technology": (
            "Engineering",
            "Computer Science",
        ),
        "Columbia Climate School Pre-College Programs": (
            "Environmental Science",
            "Climate Science",
        ),
    }
    for name, tokens in expected_tokens.items():
        fields = str(by_name[name].get("fields", ""))
        for token in tokens:
            if token not in fields:
                fail(f"{name}: expected field tag {token!r} in {fields!r}")

    print("PASS: evaluated all 9 requested programs")
    print("PASS: all added entries present in extra_opportunities with official URLs")
    print("PASS: no CSV duplicates; no normalized catalog duplicates")
    print("PASS: expired deadlines not presented as upcoming")
    print("PASS: required fields populated")
    print(f"Added programs ({len(added)}):")
    for name in added:
        row = by_name[name]
        print(f"  - {name} | {row.get('application_status')} | {row.get('url')}")


if __name__ == "__main__":
    main()
