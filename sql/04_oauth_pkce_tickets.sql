-- oauth_pkce_tickets
-- Short-lived, single-use PKCE code_verifier tickets for Google OAuth.
-- Used only by the Streamlit server via the service_role key.
-- Never expose this table to anon/authenticated clients.

create table if not exists public.oauth_pkce_tickets (
  ticket_id text primary key,
  code_verifier text not null,
  created_at timestamptz not null default timezone('utc', now()),
  expires_at timestamptz not null,
  consumed_at timestamptz null,
  constraint oauth_pkce_tickets_ticket_id_len
    check (char_length(ticket_id) between 20 and 128),
  constraint oauth_pkce_tickets_expires_after_created
    check (expires_at > created_at)
);

create index if not exists oauth_pkce_tickets_expires_at_idx
  on public.oauth_pkce_tickets (expires_at);

create index if not exists oauth_pkce_tickets_consumed_at_idx
  on public.oauth_pkce_tickets (consumed_at);

alter table public.oauth_pkce_tickets enable row level security;

-- Revoke direct access from public roles. Service role bypasses RLS.
revoke all on table public.oauth_pkce_tickets from anon, authenticated;
grant select, insert, update, delete on table public.oauth_pkce_tickets to service_role;

-- Optional: no policies for anon/authenticated (deny by default with RLS on).
-- Do NOT create INSERT/SELECT policies for anon or authenticated.

-- Optional cleanup helper (run manually or via scheduled job):
-- delete from public.oauth_pkce_tickets
-- where expires_at < timezone('utc', now()) - interval '1 day';
