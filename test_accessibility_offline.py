"""Offline accessibility contracts and WCAG contrast checks."""

import ast
from pathlib import Path


SOURCE = (Path(__file__).resolve().parent / "app.py").read_text(encoding="utf-8")


def rgb(hex_color):
    value = hex_color.lstrip("#")
    return tuple(int(value[index:index + 2], 16) / 255 for index in (0, 2, 4))


def luminance(hex_color):
    channels = []
    for value in rgb(hex_color):
        channels.append(value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(first, second):
    light, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


for foreground, background in (
    ("#083B5C", "#FFFFFF"),
    ("#041E33", "#38BDF8"),
    ("#F8FBFF", "#041E33"),
    ("#BFD3DF", "#0A4563"),
    ("#526879", "#FFFFFF"),
):
    assert contrast(foreground, background) >= 4.5, (foreground, background)

required = (
    'class="sp-skip-link"',
    'href="#sp-main-content"',
    'button:focus-visible',
    'outline: 3px solid #F5B82E',
    'min-height: 44px',
    'min-width: 44px',
    '@media (max-width: 720px)',
    '@media (prefers-reduced-motion: reduce)',
    'role="status" aria-live="polite"',
    'sidebar.setAttribute("aria-label", "Primary navigation")',
    'button.setAttribute("aria-current", "page")',
)
for fragment in required:
    assert fragment in SOURCE, fragment

tree = ast.parse(SOURCE)
for node in ast.walk(tree):
    if not isinstance(node, ast.Call):
        continue
    func = node.func
    if not (
        isinstance(func, ast.Attribute)
        and isinstance(func.value, ast.Name)
        and func.value.id == "st"
        and func.attr in {"button", "link_button", "download_button", "page_link"}
    ):
        continue
    label = node.args[0] if node.args else next(
        (kw.value for kw in node.keywords if kw.arg == "label"),
        None,
    )
    assert label is not None, f"unlabeled st.{func.attr} at line {node.lineno}"
    if isinstance(label, ast.Constant):
        assert str(label.value or "").strip(), f"empty button label at line {node.lineno}"

print("PASS: contrast, buttons, keyboard, screen-reader, and phone contracts")
