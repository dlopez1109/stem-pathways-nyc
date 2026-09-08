"""Offline contracts for stable, authenticated, browser-history-aware page URLs."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent
APP = (ROOT / "app.py").read_text(encoding="utf-8")
ASGI = (ROOT / "asgi_app.py").read_text(encoding="utf-8")

expected = {
    "Dashboard": "/dashboard",
    "Opportunities": "/opportunities",
    "College Suggestions": "/colleges",
    "My Applications": "/applications",
}
for page, path in expected.items():
    assert f'"{page}": "{path}"' in APP
    assert f'"{path.lstrip(chr(47))}": "{path}"' in ASGI

assert "async def stable_page" in ASGI
assert '"sp_route": "1"' in ASGI
assert "Route(path, stable_page" in ASGI
assert "return_to" in ASGI
assert "candidate in PAGE_PATHS.values()" in ASGI

assert "window.history[method]" in APP
assert 'window.addEventListener("popstate"' in APP
assert "window.location.reload()" in APP
assert "SP_ROUTE_CONSUMED_KEY" in APP
assert 'st.session_state[SP_ROUTE_HISTORY_MODE_KEY] = "push"' in APP
assert "sync_browser_page_path(page)" in APP

print("PASS: stable page paths, cookie return, and browser history are wired")
