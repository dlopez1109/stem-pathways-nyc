-- ============================================================
-- READ-ONLY duplicate check for STEM Pathways NYC
-- Review and run manually in the Supabase SQL editor.
-- This script does NOT alter schema, data, or privileges.
-- ============================================================

-- Profiles: more than one row per user_sub
SELECT
  user_sub,
  COUNT(*) AS row_count
FROM public.student_profiles
GROUP BY user_sub
HAVING COUNT(*) > 1
ORDER BY row_count DESC, user_sub;

-- Feedback: more than one row per user_sub
SELECT
  user_sub,
  COUNT(*) AS row_count
FROM public.user_feedback
GROUP BY user_sub
HAVING COUNT(*) > 1
ORDER BY row_count DESC, user_sub;

-- Saved opportunities: more than one row per (user_sub, opportunity_name)
SELECT
  user_sub,
  opportunity_name,
  COUNT(*) AS row_count
FROM public.saved_opportunities
GROUP BY user_sub, opportunity_name
HAVING COUNT(*) > 1
ORDER BY row_count DESC, user_sub, opportunity_name;

-- Favorite colleges: more than one row per (user_sub, college_name)
SELECT
  user_sub,
  college_name,
  COUNT(*) AS row_count
FROM public.favorite_colleges
GROUP BY user_sub, college_name
HAVING COUNT(*) > 1
ORDER BY row_count DESC, user_sub, college_name;

-- Optional summary (still read-only)
SELECT
  'student_profiles' AS table_name,
  COUNT(*) FILTER (
    WHERE user_sub IN (
      SELECT user_sub
      FROM public.student_profiles
      GROUP BY user_sub
      HAVING COUNT(*) > 1
    )
  ) AS rows_in_duplicate_groups
FROM public.student_profiles
UNION ALL
SELECT
  'user_feedback',
  COUNT(*) FILTER (
    WHERE user_sub IN (
      SELECT user_sub
      FROM public.user_feedback
      GROUP BY user_sub
      HAVING COUNT(*) > 1
    )
  )
FROM public.user_feedback
UNION ALL
SELECT
  'saved_opportunities',
  COUNT(*) FILTER (
    WHERE (user_sub, opportunity_name) IN (
      SELECT user_sub, opportunity_name
      FROM public.saved_opportunities
      GROUP BY user_sub, opportunity_name
      HAVING COUNT(*) > 1
    )
  )
FROM public.saved_opportunities
UNION ALL
SELECT
  'favorite_colleges',
  COUNT(*) FILTER (
    WHERE (user_sub, college_name) IN (
      SELECT user_sub, college_name
      FROM public.favorite_colleges
      GROUP BY user_sub, college_name
      HAVING COUNT(*) > 1
    )
  )
FROM public.favorite_colleges;
