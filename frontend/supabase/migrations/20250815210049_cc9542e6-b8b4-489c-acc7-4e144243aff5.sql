-- Check for any remaining SECURITY DEFINER functions and fix them
SELECT proname, proconfig
FROM pg_proc 
WHERE pronamespace = 'public'::regnamespace
AND prosecdef = true
AND (proconfig IS NULL OR NOT (proconfig @> ARRAY['search_path=public, pg_catalog']));