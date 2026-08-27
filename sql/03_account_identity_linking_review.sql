-- ============================================================
-- REVIEW ONLY — DO NOT AUTO-RUN IN PRODUCTION
-- Proposed verified-email account linking / migration strategy
-- STEM Pathways NYC
--
-- Goals:
--   1. Preserve every existing Google user_sub and related rows
--   2. Never rewrite student rows by email alone
--   3. Allow a future, explicit, verified-email link between:
--        - an existing Google identity (st.user.sub), and
--        - a confirmed Supabase Auth email user (auth.users.id)
--   4. Prevent cross-user access from unverified or ambiguous matches
--
-- App behavior today (no SQL required for launch):
--   - Google users keep their current user_sub forever unless an
--     admin-reviewed link is approved later.
--   - New email/password users receive auth.users.id as user_sub.
--   - The app does NOT auto-merge rows that share an email.
-- ============================================================

-- ------------------------------------------------------------
-- Optional audit: emails that appear on both Google-era profile
-- rows and confirmed Auth users. This is informational only.
-- It must NOT be used to rewrite user_sub automatically.
-- ------------------------------------------------------------

-- SELECT
--   sp.user_sub AS google_or_legacy_user_sub,
--   lower(sp.email) AS profile_email,
--   au.id AS auth_user_id,
--   au.email_confirmed_at
-- FROM public.student_profiles sp
-- JOIN auth.users au
--   ON lower(sp.email) = lower(au.email)
-- WHERE sp.email IS NOT NULL
--   AND btrim(sp.email) <> ''
--   AND au.email_confirmed_at IS NOT NULL
-- ORDER BY profile_email;

-- ------------------------------------------------------------
-- Proposed linking table (manual / reviewed migration only)
-- Both identities must be verified before a link can be approved.
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS public.account_identity_links (
  id bigserial PRIMARY KEY,
  google_user_sub text NOT NULL,
  auth_user_id uuid NOT NULL,
  verified_email text NOT NULL,
  status text NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'approved', 'rejected', 'revoked')),
  requested_at timestamptz NOT NULL DEFAULT now(),
  reviewed_at timestamptz,
  reviewed_by text,
  notes text,
  CONSTRAINT account_identity_links_google_uidx UNIQUE (google_user_sub),
  CONSTRAINT account_identity_links_auth_uidx UNIQUE (auth_user_id)
);

COMMENT ON TABLE public.account_identity_links IS
  'Reviewed links between Google OAuth subs and Supabase Auth user ids. Never auto-approve.';

-- Enable RLS and keep client roles locked down (same posture as student tables).
ALTER TABLE public.account_identity_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.account_identity_links FORCE ROW LEVEL SECURITY;

REVOKE ALL ON TABLE public.account_identity_links FROM anon, authenticated, public;
GRANT ALL ON TABLE public.account_identity_links TO service_role;

-- ------------------------------------------------------------
-- Approval rules (application / operator checklist — not automatic):
--   1. Auth user email_confirmed_at IS NOT NULL
--   2. Google account email is verified by the IdP
--   3. lower(Google email) == lower(Auth email) == verified_email
--   4. google_user_sub already owns the student rows to preserve
--   5. auth_user_id has no conflicting student rows, OR those rows
--      are empty disposable signup shells owned by the same person
--   6. Human reviewer sets status = 'approved'
--
-- After approval, the app may recognize either identity as the same
-- person ONLY through this table. Do not rewrite historical user_sub
-- values unless a separate, explicitly reviewed data-move script is
-- written and tested on a staging copy first.
-- ------------------------------------------------------------

-- Example read for an approved link (safe / non-mutating):
-- SELECT google_user_sub, auth_user_id, verified_email
-- FROM public.account_identity_links
-- WHERE status = 'approved';
