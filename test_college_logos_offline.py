"""Offline audit for college catalog logo coverage.

Run: python3 test_college_logos_offline.py
Does not touch secrets, network, or live Auth.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.py"
CATALOG = ROOT / "data" / "college_catalog.json"
LOGO_DIR = ROOT / "assets" / "college_logos"
SOURCE = APP.read_text(encoding="utf-8")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def college_logo_slug(college_name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", str(college_name or "").strip().lower())
    return slug.strip("-")


def load_catalog_names() -> list[str]:
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    colleges = payload.get("colleges") or []
    names = []
    for row in colleges:
        if not isinstance(row, dict):
            continue
        name = str(row.get("name") or "").strip()
        if name:
            names.append(name)
    if len(names) < 90:
        fail(f"expected ~96 catalog colleges, found {len(names)}")
    return names


def extract_logo_map() -> dict[str, str]:
    match = re.search(
        r"COLLEGE_LOGO_FILES\s*=\s*\{(.*?)\n\}",
        SOURCE,
        flags=re.S,
    )
    if not match:
        fail("COLLEGE_LOGO_FILES dict not found in app.py")
    body = match.group(1)
    pairs = re.findall(r'"([^"]+)"\s*:\s*"([^"]+)"', body)
    if not pairs:
        fail("COLLEGE_LOGO_FILES appears empty")
    return dict(pairs)


def valid_image(path: Path) -> bool:
    try:
        raw = path.read_bytes()
    except OSError:
        return False
    if len(raw) < 64:
        return False
    suffix = path.suffix.lower()
    if suffix == ".svg":
        text = raw[:5000].decode("utf-8", errors="ignore").lower()
        return "<svg" in text and "<html" not in text
    if suffix == ".png":
        return raw.startswith(b"\x89PNG")
    if suffix in {".jpg", ".jpeg"}:
        return raw.startswith(b"\xff\xd8")
    if suffix == ".webp":
        return raw[:4] == b"RIFF" and b"WEBP" in raw[:16]
    return False


def resolve_local_logo(name: str, logo_map: dict[str, str]) -> Path | None:
    filename = logo_map.get(name)
    if filename:
        mapped = LOGO_DIR / filename
        if mapped.is_file() and valid_image(mapped):
            return mapped

    slug = college_logo_slug(name)
    if not slug:
        return None
    for ext in (".svg", ".png", ".webp", ".jpg", ".jpeg"):
        candidate = LOGO_DIR / f"{slug}{ext}"
        if candidate.is_file() and valid_image(candidate):
            return candidate
    return None


def test_source_contracts() -> None:
    required = [
        "COLLEGE_LOGO_FILES",
        "COLLEGE_LOGO_ALIASES",
        "SUNY Polytechnic Institute",
        "suny-polytechnic-institute.png",
        "def resolve_college_logo_path(",
        "def college_logo_mark_html(",
        "object-fit: contain",
        "sp-fav-college-initials",
        "aria-label=",
    ]
    for item in required:
        if item not in SOURCE:
            fail(f"missing required symbol/text: {item}")

    # Logo rendering must keep contain + centered padding.
    if "object-position: center" not in SOURCE:
        fail("logo CSS missing object-position: center")
    if ".sp-fav-college-mark" not in SOURCE:
        fail("missing .sp-fav-college-mark styles")


def test_catalog_logo_or_initials_coverage() -> None:
    names = load_catalog_names()
    logo_map = extract_logo_map()

    if "SUNY Polytechnic Institute" not in logo_map:
        fail("SUNY Polytechnic Institute missing from COLLEGE_LOGO_FILES")
    if logo_map["SUNY Polytechnic Institute"] != "suny-polytechnic-institute.png":
        fail("SUNY Polytechnic Institute alias filename incorrect")

    with_logo = []
    initials_fallback = []
    broken = []

    for name in names:
        path = resolve_local_logo(name, logo_map)
        if path is None:
            initials_fallback.append(name)
            continue
        if not valid_image(path):
            broken.append((name, path.name))
            continue
        with_logo.append(name)

    if broken:
        fail(f"broken/invalid logo files: {broken[:8]}")

    # Every catalog college must resolve to either a valid local image or
    # intentional initials fallback (no unresolved/corrupt middle state).
    covered = len(with_logo) + len(initials_fallback)
    if covered != len(names):
        fail(f"coverage mismatch: {covered} != {len(names)}")

    # Mapped filenames must exist when listed.
    for name, filename in logo_map.items():
        path = LOGO_DIR / filename
        if not path.is_file():
            fail(f"mapped logo missing on disk for {name}: {filename}")
        if not valid_image(path):
            fail(f"mapped logo invalid for {name}: {filename}")

    print(
        f"PASS: college logos offline audit "
        f"(catalog={len(names)}, logos={len(with_logo)}, "
        f"initials_fallback={len(initials_fallback)})"
    )
    if initials_fallback:
        print("Initials fallback colleges:")
        for name in initials_fallback:
            print(f" - {name}")


def main() -> None:
    test_source_contracts()
    test_catalog_logo_or_initials_coverage()


if __name__ == "__main__":
    main()
