# TV9 Comscore Analytics Pipeline

## Project Overview

This project is an end-to-end analytics engineering pipeline built to automate the ingestion, transformation, validation, and reporting of Comscore digital audience data.

The objective was to eliminate manual data handling and create a repeatable reporting workflow for tracking publisher performance, audience growth trends, and competitive benchmarking across major digital media networks.

The pipeline fetches raw monthly Comscore datasets, applies data quality controls, standardizes the schema, loads the cleaned data into PostgreSQL, and powers an interactive Power BI dashboard for business analysis.

This project was designed with production-style principles such as schema validation, data integrity checks, logging, and modular SQL layers.

---

## Business Problem

Digital media performance reporting often involves fragmented CSV files, manual validation, and repetitive dashboard refreshes. This creates operational overhead and increases the risk of reporting inconsistencies.

To solve this, the pipeline was built to:

* Automate monthly Comscore ingestion
* Standardize audience datasets into a structured warehouse layer
* Validate data quality before loading
* Enable fast business reporting through PostgreSQL
* Build a centralized dashboard for audience trend analysis

---

## Solution Architecture

```text
Raw Comscore CSV
       │
       ▼
Python ETL Pipeline
(Fetch → Validate → Clean → Transform)
       │
       ▼
PostgreSQL Storage Layer
(Schema + Constraints + Indexes)
       │
       ▼
SQL Business Layer
(Analytics + Quality Checks + Monitoring)
       │
       ▼
Power BI Dashboard
(KPIs + Trend Analysis + Competitive Benchmarking)
```

---

## Tech Stack

| Layer                 | Technology       |
| --------------------- | ---------------- |
| Data Ingestion        | Python, Requests |
| Data Processing       | Pandas           |
| Data Warehouse        | PostgreSQL       |
| Database Connectivity | SQLAlchemy       |
| Business Logic        | SQL              |
| Visualization         | Power BI         |
| Monitoring            | Logging          |
| Version Control       | Git, GitHub      |

---

## Core Features

### Automated Data Ingestion

Fetches the latest Comscore CSV directly from the source endpoint.

### Schema Validation

Ensures incoming files match the expected production schema before processing.

### Data Cleaning

Handles:

* duplicate removal
* null value filtering
* type standardization
* text normalization

### Data Quality Checks

Validates:

* duplicate business keys
* negative audience counts
* schema mismatches
* missing critical fields

### Full Refresh Load Strategy

Implements table truncation and reload for maintaining fresh monthly snapshots.

### SQL Analytics Layer

Separates analytical logic into reusable SQL modules for business reporting.

### Dashboard Reporting

Provides business-facing KPIs and trend visualizations through Power BI.

---

## Project Structure

```text
PowerBI_Automation_Project/
├── automation/
│   ├── automation.py
│   ├── config.py
│   └── requirements.txt
│
├── data/
│   └── sample.csv
│
├── exports/
│   └── cleaned_comscore.csv
│
├── logs/
│   └── automation.log
│
├── powerbi/
│   └── TV9 Comscore Dashboard.pbix
│
├── sql/
│   ├── 01_schema.sql
│   ├── 02_constraints.sql
│   ├── 03_indexes.sql
│   ├── 04_quality_checks.sql
│   ├── 05_business_queries.sql
│   └── 06_monitoring_queries.sql
│
├── .env.example
├── .gitignore
└── README.md
```

---

## Database Design

The PostgreSQL layer is structured for analytical workloads.

### Includes:

* normalized schema structure
* business key constraints
* data integrity checks
* optimized indexes for filtering and aggregation
* operational monitoring queries

### Business Key Logic:

```sql
(property_name, segments, year, month_num)
```

This ensures uniqueness for each publisher-segment-month record.

---

## Power BI Dashboard Coverage

The dashboard provides visibility into:

* Portfolio Audience Performance
* Month-over-Month Growth (MoM)
* Quarter-over-Quarter Growth (QoQ)
* Year-over-Year Growth (YoY)
* Market Leader Analysis
* Growth Leader Analysis
* Biggest Decliner Tracking
* Monthly Audience Trend by Network
* Segment-level Competitive Benchmarking

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd PowerBI_Automation_Project
```

---

### 2. Install Dependencies

```bash
pip install -r automation/requirements.txt
```

---

### 3. Configure Environment Variables

Create:

```text
.env
```

Add:

```env
DB_HOST=localhost
DB_NAME=TV9
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

---

### 4. Create Database Table

Run:

```sql
sql/01_schema.sql
sql/02_constraints.sql
sql/03_indexes.sql
```

---

### 5. Execute Pipeline

```bash
python automation/automation.py
```

---

## Data Quality Framework

Before every load, the pipeline validates:

* Schema consistency
* Null business keys
* Duplicate primary business records
* Invalid numeric values
* Negative audience metrics
* Growth outliers

This prevents bad data from entering the reporting layer.

---

## Business Use Cases

This pipeline supports:

* Media audience trend reporting
* Publisher performance tracking
* Competitive network analysis
* Historical growth benchmarking
* Segment-level market intelligence
* Executive reporting dashboards

---

## Future Improvements

Planned enhancements:

* Incremental load framework
* Airflow orchestration
* Automated Power BI refresh API integration
* Data anomaly alerting
* Cloud warehouse migration (BigQuery / Snowflake)
* CI/CD deployment pipeline

---

## Key Learnings

Through this project:

* Built production-style ETL workflows
* Applied data quality engineering principles
* Designed analytical PostgreSQL schemas
* Improved SQL optimization practices
* Developed business-focused Power BI reporting
* Structured reusable analytics layers for reporting pipelines

---

## Author

**Priyam Patel**
Data Analyst & Engineering | Analytics Engineering | Business Intelligence
