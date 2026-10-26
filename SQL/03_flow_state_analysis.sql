WITH ide_events AS
(
    SELECT
        developer_id,
        event_time,
        duration_minutes,
        lagInFrame(event_time, 1, event_time) OVER
        (
            PARTITION BY developer_id
            ORDER BY event_time
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS previous_event_time
    FROM COGNISTREAM.ide_events
    WHERE duration_minutes > 0
),
session_flags AS
(
    SELECT
        *,
        if(
            dateDiff('minute', previous_event_time, event_time) > 15
            OR previous_event_time = event_time,
            1,
            0
        ) AS new_session
    FROM ide_events
),
session_ids AS
(
    SELECT
        *,
        sum(new_session) OVER
        (
            PARTITION BY developer_id
            ORDER BY event_time
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS session_id
    FROM session_flags
)
SELECT
    developer_id,
    session_id,
    min(event_time) AS session_start,
    max(event_time) AS last_event_time,
    count() AS event_count,
    sum(duration_minutes) AS total_coding_minutes
FROM session_ids
GROUP BY developer_id, session_id
HAVING sum(duration_minutes) >= 90
ORDER BY total_coding_minutes DESC
LIMIT 100;