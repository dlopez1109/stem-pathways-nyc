"""Offline audit for universal Thrive Scholars and LEDA catalog entries."""

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = (ROOT / "app.py").read_text(encoding="utf-8")


def extract_extras():
    marker = SOURCE.index("extra_opportunities = [")
    start = SOURCE.index("[", marker)
    depth = 0
    for index in range(start, len(SOURCE)):
        if SOURCE[index] == "[":
            depth += 1
        elif SOURCE[index] == "]":
            depth -= 1
            if depth == 0:
                return ast.literal_eval(SOURCE[start:index + 1])
    raise AssertionError("extra_opportunities list did not close")


rows = {row["name"]: row for row in extract_extras()}
for name in ("Thrive Scholars", "LEDA Scholars Program"):
    assert name in rows, f"missing {name}"
    row = rows[name]
    assert row.get("eligible_interest_scope") == "Any major"
    fields = {part.strip() for part in row.get("fields", "").split(";")}
    assert {"Any Major", "All Fields"}.issubset(fields)
    assert row.get("grades") == "11"
    assert str(row.get("url", "")).startswith("https://")
    assert row.get("cost") and row.get("eligibility_summary")

scope_block = SOURCE[
    SOURCE.index("def opportunity_scope_matches_interests"):
    SOURCE.index("def stem_fields_for_opportunity_area")
]
any_major_position = scope_block.index('if scope in {')
empty_interests_position = scope_block.index('if not expanded_interests:')
assert any_major_position < empty_interests_position, (
    "Any-major programs must match even when no field interests are selected"
)

print("PASS: Thrive Scholars and LEDA are available to every field and major")
