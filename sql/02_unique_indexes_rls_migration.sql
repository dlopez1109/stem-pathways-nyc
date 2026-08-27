-- ============================================================
-- MIGRATION (manual review required — DO NOT auto-run)
-- STEM Pathways NYC: unique indexes + RLS lockdown
--
-- Prerequisites:
--   1. Run sql/01_duplicate_check_readonly.sql
--   2. Resolve any duplicate rows before creating unique indexes
--
-- Goal:
--   - Enforce intended uniqueness for upsert conflict targets
--   - Enable RLS on student data tables
--   - Revoke direct table access from anon / authenticated / public
--   - Preserve access for service_role (used by the Streamlit server)
-- ============================================================

BEGIN;

-- ------------------------------------------------------------
-- Unique indexes matching app upsert conflict targets
-- ------------------------------------------------------------

CREATE UNIQUE INDEX IF NOT EXISTS student_profiles_user_sub_uidx
  ON public.student_profiles (user_sub);

CREATE UNIQUE INDEX IF NOT EXISTS user_feedback_user_sub_uidx
  ON public.user_feedback (user_sub);

CREATE UNIQUE INDEX IF NOT EXISTS saved_opportunities_user_sub_opportunity_uidx
  ON public.saved_opportunities (user_sub, opportunity_name);

CREATE UNIQUE INDEX IF NOT EXISTS favorite_colleges_user_sub_college_uidx
  ON public.favorite_colleges (user_sub, college_name);

-- ------------------------------------------------------------
-- Row Level Security
-- The app uses the service_role key server-side. service_role
-- bypasses RLS, so enabling RLS still allows the app to work
-- while blocking PostgREST access via anon/authenticated keys.
-- ------------------------------------------------------------

ALTER TABLE public.student_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.saved_opportunities ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.favorite_colleges ENABLE ROW LEVEL SECURITY;

-- Force RLS even for table owners in the API path (optional hardening).
-- Comment these out if your Supabase project role setup requires otherwise.
ALTER TABLE public.student_profiles FORCE ROW LEVEL SECURITY;
ALTER TABLE public.user_feedback FORCE ROW LEVEL SECURITY;
ALTER TABLE public.saved_opportunities FORCE ROW LEVEL SECURITY;
ALTER TABLE public.favorite_colleges FORCE ROW LEVEL SECURITY;

-- ------------------------------------------------------------
-- Revoke client-facing privileges; keep service_role usable
-- ------------------------------------------------------------

REVOKE ALL ON TABLE public.student_profiles FROM anon, authenticated, public;
REVOKE ALL ON TABLE public.user_feedback FROM anon, authenticated, public;
REVOKE ALL ON TABLE public.saved_opportunities FROM anon, authenticated, public;
REVOKE ALL ON TABLE public.favorite_colleges FROM anon, authenticated, public;

GRANT ALL ON TABLE public.student_profiles TO service_role;
GRANT ALL ON TABLE public.user_feedback TO service_role;
GRANT ALL ON TABLE public.saved_opportunities TO service_role;
GRANT ALL ON TABLE public.favorite_colleges TO service_role;

COMMIT;

-- After applying, re-check duplicates (should return zero rows):
-- \i sql/01_duplicate_check_readonly.sql
