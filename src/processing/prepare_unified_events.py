
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Standard columns shared across all event sources
COMMON_COLUMNS = [
    "event_id",
    "source_row_number",
    "developer_id",
    "event_time",
    "source",
    "event_type",
    "duration_minutes",
    "channel",
    "language",
    "repository",
    "branch",
]


def standardise_events(file_name, source, event_column):
    path = RAW_DIR / file_name
    df = pd.read_csv(path)

    required = ["developer_id", "event_time", event_column]
    missing_columns = set(required) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"{file_name} is missing columns: {missing_columns}"
        )

    # Preserve a reference to the original CSV row.
    df["source_row_number"] = range(2, len(df) + 2)

    # Parse timestamps consistently.
    df["event_time"] = pd.to_datetime(
        df["event_time"],
        errors="raise",
        utc=True
    )

    # Standardise event-type column names.
    df["event_type"] = df[event_column].astype("string")
    df["source"] = source

    # Populate optional columns only when available.
    for column in COMMON_COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA

    # IDs are unique to a source row, not deduplication keys.
    df["event_id"] = (
        source.lower()
        + "_"
        + df["source_row_number"].astype(str)
    )

    return df[COMMON_COLUMNS]


slack = standardise_events(
    "slack_events.csv", "Slack", "message_type"
)

ide = standardise_events(
    "ide_activity.csv", "IDE", "activity_type"
)

github = standardise_events(
    "github_events.csv", "GitHub", "event_type"
)

# Keep every row until duplicate-handling rules are decided.
unified = pd.concat(
    [slack, ide, github],
    ignore_index=True
)

# Sort by time for chronological analysis.
unified = unified.sort_values(
    ["event_time", "developer_id", "source"],
    kind="stable"
).reset_index(drop=True)

# Add useful time dimensions for future analysis.
unified["event_date"] = unified["event_time"].dt.date
unified["event_hour"] = unified["event_time"].dt.hour

output_path = PROCESSED_DIR / "unified_events.csv"
unified.to_csv(output_path, index=False)

print("Unified dataset created successfully.")
print("Output:", output_path)
print("Rows:", len(unified))
print("Columns:", len(unified.columns))
print("\nRows by source:")
print(unified["source"].value_counts())
print("\nMissing values by column:")
print(unified.isna().sum())
print("\nSample records:")
print(unified.head().to_string(index=False))
