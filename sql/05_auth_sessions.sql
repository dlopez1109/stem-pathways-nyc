-- auth_sessions + auth_cookie_tickets
-- Opaque browser cookie (sp_sid) points at a server-side session row.
-- Access/refresh tokens are stored encrypted at rest and never placed in cookies,
-- query params, localStorage, or HTML.
-- Used only by the Streamlit/ASGI server via the service_role key.
-- Never expose these tables to anon/authenticated clients.

create table if not exists public.auth_sessions (
  session_id text primary key,
  user_id uuid not null,
  provider text not null,
  access_token_enc text not null,
  refresh_token_enc text not null,
  email text null,
  created_at timestamptz not null default timezone('utc', now()),
  expires_at timestamptz not null,
  last_seen_at timestamptz not null default timezone('utc', now()),
  idle_expires_at timestamptz not null,
  revoked_at timestamptz null,
  rotated_from text null,
  constraint auth_sessions_session_id_len
    check (char_length(session_id) between 20 and 128),
  constraint auth_sessions_provider_ok
    check (provider in ('email', 'google')),
  constraint auth_sessions_expires_after_created
    check (expires_at > created_at),
  constraint auth_sessions_idle_after_created
    check (idle_expires_at > created_at)
);

create index if not exists auth_sessions_user_id_idx
  on public.auth_sessions (user_id);

create index if not exists auth_sessions_expires_at_idx
  on public.auth_sessions (expires_at);

create index if not exists auth_sessions_revoked_at_idx
  on public.auth_sessions (revoked_at);

create table if not exists public.auth_cookie_tickets (
  ticket_id text primary key,
  session_id text not null,
  purpose text not null,
  created_at timestamptz not null default timezone('utc', now()),
  expires_at timestamptz not null,
  consumed_at timestamptz null,
  constraint auth_cookie_tickets_ticket_id_len
    check (char_length(ticket_id) between 20 and 128),
  constraint auth_cookie_tickets_purpose_ok
    check (purpose in ('set', 'clear')),
  constraint auth_cookie_tickets_expires_after_created
    check (expires_at > created_at)
);

create index if not exists auth_cookie_tickets_expires_at_idx
  on public.auth_cookie_tickets (expires_at);

create index if not exists auth_cookie_tickets_consumed_at_idx
  on public.auth_cookie_tickets (consumed_at);

alter table public.auth_sessions enable row level security;
alter table public.auth_cookie_tickets enable row level security;

revoke all on table public.auth_sessions from anon, authenticated;
revoke all on table public.auth_cookie_tickets from anon, authenticated;

grant select, insert, update, delete on table public.auth_sessions to service_role;
grant select, insert, update, delete on table public.auth_cookie_tickets to service_role;
