"""ASGI entrypoint for STEM Pathways NYC with secure auth cookie routes.

Render start command:
  streamlit run asgi_app.py --server.port=$PORT --server.address=0.0.0.0

Do not run `streamlit run app.py` in production if you need HttpOnly session
persistence — cookies are set only through the /auth/* HTTP routes below.

The cookie value is an opaque session ID only. Tokens never appear in cookies,
query parameters, HTML, or localStorage.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlencode

import streamlit as st
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.routing import Route

import auth_persist

SCRIPT_PATH = str(Path(__file__).resolve().with_name("app.py"))

PAGE_PATHS = {
    "dashboard": "/dashboard",
    "pathway": "/pathway",
    "opportunities": "/opportunities",
    "deadlines": "/deadlines",
    "colleges": "/colleges",
    "projects": "/projects",
    "resources": "/resources",
    "applications": "/applications",
    "favorite-colleges": "/favorite-colleges",
    "gpa-calculator": "/gpa-calculator",
    "feedback": "/feedback",
    "profile": "/profile",
    "admin": "/admin",
}


def _safe_return_path(request: Request, default: str = "/") -> str:
    candidate = str(request.query_params.get("return_to") or "").strip()
    return candidate if candidate in PAGE_PATHS.values() else default


async def stable_page(request: Request):
    """Boot the single Streamlit app with the requested friendly page selected."""

    slug = str(request.url.path or "").strip("/").lower()
    if slug not in PAGE_PATHS:
        return RedirectResponse(url="/", status_code=303)
    query = urlencode({"page": slug, "sp_route": "1"})
    return RedirectResponse(url=f"/?{query}", status_code=303)


def _request_host(request: Request) -> str:
    host = request.headers.get("host") or request.url.hostname or ""
    return str(host)


async def persist_session(request: Request):
    """Exchange a one-time ticket for an HttpOnly Secure opaque session cookie."""

    ticket = str(request.query_params.get("ticket") or "").strip()
    host = _request_host(request)
    payload = auth_persist.consume_cookie_ticket(ticket)

    if payload is None:
        response = RedirectResponse(url=_safe_return_path(request), status_code=303)
        auth_persist.apply_clear_session_cookie(response, host=host)
        return response

    purpose = str(payload.get("purpose") or "").strip().lower()
    session_id = str(payload.get("session_id") or "").strip()

    response = RedirectResponse(url=_safe_return_path(request), status_code=303)
    try:
        if purpose == "clear":
            auth_persist.apply_clear_session_cookie(response, host=host)
        elif purpose == "set" and auth_persist.session_id_is_valid(session_id):
            # Confirm the session still exists and is active before setting cookie.
            loaded = auth_persist.load_server_session(session_id)
            if loaded is None:
                auth_persist.apply_clear_session_cookie(response, host=host)
            else:
                auth_persist.apply_set_session_cookie(
                    response,
                    session_id,
                    host=host,
                )
        else:
            auth_persist.apply_clear_session_cookie(response, host=host)
    except Exception:
        auth_persist.apply_clear_session_cookie(response, host=host)
    return response


async def clear_session(request: Request):
    """Delete the STEM Pathways auth cookie and return home."""

    host = _request_host(request)
    response = RedirectResponse(url="/", status_code=303)
    auth_persist.apply_clear_session_cookie(response, host=host)
    return response


app = st.App(
    SCRIPT_PATH,
    routes=[
        Route("/auth/persist-session", persist_session, methods=["GET"]),
        Route("/auth/clear-session", clear_session, methods=["GET"]),
        *[
            Route(path, stable_page, methods=["GET"], name=f"page-{slug}")
            for slug, path in PAGE_PATHS.items()
        ],
    ],
)

if __name__ == "__main__":
    app.run()
