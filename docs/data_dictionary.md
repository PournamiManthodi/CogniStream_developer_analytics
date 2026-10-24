# CogniStream Data Dictionary

## 1. Slack Events

| Column | Description | Data type |
|---|---|---|
| `developer_id` | Developer identifier associated with the event | String or identifier |
| `event_time` | Timestamp of the Slack event | Datetime |
| `channel` | Slack channel associated with the event | String |
| `message_type` | Recorded Slack event category | String |

## 2. IDE Activity

| Column | Description | Data type |
|---|---|---|
| `developer_id` | Developer identifier associated with the event | String or identifier |
| `event_time` | Timestamp of the IDE activity | Datetime |
| `activity_type` | Type of recorded IDE activity | String |
| `language` | Programming language associated with the activity, if available | String |
| `duration_minutes` | Recorded duration of the activity in minutes | Numeric |

## 3. GitHub Events

| Column | Description | Data type |
|---|---|---|
| `developer_id` | Developer identifier associated with the event | String or identifier |
| `event_time` | Timestamp of the GitHub event | Datetime |
| `event_type` | Type of GitHub event | String |
| `repository` | Repository associated with the event | String |
| `branch` | Branch associated with the event | String |

## 4. Notes

- Confirm each field's data type against the actual CSV.
- Record any additional columns present in the files.
- Use consistent names and definitions in the unified event schema.
- Keep source-specific values null when they do not apply to an event.
