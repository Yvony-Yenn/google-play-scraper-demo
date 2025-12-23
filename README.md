# Google Play Scraper Demo

This repository contains a simple first-version Python scraper for collecting Google Play Store app metadata and reviews.  
The demo includes basic request workflow, parsing logic, and structured output for future data ingestion pipelines.

## Features
- Fetch Google Play Store app metadata (title, developer, rating, installs)
- Basic review extraction
- Simple request handling (no complex anti-bot)
- Outputs data in JSON/CSV format

## Notes
This is an initial demo version prepared after finals week.  
Weekly iterations and improvements will continue next week (error handling, pagination, review depth, etc.).

## Data Loading & Database Schema

The cleaned Google Play review data is loaded into a MySQL database
using a custom schema defined in `sql/review_analytics.sql`.

The loading logic is implemented in `scripts/load_to_mysql.py`, which:
- Inserts app metadata and reviews into normalized tables
- Uses primary keys to prevent duplicate records
- Is safe to re-run (idempotent)

Current dataset size: ~7,300 reviews.

## How to Run
Set MYSQL_PASSWORD as an environment variable before running,
and ensure the MySQL schema has been created using `sql/review_analytics.sql`.

