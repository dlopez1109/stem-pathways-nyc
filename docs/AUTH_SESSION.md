# Auth session persistence

## Problem
Refreshing the browser cleared login because Supabase tokens lived only in
Streamlit `session_state` (process memory for that websocket).

## Design
- Cookie `sp_sid`: opaque random session ID, `Secure` + `HttpOnly` + `SameSite=Lax`
- Table `auth_sessions`: encrypted access/refresh tokens (service_role only)
- Table `auth_cookie_tickets`: one-time tickets so ASGI routes can set cookies
- Absolute lifetime: 30 days
- Idle timeout: 7 days (sliding on activity)
- Session ID rotates on login and access-token refresh
- Sign out revokes the server row and clears the cookie via `/auth/clear-session`
- Ownership remains Supabase Auth `user.id` UUID (no email linking)

## Required SQL
Run in Supabase SQL editor:
- `sql/04_oauth_pkce_tickets.sql` (existing Google PKCE tickets)
- `sql/05_auth_sessions.sql` (this feature)

## Environment / secrets
Render environment (recommended):
- `SP_AUTH_PERSIST_SECRET` — long random secret for token encryption
- Existing Supabase URL + service_role remain in Streamlit secrets

Or in `.streamlit/secrets.toml`:
```toml
[auth]
persist_secret = "..."   # or cookie_secret fallback
```

## Render start command
HttpOnly cookies require the ASGI wrapper:

```bash
streamlit run asgi_app.py --server.port=$PORT --server.address=0.0.0.0
```

Do **not** use `streamlit run app.py` in production if refresh persistence is required.

## Local verification
```bash
python3 -m py_compile app.py auth_persist.py asgi_app.py
python3 test_auth_persist_offline.py
python3 test_oauth_ownership_offline.py
```

## Stable page URLs (`/dashboard`, `/opportunities`, `/profile`)
Not implemented in this change. Streamlit multipage/query routing can coexist with
auth cookies, but path-based routes must not bypass `asgi_app.py` or drop the
`sp_sid` cookie. Prefer a follow-up that keeps a single `st.App` entrypoint and
maps paths → `st.session_state.current_page` without a second process.
