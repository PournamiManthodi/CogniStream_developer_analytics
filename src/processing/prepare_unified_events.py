
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

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
    path = PROCESSED_DIR / file_name

    if not path.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {path}\n"
            "Run clean_datasets.py first."
        )

    df = pd.read_csv(path)

    required = ["developer_id", "event_time", event_column]
    missing_columns = set(required) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"{file_name} is missing columns: {missing_columns}"
        )

    # Preserve original CSV row references when available.
    if "source_row_number" not in df.columns:
        df["source_row_number"] = range(2, len(df) + 2)

    df["event_time"] = pd.to_datetime(
        df["event_time"], errors="raise", utc=True
    )

    df["event_type"] = df[event_column].astype("string")
    df["source"] = source

    for column in COMMON_COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA

    # IDs identify the retained source rows.
    df["event_id"] = (
        source.lower()
        + "_"
        + df["source_row_number"].astype(str)
    )

    return df[COMMON_COLUMNS]


slack = standardise_events(
    "slack_events_cleaned.csv", "Slack", "message_type"
)

ide = standardise_events(
    "ide_activity_cleaned.csv", "IDE", "activity_type"
)

github = standardise_events(
    "github_events_cleaned.csv", "GitHub", "event_type"
)

unified = pd.concat([slack, ide, github], ignore_index=True)

unified = unified.sort_values(
    ["event_time", "developer_id", "source"],
    kind="stable"
).reset_index(drop=True)

unified["event_date"] = unified["event_time"].dt.strftime("%Y-%m-%d")
unified["event_hour"] = unified["event_time"].dt.hour

output_path = PROCESSED_DIR / "unified_events.csv"
unified.to_csv(output_path, index=False)

print("=" * 60)
print("CLEANED UNIFIED DATASET CREATED")
print("=" * 60)
print("Output:", output_path)
print("Rows:", len(unified))
print("Columns:", len(unified.columns))

print("\nRows by source:")
print(unified["source"].value_counts())

print("\nDuplicate event IDs:", unified["event_id"].duplicated().sum())
print("Exact duplicate rows:", unified.duplicated().sum())
print("Invalid timestamps:", unified["event_time"].isna().sum())

print("\nRows by source after cleaning:")
print(unified.groupby("source").size())

print("\nSample records:")
print(unified.head().to_string(index=False))
