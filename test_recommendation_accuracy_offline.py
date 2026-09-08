"""Offline contracts for separated finance scoring and honest alignment scores."""

from pathlib import Path


SOURCE = (Path(__file__).resolve().parent / "app.py").read_text(encoding="utf-8")


required = {
    '"Finance & Economics"': "missing separate Finance slider",
    '"Business & Entrepreneurship"': "business slider was not separated",
    '"finance": int(rating_finance)': "finance rating is absent from scoring",
    '"finance": "Finance & Economics"': "finance category label is missing",
    '"finance": "Finance"': "Finance is not the category anchor",
    '<div class="sp-stem-dir-score-label">Alignment Score</div>': (
        "result still labels the value as a generic match score"
    ),
    'percentage = round(max(0.0, min(100.0, float(score))))': (
        "displayed score is not the actual bounded alignment value"
    ),
}
for fragment, message in required.items():
    assert fragment in SOURCE, message

scoring_start = SOURCE.index("interest_major_map = {")
scoring_end = SOURCE.index("category_labels = {", scoring_start)
interest_map_source = SOURCE[scoring_start:scoring_end]
business_start = interest_map_source.index('"business": [')
finance_start = interest_map_source.index('"finance": [', business_start)
business_block = interest_map_source[business_start:finance_start]
assert '"Finance"' not in business_block
assert '"Economics"' not in business_block

assert "(score / max_score_value) * 100" not in SOURCE

print("PASS: Finance is separate and alignment scores are not forced to 100%")
