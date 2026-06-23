import logging
import sys
from pathlib import Path
from io import StringIO

import pandas as pd
import requests
from sqlalchemy import create_engine, text

from config import DB_CONFIG

# PATHS

PROJECT_ROOT = Path(__file__).parent.parent

DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
EXPORTS_DIR = PROJECT_ROOT / "exports"
POWERBI_DIR = PROJECT_ROOT / "powerbi"
 
LOGS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# LOGGING

def setup_logging():

    logger = logging.getLogger()

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        LOGS_DIR / "automation.log"
    )

    console_handler = logging.StreamHandler(sys.stdout)

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logging()

#  SCHEMA

EXPECTED_COLUMNS = [
    "property_name",
    "display_name",
    "is_network",
    "parent_network",
    "segments",
    "report_month",
    "month_label",
    "year",
    "month_num",
    "quarter",
    "quarter_label",
    "financial_year",
    "unique_users",
    "prev_month_uu",
    "prev_quarter_uu",
    "prev_year_uu",
    "mom_pct",
    "mom_abs",
    "qoq_pct",
    "qoq_abs",
    "yoy_pct",
    "yoy_abs",
    "rank_in_segment",
    "data_source"
]

# FETCH CSV

def fetch_csv(url):

    logger.info("Downloading CSV")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    df = pd.read_csv(StringIO(response.text))

    logger.info(f"Rows downloaded: {len(df)}")

    return df

# VALIDATE SCHEMA

def validate_schema(df):

    actual_columns = [c.strip().lower() for c in df.columns]

    missing = [
        c for c in EXPECTED_COLUMNS
        if c not in actual_columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    logger.info("Schema validation passed")

# CLEAN DATA

def clean_data(df):

    logger.info("Cleaning data")

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    before = len(df)

    df = df.drop_duplicates()

    logger.info(
        f"Removed duplicates: {before - len(df)}"
    )

    critical_cols = [
        "property_name",
        "segments",
        "year",
        "month_num",
        "unique_users"
    ]

    before = len(df)

    df = df.dropna(subset=critical_cols)

    logger.info(
        f"Rows removed due to missing keys: "
        f"{before - len(df)}"
    )

    return df

# TYPE CONVERSION

def convert_types(df):

    logger.info("Converting data types")

    numeric_columns = [
        "year",
        "month_num",
        "quarter",
        "unique_users",
        "prev_month_uu",
        "prev_quarter_uu",
        "prev_year_uu",
        "mom_pct",
        "mom_abs",
        "qoq_pct",
        "qoq_abs",
        "yoy_pct",
        "yoy_abs",
        "rank_in_segment"
    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # FIX FOR POSTGRES BOOLEAN
    if "is_network" in df.columns:

        df["is_network"] = (
            pd.to_numeric(
                df["is_network"],
                errors="coerce"
            )
            .fillna(0)
            .astype(int)
            .astype(bool)
        )

    if "report_month" in df.columns:

        df["report_month"] = pd.to_datetime(
            df["report_month"],
            errors="coerce"
        )

    # Convert text columns
    text_columns = [
        "property_name",
        "display_name",
        "parent_network",
        "segments",
        "month_label",
        "quarter_label",
        "financial_year",
        "data_source"
    ]

    for col in text_columns:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .replace("nan", None)
            )

    return df
# DATA QUALITY CHECKS

def run_quality_checks(df):

    logger.info("Running quality checks")

    pk_duplicates = df.duplicated(
        subset=[
            "property_name",
            "segments",
            "year",
            "month_num"
        ]
    )

    duplicate_count = pk_duplicates.sum()

    if duplicate_count > 0:

        duplicate_rows = df[pk_duplicates]

        duplicate_rows.to_csv(
            EXPORTS_DIR / "duplicate_rows.csv",
            index=False
        )

        raise ValueError(
            f"Primary key duplicates found: "
            f"{duplicate_count}"
        )

    negative_users = (
        df["unique_users"] < 0
    ).sum()

    if negative_users > 0:

        raise ValueError(
            f"Negative users found: "
            f"{negative_users}"
        )

    logger.info(
        "Quality checks passed"
    )

# SAVE BACKUP

def save_backup(df):

    backup_file = (
        EXPORTS_DIR /
        "cleaned_comscore.csv"
    )

    df.to_csv(
        backup_file,
        index=False
    )

    logger.info(
        f"Backup saved: {backup_file}"
    )

# DATABASE

def get_engine():

    connection_string = (
        f"postgresql+psycopg2://"
        f"{DB_CONFIG['user']}:"
        f"{DB_CONFIG['password']}@"
        f"{DB_CONFIG['host']}:"
        f"{DB_CONFIG['port']}/"
        f"{DB_CONFIG['database']}"
    )

    return create_engine(connection_string)

# FULL REFRESH LOAD

def load_to_postgres(df):

    logger.info(
        "Starting PostgreSQL load"
    )

    engine = get_engine()

    with engine.begin() as conn:

        logger.info(
            "Truncating table"
        )

        conn.execute(
            text(
                "TRUNCATE TABLE comscore_data"
            )
        )

        logger.info(
            "Loading fresh data"
        )

        df.to_sql(
            "comscore_data",
            conn,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000
        )

    logger.info(
        f"Rows loaded: {len(df)}"
    )

# MAIN.

def main():

    logger.info("=" * 60)
    logger.info("ETL STARTED")
    logger.info("=" * 60)

    try:

        url = (
            "http://static.tv9hindi.com/comscore.csv"
        )

        df = fetch_csv(url)

        validate_schema(df)

        df = clean_data(df)

        df = convert_types(df)

        run_quality_checks(df)

        save_backup(df)

        load_to_postgres(df)

        logger.info("=" * 60)
        logger.info("ETL COMPLETED")
        logger.info("=" * 60)

    except Exception as e:

        logger.exception(
            f"ETL FAILED: {e}"
        )

        raise


if __name__ == "__main__":
    main()
