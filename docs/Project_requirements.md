# CogniStream — Project Requirements

## 1. Project Overview

**Project Name:** CogniStream — Developer Flow-State & Cognitive Load Analytics

**Project Domain:** Data Analytics, Data Engineering and Developer Productivity Analytics

**Project Objective:** To analyse developer activity events from GitHub, Slack and IDE tools to understand activity patterns, context switching and potential interruptions during software development.

## 2. Problem Statement

Traditional productivity metrics, such as commits and issues closed, do not fully explain how developers spend their time or how interruptions may affect focused work. CogniStream aims to combine developer activity events into a unified dataset and analyse patterns that may help identify potential periods of uninterrupted focus and sources of workflow friction.

## 3. Data Sources

The project uses three CSV datasets:

- `github_events.csv` — GitHub activity, including commits, pull requests, reviews and issues.
- `slack_events.csv` — Slack activity, including messages, mentions, replies and notifications.
- `ide_activity.csv` — IDE activity, including coding, debugging, file editing, terminal use and idle activity.

The datasets are stored in the `data/raw/` directory.

## 4. Project Objectives

1. Inspect and validate the source datasets.
2. Identify missing values, duplicate records, invalid timestamps and inconsistent categories.
3. Standardise and combine events into a unified event schema.
4. Develop a repeatable data-processing and ingestion workflow.
5. Store and query event data using the planned analytical database.
6. Analyse activity trends, potential interruptions and context switching.
7. Define and evaluate a transparent rule for identifying candidate flow-state periods.
8. Build a dashboard to present developer activity metrics and analytical findings.
9. Document the methodology, limitations and project outcomes.

## 5. Key Analytical Questions

- How many events are recorded by each source?
- How does developer activity change over time?
- Which types of GitHub, Slack and IDE events occur most frequently?
- How often do Slack events occur near IDE activity?
- What patterns may indicate context switching?
- How can candidate periods of uninterrupted IDE activity be identified?
- Which activity patterns are associated with longer focus periods?

## 6. Planned Technology Stack

- **Programming:** Python
- **Data processing:** Pandas and/or Polars
- **Workflow orchestration:** Apache Airflow
- **Analytical database:** ClickHouse
- **Backend API:** FastAPI
- **Dashboard:** React and Tremor.js
- **Version control:** Git and GitHub

## 7. Data Quality and Validation

The datasets will be checked for:

- Missing values
- Exact duplicate records
- Invalid or unparseable timestamps
- Incorrect data types
- Invalid duration values
- Unexpected event categories
- Inconsistent identifiers and timestamp formats

The original raw datasets will be preserved. Any cleaning and transformation will be performed on separate processed data.

## 8. Planned Project Deliverables

- Source-data inspection scripts
- Data dictionary and data-quality report
- Unified event dataset and processing scripts
- Automated ingestion workflow
- Analytical database tables and queries
- Flow-state and interruption analysis
- Interactive dashboard
- Project documentation and final presentation

## 9. Evaluation Criteria

The project will be evaluated based on:

- Correctness and consistency of the processed data
- Successful integration of the three event sources
- Reliability and repeatability of the processing workflow
- Clarity of analytical metrics and visualisations
- Transparency of flow-state and interruption definitions
- Documentation quality and acknowledgement of data limitations

## 10. Assumptions and Limitations

The activity records will be treated as event logs, and their provenance will be documented. Unless verified otherwise, the analysis will not assume that the datasets represent real developer behaviour.

A Slack event does not necessarily prove an interruption, and an IDE event does not independently prove continuous concentration. Flow-state metrics will therefore be presented as rule-based estimates rather than direct measurements of cognitive state.

## 11. Project Status

**Current phase:** Project setup and initial dataset validation.

The next phase is to inspect the three source datasets, document data quality and design the unified event schema before implementing the ingestion pipeline.
