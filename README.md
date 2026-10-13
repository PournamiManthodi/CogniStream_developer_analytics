# CogniStream — Developer Flow-State & Cognitive Load Analytics

## Project Overview

CogniStream is a developer activity analytics project designed to explore uninterrupted coding sessions, potential work interruptions, and context switching.

The project aims to help engineering managers understand activity patterns beyond basic output measures such as commits and completed tickets.

## Business Problem

Traditional engineering productivity metrics describe output but do not fully explain interruptions or the continuity of focused work.

CogniStream investigates timestamped developer activity events to identify focus-session patterns, analyse potential interruptions, and generate data-informed recommendations for improving the developer experience.

## Project Objectives

- Collect and organise developer activity events from mock GitHub, Slack, and IDE sources.
- Clean and validate timestamped event data.
- Calculate uninterrupted coding sessions using documented rules.
- Analyse interruptions and transitions between activity types.
- Build an interactive dashboard to communicate findings.
- Document data quality, methodology, limitations, and recommendations.

## Planned Technology Stack

- **Programming:** Python
- **Data processing:** Polars
- **Orchestration:** Apache Airflow
- **Database:** ClickHouse
- **Backend:** FastAPI
- **Frontend:** React and Tremor.js
- **Version control:** Git and GitHub

## Planned Project Workflow

1. Generate or collect mock developer activity events.
2. Validate and clean the event data.
3. Load structured events into ClickHouse.
4. Calculate focus sessions, interruptions, and context switching.
5. Serve aggregated metrics through an API.
6. Present the results in an interactive dashboard.
7. Test, document, and review the project.

## Planned Analytical Metrics

- Total valid events
- Observed coding duration
- Uninterrupted coding sessions of at least 90 minutes
- Interruption counts and rates
- Context-switch counts
- Activity patterns by hour, day, and event source

Metric definitions will be documented and validated before final results are reported.

## Project Status

**Status:** In progress

This repository is being developed in stages. The technology stack, analytical metrics, and deliverables will be updated as each component is implemented and tested.

## Data and Privacy

The initial implementation will use synthetic or appropriately authorised data. Developer activity patterns will be analysed as operational indicators, not as direct measurements of mental state or individual productivity.

No confidential company information, private credentials, or unauthorised personal data should be committed to this repository.

## Repository Structure

- `data/` — raw and processed datasets
- `src/` — ingestion, processing, and analytics code
- `tests/` — data quality and logic tests
- `docs/` — project documentation
- `airflow/` — orchestration workflows
- `database/` — database schemas and SQL
- `backend/` — API implementation
- `frontend/` — dashboard application

## Author

Project developed as part of a data analytics learning and internship assignment.

## Disclaimer

The project is intended for analytical learning and demonstration. Findings depend on the quality, coverage, and assumptions of the event data.
