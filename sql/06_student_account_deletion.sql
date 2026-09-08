-- Atomic student account deletion for STEM Pathways NYC.
-- Run once in the Supabase SQL editor before enabling the UI in production.
-- The app invokes this only with its server-side service_role client.

begin;

create or replace function public.delete_student_account(target_user_id uuid)
returns boolean
language plpgsql
security definer
set search_path = ''
as $$
declare
  owner_keys text[];
begin
  if target_user_id is null then
    raise exception 'target_user_id is required';
  end if;

  -- The canonical Auth UUID plus legacy owner keys that an administrator has
  -- explicitly reviewed and approved for this same account.
  select array_append(
    coalesce(array_agg(google_user_sub), array[]::text[]),
    target_user_id::text
  )
  into owner_keys
  from public.account_identity_links
  where auth_user_id = target_user_id
    and status = 'approved';

  delete from public.saved_opportunities where user_sub = any(owner_keys);
  delete from public.favorite_colleges where user_sub = any(owner_keys);
  delete from public.user_feedback where user_sub = any(owner_keys);
  delete from public.student_profiles where user_sub = any(owner_keys);
  delete from public.account_identity_links
    where auth_user_id = target_user_id
       or google_user_sub = any(owner_keys);

  -- Revoke/delete every durable browser session before removing Auth.
  delete from public.auth_cookie_tickets
    where session_id in (
      select session_id from public.auth_sessions where user_id = target_user_id
    );
  delete from public.auth_sessions where user_id = target_user_id;

  delete from auth.users where id = target_user_id;
  if not found then
    raise exception 'Auth account not found';
  end if;

  return true;
end;
$$;

revoke all on function public.delete_student_account(uuid)
  from public, anon, authenticated;
grant execute on function public.delete_student_account(uuid)
  to service_role;

commit;
