print("Duplicate investigation script started!")

from pathlib import Path
import pandas as pd

print("Python and Pandas are working.")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

print("Project folder:", PROJECT_ROOT)
print("Raw data folder:", RAW_DIR)
print("Raw folder exists:", RAW_DIR.exists())
print("Files found:", [p.name for p in RAW_DIR.glob("*.csv")])



from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

FILES = {
    "Slack": RAW_DIR / "slack_events.csv",
    "IDE": RAW_DIR / "ide_activity.csv",
    "GitHub": RAW_DIR / "github_events.csv",
}

for source, path in FILES.items():
    print("\n" + "=" * 50)
    print(f"{source.upper()} DUPLICATE INVESTIGATION")
    print("=" * 50)

    df = pd.read_csv(path)

    # Mark every occurrence of an exact duplicate,
    # including the first occurrence.
    duplicate_mask = df.duplicated(keep=False)
    duplicate_rows = df[duplicate_mask]

    print("Total rows:", len(df))
    print("Exact duplicate rows after first occurrence:",
          df.duplicated().sum())
    print("Rows belonging to duplicate groups:",
          len(duplicate_rows))

    if not duplicate_rows.empty:
        print("\nExamples of repeated records:")
        print(duplicate_rows.head(10).to_string(index=False))

        print("\nRepeated record groups:")
        print(
            duplicate_rows
            .value_counts()
            .head(10)
            .to_string()
        )
    else:
        print("No exact duplicate rows found.")
