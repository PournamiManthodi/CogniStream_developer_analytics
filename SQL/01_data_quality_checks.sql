-- 1. Check event source distribution
SELECT
    source,
    count() AS total_events,
    uniqExact(developer_id) AS unique_developers
FROM COGNISTREAM.unified_events
GROUP BY source
ORDER BY total_events DESC;

-- 2. Check events by date
SELECT
    event_date,
    count() AS total_events
FROM COGNISTREAM.unified_events
GROUP BY event_date
ORDER BY event_date;

-- 3. Check event types
SELECT
    source,
    event_type,
    count() AS total_events
FROM COGNISTREAM.unified_events
GROUP BY source, event_type
ORDER BY source, total_events DESC;