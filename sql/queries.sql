-- Market leader
SELECT
    parent_network,
    SUM(unique_users) AS total_users
FROM public.comscore_data
GROUP BY parent_network
ORDER BY total_users DESC;


-- Biggest growth leader
SELECT
    parent_network,
    AVG(mom_pct) AS avg_growth
FROM public.comscore_data
GROUP BY parent_network
ORDER BY avg_growth DESC;


-- Biggest decliner
SELECT
    parent_network,
    AVG(mom_pct) AS avg_decline
FROM public.comscore_data
GROUP BY parent_network
ORDER BY avg_decline ASC;


-- Segment distribution
SELECT
    segments,
    COUNT(*) AS cnt
FROM public.comscore_data
GROUP BY segments
ORDER BY cnt DESC;


-- Top properties by audience
SELECT
    property_name,
    SUM(unique_users) AS total_users
FROM public.comscore_data
GROUP BY property_name
ORDER BY total_users DESC
LIMIT 10;


-- Monthly trend
SELECT
    report_month,
    SUM(unique_users) AS total_users
FROM public.comscore_data
GROUP BY report_month
ORDER BY report_month;