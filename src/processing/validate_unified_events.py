
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FILE_PATH = PROJECT_ROOT / "data" / "processed" / "unified_events.csv"

print("=" * 60)
print("COGNISTREAM UNIFIED DATA VALIDATION")
print("=" * 60)

if not FILE_PATH.exists():
    raise FileNotFoundError(f"Unified dataset not found: {FILE_PATH}")

df = pd.read_csv(FILE_PATH)

print("\n1. BASIC INFORMATION")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Column names:", df.columns.tolist())

print("\n2. SOURCE DISTRIBUTION")
print(df["source"].value_counts(dropna=False))

print("\n3. DUPLICATE CHECKS")
print("Duplicate event IDs:", df["event_id"].duplicated().sum())
print("Exact duplicate rows:", df.duplicated().sum())

print("\n4. REQUIRED FIELD CHECKS")
required = [
    "event_id",
    "developer_id",
    "event_time",
    "source",
    "event_type",
    "event_date",
    "event_hour",
]

for column in required:
    print(f"{column}: {df[column].isna().sum()} missing values")

print("\n5. TIMESTAMP VALIDATION")
timestamps = pd.to_datetime(df["event_time"], errors="coerce", utc=True)

print("Invalid timestamps:", timestamps.isna().sum())

expected_dates = timestamps.dt.strftime("%Y-%m-%d")
actual_dates = df["event_date"].astype("string")

print(
    "Event date mismatches:",
    (expected_dates != actual_dates).fillna(True).sum()
)

expected_hours = timestamps.dt.hour
actual_hours = pd.to_numeric(df["event_hour"], errors="coerce")

print(
    "Event hour mismatches:",
    (expected_hours != actual_hours).fillna(True).sum()
)

print("\n6. SOURCE-SPECIFIC VALIDATION")

rules = {
    "Slack": ["channel"],
    "IDE": ["language", "duration_minutes"],
    "GitHub": ["repository", "branch"],
}

for source, columns in rules.items():
    subset = df[df["source"] == source]
    print(f"\n{source}: {len(subset)} rows")

    for column in columns:
        print(f"  Missing {column}: {subset[column].isna().sum()}")

print("\n7. FINAL CHECK")
expected_sources = {"Slack", "IDE", "GitHub"}
actual_sources = set(df["source"].dropna().unique())

print("Expected sources present:", actual_sources == expected_sources)
print("Expected total rows (299924):", len(df) == 299924)

print("\nValidation finished. Review all results before proceeding.")
