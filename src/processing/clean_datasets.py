
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

FILES = {
    "Slack": "slack_events.csv",
    "IDE": "ide_activity.csv",
    "GitHub": "github_events.csv",
}

REQUIRED_COLUMNS = {
    "Slack": ["developer_id", "event_time", "channel", "message_type"],
    "IDE": [
        "developer_id", "event_time", "activity_type",
        "language", "duration_minutes"
    ],
    "GitHub": [
        "developer_id", "event_time", "event_type",
        "repository", "branch"
    ],
}

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("COGNISTREAM SOURCE DATA CLEANING")
print("=" * 60)

for source, filename in FILES.items():
    input_path = RAW_DIR / filename
    output_path = OUTPUT_DIR / filename.replace(".csv", "_cleaned.csv")

    print(f"\n--- {source} ---")

    if not input_path.exists():
        print(f"ERROR: File not found: {input_path}")
        continue

    df = pd.read_csv(input_path)
    original_rows = len(df)

    # Check that required columns exist.
    missing_columns = [
        col for col in REQUIRED_COLUMNS[source]
        if col not in df.columns
    ]

    if missing_columns:
        print("ERROR: Required columns missing:", missing_columns)
        continue

    # Standardize whitespace in column names.
    df.columns = df.columns.str.strip()

    # Normalize timestamps to UTC; invalid timestamps become missing.
    df["event_time"] = pd.to_datetime(
        df["event_time"], errors="coerce", utc=True
    )

    invalid_timestamps = int(df["event_time"].isna().sum())
    missing_required = int(
        df[REQUIRED_COLUMNS[source]].isna().any(axis=1).sum()
    )

    # Identify exact duplicates before removing them.
    duplicate_count = int(df.duplicated().sum())

    # Stop rather than silently discard records with invalid required data.
    if invalid_timestamps > 0 or missing_required > 0:
        print("Cleaning stopped for this file.")
        print("Invalid timestamps:", invalid_timestamps)
        print("Rows with missing required fields:", missing_required)
        print("Review these rows before cleaning.")
        continue

    # Remove exact duplicate rows only in the processed copy.
    cleaned = df.drop_duplicates().copy()

    cleaned.to_csv(output_path, index=False)

    print("Original rows:", original_rows)
    print("Exact duplicate rows identified:", duplicate_count)
    print("Rows in cleaned copy:", len(cleaned))
    print("Rows removed:", original_rows - len(cleaned))
    print("Invalid timestamps:", invalid_timestamps)
    print("Rows with missing required fields:", missing_required)
    print("Saved to:", output_path)

print("\nCleaning pass finished. Raw files were not modified.")
