-- CogniStream: Context Switching Metrics

WITH ordered_events AS (
    SELECT
        developer_id,
        event_date,
        event_time,
        source,

        lagInFrame(source, 1) OVER (
            PARTITION BY developer_id, event_date
            ORDER BY event_time
        ) AS previous_source

    FROM COGNISTREAM.unified_events
)

SELECT
    developer_id,
    event_date,

    count() AS total_events,

    countIf(
        previous_source IS NOT NULL
        AND source != previous_source
    ) AS context_switches,

    round(
        countIf(
            previous_source IS NOT NULL
            AND source != previous_source
        ) * 100.0 / count(),
        2
    ) AS context_switch_rate

FROM ordered_events

GROUP BY
    developer_id,
    event_date

ORDER BY
    event_date,
    developer_id;