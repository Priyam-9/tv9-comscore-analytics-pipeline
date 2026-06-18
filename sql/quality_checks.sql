-- Duplicate business key check
SELECT
    property_name,
    segments,
    year,
    month_num,
    COUNT(*)
FROM public.comscore_data
GROUP BY 1,2,3,4
HAVING COUNT(*) > 1;


-- Negative audience validation
SELECT *
FROM public.comscore_data
WHERE unique_users < 0;


-- Missing critical fields
SELECT *
FROM public.comscore_data
WHERE property_name IS NULL
   OR segments IS NULL
   OR report_month IS NULL;


-- Invalid growth outliers
SELECT *
FROM public.comscore_data
WHERE mom_pct > 500
   OR mom_pct < -500
   OR qoq_pct > 500
   OR qoq_pct < -500
   OR yoy_pct > 500
   OR yoy_pct < -500;


-- Network mapping validation
SELECT
    display_name,
    is_network,
    parent_network
FROM public.comscore_data;