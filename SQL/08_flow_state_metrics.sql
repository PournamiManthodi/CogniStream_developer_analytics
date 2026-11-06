-- CogniStream: Candidate Flow-State Metrics

SELECT
    developer_id,
    event_date,

    count() AS ide_events,

    round(
        sum(duration_minutes),
        2
    ) AS coding_minutes,

    round(
        avg(duration_minutes),
        2
    ) AS avg_session_duration

FROM COGNISTREAM.unified_events

WHERE source = 'IDE'

GROUP BY
    developer_id,
    event_date

ORDER BY
    event_date,
    developer_id;