"""Source-level guards for the opportunity/sidebar visual regression."""

from pathlib import Path


SOURCE = Path(__file__).with_name("app.py").read_text(encoding="utf-8")


def main():
    accessibility = SOURCE[SOURCE.index('<style id="sp-accessibility-v1">'):]
    broken = (
        'html body .stApp [data-testid="stSidebar"] button,\n'
        'html body .stApp [data-testid="stSidebar"] button * {'
    )
    assert broken not in accessibility, "nested sidebar nodes still receive 44px height"
    assert "OPPORTUNITY VISUAL REGRESSION GUARD" in SOURCE
    assert '[class*="st-key-best_match_card_"]' in SOURCE
    assert "grid-template-columns: repeat(auto-fit" in SOURCE
    assert "background-color: #FFFFFF !important" in accessibility
    assert ".sp-rec-heading h3" in accessibility
    assert ".sp-rec-desc" in accessibility
    print("PASS: opportunity layout, card contrast, and sidebar sizing guards")


if __name__ == "__main__":
    main()
