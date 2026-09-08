"""Offline source contracts for compact multi-major recommendation results."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = (ROOT / "app.py").read_text(encoding="utf-8")


def require(fragment, message):
    if fragment not in SOURCE:
        raise AssertionError(message)


require("selected = strong[:3] if strong else ranked[:3]", "results are not capped at three")
require("for match_field, _match_score in top_matches[:3]:", "careers do not cover each displayed match")
require("if len(match_careers) >= 2:", "career samples are not capped per major")
require("seen_careers = set()", "career cards are not deduplicated")

if "strong[:5]" in SOURCE or "top_matches[3:5]" in SOURCE:
    raise AssertionError("legacy five-result rendering is still present")

print("PASS: potential majors capped at 3 with compact multi-major careers")
