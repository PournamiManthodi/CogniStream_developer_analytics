
from pathlib import Path
import pandas as pd

# Find the root directory of the project
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Paths to the three datasets
FILES = {
    "Slack": RAW_DIR / "slack_events.csv",
    "IDE": RAW_DIR / "ide_activity.csv",
    "GitHub": RAW_DIR / "github_events.csv",
}


def inspect_dataset(source_name, file_path):
    print("\n" + "=" * 60)
    print(f"{source_name.upper()} DATASET")
    print("=" * 60)

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        return

    try:
        df = pd.read_csv(file_path)
    except Exception as error:
        print(f"Could not read file: {error}")
        return

    print(f"\nFile: {file_path.name}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes.to_string())

    print("\nMissing values by column:")
    print(df.isna().sum().to_string())

    print("\nExact duplicate rows:", df.duplicated().sum())

    # Check timestamp validity
    if "event_time" in df.columns:
        timestamps = pd.to_datetime(
            df["event_time"],
            errors="coerce",
            utc=True
        )

        print("\nInvalid timestamps:", timestamps.isna().sum())
        print("Earliest valid timestamp:", timestamps.min())
        print("Latest valid timestamp:", timestamps.max())

    # Check IDE activity duration
    if "duration_minutes" in df.columns:
        duration = pd.to_numeric(
            df["duration_minutes"],
            errors="coerce"
        )

        print("\nInvalid duration values:", duration.isna().sum())
        print("Zero or negative durations:", (duration <= 0).sum())
        print("\nDuration statistics:")
        print(duration.describe().to_string())

    # Check category frequencies
    for column in ["event_type", "activity_type", "message_type"]:
        if column in df.columns:
            print(f"\nFrequency of {column}:")
            print(df[column].value_counts(dropna=False).to_string())

    print("\nFirst 5 rows:")
    print(df.head().to_string(index=False))


def main():
    for source_name, file_path in FILES.items():
        inspect_dataset(source_name, file_path)


if __name__ == "__main__":
    main()

