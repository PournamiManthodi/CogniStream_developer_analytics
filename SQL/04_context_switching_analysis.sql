
-- CogniStream: Developer Context-Switching Analysis
-- Measures transitions between IDE, GitHub, and Slack events.

WITH ordered_events AS
(
    SELECT
        developer_id,
        event_time,
        event_date,
        source,
        lagInFrame(source, 1, source) OVER
        (
            PARTITION BY developer_id
            ORDER BY event_time, event_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS previous_source,
        row_number() OVER
        (
            PARTITION BY developer_id
            ORDER BY event_time, event_id
        ) AS event_number
    FROM COGNISTREAM.unified_events
),
switch_events AS
(
    SELECT
        developer_id,
        event_date,
        source,
        previous_source,
        if(
            event_number > 1 AND source != previous_source,
            1,
            0
        ) AS is_context_switch
    FROM ordered_events
)
SELECT
    developer_id,
    event_date,
    count() AS total_events,
    sum(is_context_switch) AS context_switches,
    round(
        100.0 * sum(is_context_switch) / count(),
        2
    ) AS context_switch_rate_percent
FROM switch_events
GROUP BY developer_id, event_date
ORDER BY context_switches DESC
LIMIT 100;
