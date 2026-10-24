# CogniStream — Initial Data Quality Report

## 1. Overview

The three source datasets were inspected using Python and Pandas. The initial validation covered dataset dimensions, column names, data types, missing values, exact duplicate rows, timestamp validity and selected category and duration statistics.

## 2. Initial Results

| Dataset | Rows | Columns | Missing Values | Exact Duplicate Rows | Invalid Timestamps |
|---|---:|---:|---:|---:|---:|
| Slack | 100,000 | 4 | 0 | 48 | 0 |
| IDE | 100,000 | 5 | 0 | 0 | 0 |
| GitHub | 100,000 | 5 | 0 | 28 | 0 |

## 3. Key Observations

- All three datasets were successfully loaded and inspected.
- No missing values were found in the inspected columns.
- No unparseable timestamps were detected by the initial timestamp check.
- Slack and GitHub contain exact duplicate rows that require investigation.
- IDE activity durations range from 1 to 90 minutes, with an average of approximately 45.43 minutes.
- All three datasets report the same timestamp range, from July 1, 2026, 09:00 to August 1, 2026, 08:59 UTC, according to the inspection output.

## 4. Planned Actions

1. Investigate exact duplicate records.
2. Validate event categories and developer identifiers.
3. Confirm timestamp and duration semantics.
4. Define a common schema for all three sources.
5. Create a combined event dataset while preserving source traceability.
6. Revalidate the combined dataset before analytical processing.

## 5. Limitations

These checks represent an initial quality assessment and do not establish that all records are accurate or representative of real developer behaviour. Duplicate-handling decisions and flow-state assumptions require further validation.

