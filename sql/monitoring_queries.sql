-- Row volume
SELECT COUNT(*) AS total_rows
FROM public.comscore_data;


-- Latest data check
SELECT MAX(report_month) AS latest_month
FROM public.comscore_data;


-- Coverage by year
SELECT
    year,
    COUNT(*)
FROM public.comscore_data
GROUP BY year
ORDER BY year;


-- Distinct publishers
SELECT COUNT(DISTINCT display_name)
FROM public.comscore_data;

-- Load timestamps
SELECT
    MIN(load_timestamp),
    MAX(load_timestamp)
FROM public.comscore_data;