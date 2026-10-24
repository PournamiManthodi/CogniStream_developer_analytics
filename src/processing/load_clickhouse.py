
import os
from pathlib import Path

import polars as pl
import clickhouse_connect
from dotenv import load_dotenv


# --------------------------------------------------
# 1. PROJECT PATHS AND CONNECTION SETTINGS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"

load_dotenv(PROJECT_ROOT / ".env")

host = os.getenv("CLICKHOUSE_HOST")
port = int(os.getenv("CLICKHOUSE_PORT", "8443"))
username = os.getenv("CLICKHOUSE_USER")
password = os.getenv("CLICKHOUSE_PASSWORD")

if not all([host, username, password]):
    raise ValueError(
        "Missing ClickHouse credentials. Check the .env file "
        "in your project root."
    )

# --------------------------------------------------
# 2. READ AND STANDARDIZE EVENT DATA WITH POLARS
# --------------------------------------------------

def read_csv(filename: str) -> pl.DataFrame:
    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pl.read_csv(path, try_parse_dates=False)

    if df.height == 0:
        raise ValueError(f"Dataset is empty: {filename}")

    return df


def standardize_event_time(df: pl.DataFrame) -> pl.DataFrame:
    if "event_time" not in df.columns:
        raise ValueError("Required column event_time is missing.")

    df = df.with_columns(
        pl.col("event_time")
        .cast(pl.String)
        .str.to_datetime(time_zone="UTC", strict=True)
    )

    return df


def add_source_event_id(
    df: pl.DataFrame, prefix: str
) -> pl.DataFrame:
    # Stable IDs for the source-specific tables.
    df = df.with_row_index(name="_row_number", offset=1)

    df = df.with_columns(
        pl.concat_str(
            [
                pl.lit(prefix),
                pl.col("_row_number").cast(pl.String),
            ]
        ).alias("event_id")
    )

    return df.drop("_row_number")


def prepare_github() -> pl.DataFrame:
    df = read_csv("github_events_cleaned.csv")
    df = standardize_event_time(df)
    df = add_source_event_id(df, "GH_")

    return df.select(
        "event_id",
        "developer_id",
        "event_time",
        "event_type",
        "repository",
        "branch",
    )


def prepare_slack() -> pl.DataFrame:
    df = read_csv("slack_events_cleaned.csv")
    df = standardize_event_time(df)
    df = add_source_event_id(df, "SL_")

    return df.select(
        "event_id",
        "developer_id",
        "event_time",
        "channel",
        "message_type",
    )


def prepare_ide() -> pl.DataFrame:
    df = read_csv("ide_activity_cleaned.csv")
    df = standardize_event_time(df)
    df = add_source_event_id(df, "IDE_")

    df = df.with_columns(
        pl.col("duration_minutes").cast(pl.UInt16, strict=True)
    )

    return df.select(
        "event_id",
        "developer_id",
        "event_time",
        "activity_type",
        "language",
        "duration_minutes",
    )


def prepare_unified() -> pl.DataFrame:
    df = read_csv("unified_events.csv")
    df = standardize_event_time(df)

    # Match the ClickHouse unified_events table schema.
    df = df.with_columns(
        pl.col("event_id").cast(pl.String),
        pl.col("source_row_number").cast(pl.UInt32, strict=True),
        pl.col("developer_id").cast(pl.String),
        pl.col("source").cast(pl.String),
        pl.col("event_type").cast(pl.String),
        pl.col("duration_minutes").cast(pl.UInt16, strict=False),
        pl.col("channel").cast(pl.String),
        pl.col("language").cast(pl.String),
        pl.col("repository").cast(pl.String),
        pl.col("branch").cast(pl.String),
        pl.col("event_date").str.to_date(strict=True),
        pl.col("event_hour").cast(pl.UInt8, strict=True),
    )

    return df.select(
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
        "event_date",
        "event_hour",
    )


# --------------------------------------------------
# 3. CONNECT AND LOAD INTO CLICKHOUSE
# --------------------------------------------------

def main():
    print("Preparing datasets with Polars...")

    datasets = {
        "github_events": prepare_github(),
        "slack_events": prepare_slack(),
        "ide_events": prepare_ide(),
        "unified_events": prepare_unified(),
    }

    expected_rows = {
        "github_events": 99972,
        "slack_events": 99952,
        "ide_events": 100000,
        "unified_events": 299924,
    }

    for table, df in datasets.items():
        print(f"{table}: {df.height:,} rows")
        if df.height != expected_rows[table]:
            raise ValueError(
                f"{table}: expected {expected_rows[table]:,} rows, "
                f"found {df.height:,}. Check the input CSV."
            )

    print("\nConnecting to ClickHouse Cloud...")

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=username,
        password=password,
        secure=True,
        database="COGNISTREAM",
    )

    try:
        print("Connected. Checking service...")

        print("ClickHouse version:", client.server_version)

        # These are dedicated project tables. Clearing them before
        # each complete reload prevents duplicate rows on reruns.
        # Do not use this on tables containing other important data.
        for table in datasets:
            client.command(
                f"TRUNCATE TABLE COGNISTREAM.{table}"
            )

        for table, df in datasets.items():
            print(f"\nLoading {table}...")

            client.insert_df_arrow(
                table,
                df,
                database="COGNISTREAM",
            )

            result = client.query(
                f"SELECT count() FROM COGNISTREAM.{table}"
            )
            actual_rows = result.result_set[0][0]

            print(f"Rows in ClickHouse: {actual_rows:,}")

            if actual_rows != expected_rows[table]:
                raise RuntimeError(
                    f"Row count mismatch in {table}: "
                    f"expected {expected_rows[table]:,}, "
                    f"found {actual_rows:,}"
                )

        print("\nAll four tables loaded and row counts verified.")

        print("\nUnified events by source:")
        result = client.query(
            """
            SELECT source, count() AS total_events
            FROM COGNISTREAM.unified_events
            GROUP BY source
            ORDER BY source
            """
        )

        for row in result.result_set:
            print(f"{row[0]}: {row[1]:,}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
