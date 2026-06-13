# ==========================================
# LOAD CLEAN DATA TO POSTGRESQL WAREHOUSE
# File: etl/03_load_to_warehouse.py
# ==========================================

import pandas as pd
from sqlalchemy import create_engine

# ==========================================
# POSTGRESQL CONNECTION
# ==========================================

DB_USER = "postgres"
DB_PASSWORD = "harshith123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nifty100warehouse"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("✅ PostgreSQL Connected")

# ==========================================
# LOAD CLEAN CSV FILES
# ==========================================

company_df = pd.read_csv("data/clean/clean_companies.csv")
balance_df = pd.read_csv("data/clean/clean_balance_sheet.csv")
cashflow_df = pd.read_csv("data/clean/clean_cashflow.csv")
profit_df = pd.read_csv("data/clean/clean_profit_loss.csv")
analysis_df = pd.read_csv("data/clean/clean_analysis.csv")

# ==========================================
# CLEAN COLUMN NAMES
# ==========================================

for df in [
    company_df,
    balance_df,
    cashflow_df,
    profit_df,
    analysis_df
]:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

# ==========================================
# FIX COLUMN NAMES
# ==========================================

# ---- COMPANY TABLE ----

company_df.rename(columns={
    "company_id": "symbol",
    "name": "company_name"
}, inplace=True)

# ---- PROFIT LOSS TABLE ----

profit_df.rename(columns={
    "company_id": "symbol",
    "sales_cr": "sales",
    "net_profit_cr": "net_profit",
    "profit_after_tax": "net_profit"
}, inplace=True)

# ---- BALANCE SHEET TABLE ----

balance_df.rename(columns={
    "company_id": "symbol"
}, inplace=True)

# ---- CASHFLOW TABLE ----

cashflow_df.rename(columns={
    "company_id": "symbol",
    "net_cash_flow": "free_cash_flow"
}, inplace=True)

# ==========================================
# ADD MISSING COLUMNS IF NOT EXISTS
# ==========================================

# ---- COMPANY TABLE ----

required_company_cols = [
    "symbol",
    "company_name",
    "sector"
]

for col in required_company_cols:
    if col not in company_df.columns:
        company_df[col] = "Unknown"

# ---- PROFIT TABLE ----

required_profit_cols = [
    "symbol",
    "year",
    "sales",
    "net_profit"
]

for col in required_profit_cols:
    if col not in profit_df.columns:
        profit_df[col] = 0

# ---- BALANCE TABLE ----

required_balance_cols = [
    "symbol",
    "year",
    "equity_capital",
    "reserves",
    "borrowings",
    "total_assets",
    "debt_to_equity",
    "equity_ratio"
]

for col in required_balance_cols:
    if col not in balance_df.columns:
        balance_df[col] = 0

# ---- CASHFLOW TABLE ----

required_cashflow_cols = [
    "symbol",
    "year",
    "operating_activity",
    "investing_activity",
    "financing_activity",
    "free_cash_flow"
]

for col in required_cashflow_cols:
    if col not in cashflow_df.columns:
        cashflow_df[col] = 0

# ==========================================
# REMOVE DUPLICATES
# ==========================================

company_df = company_df.drop_duplicates()

profit_df = profit_df.drop_duplicates()

balance_df = balance_df.drop_duplicates()

cashflow_df = cashflow_df.drop_duplicates()

analysis_df = analysis_df.drop_duplicates()

# ==========================================
# FILL NULL VALUES
# ==========================================

company_df = company_df.fillna("Unknown")

profit_df = profit_df.fillna(0)

balance_df = balance_df.fillna(0)

cashflow_df = cashflow_df.fillna(0)

analysis_df = analysis_df.fillna(0)

# ==========================================
# SELECT REQUIRED COLUMNS
# ==========================================

company_df = company_df[
    [
        "symbol",
        "company_name",
        "sector"
    ]
]

profit_df = profit_df[
    [
        "symbol",
        "year",
        "sales",
        "net_profit"
    ]
]

balance_df = balance_df[
    [
        "symbol",
        "year",
        "equity_capital",
        "reserves",
        "borrowings",
        "total_assets",
        "debt_to_equity",
        "equity_ratio"
    ]
]

cashflow_df = cashflow_df[
    [
        "symbol",
        "year",
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "free_cash_flow"
    ]
]

# ==========================================
# LOAD TO POSTGRESQL
# ==========================================

company_df.to_sql(
    "dim_company",
    engine,
    if_exists="replace",
    index=False
)

print("✅ Loaded dim_company")

profit_df.to_sql(
    "fact_profit_loss",
    engine,
    if_exists="replace",
    index=False
)

print("✅ Loaded fact_profit_loss")

balance_df.to_sql(
    "fact_balance_sheet",
    engine,
    if_exists="replace",
    index=False
)

print("✅ Loaded fact_balance_sheet")

cashflow_df.to_sql(
    "fact_cash_flow",
    engine,
    if_exists="replace",
    index=False
)

print("✅ Loaded fact_cash_flow")

analysis_df.to_sql(
    "fact_analysis",
    engine,
    if_exists="replace",
    index=False
)

print("✅ Loaded fact_analysis")

# ==========================================
# SUCCESS MESSAGE
# ==========================================

print("\n🎉 ALL TABLES LOADED SUCCESSFULLY")
print("✅ Warehouse Ready")