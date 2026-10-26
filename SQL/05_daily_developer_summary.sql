
-- CogniStream: Daily Developer Activity Summary

SELECT
    developer_id,
    event_date,
    count() AS total_events,

    countIf(source = 'IDE') AS ide_events,
    countIf(source = 'GitHub') AS github_events,
    countIf(source = 'Slack') AS slack_events,

    uniqExact(source) AS tools_used,

    round(
        countIf(source = 'Slack') * 100.0 / count(),
        2
    ) AS slack_activity_percent,

    round(
        countIf(source = 'IDE') * 100.0 / count(),
        2
    ) AS ide_activity_percent

FROM COGNISTREAM.unified_events
GROUP BY
    developer_id,
    event_date
ORDER BY
    event_date,
    developer_id;
