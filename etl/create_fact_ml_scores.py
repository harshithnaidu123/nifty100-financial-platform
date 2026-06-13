import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# ==========================================
# DATABASE CONNECTION
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
# LOAD DATA
# ==========================================

profit_df = pd.read_csv("data/clean/clean_profit_loss.csv")
balance_df = pd.read_csv("data/clean/clean_balance_sheet.csv")
cashflow_df = pd.read_csv("data/clean/clean_cashflow.csv")

# ==========================================
# CLEAN COLUMN NAMES
# ==========================================

for df in [profit_df, balance_df, cashflow_df]:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

# ==========================================
# FIX COLUMN NAMES
# ==========================================

profit_df.rename(columns={
    "company_id": "symbol",
    "sales_cr": "sales",
    "net_profit_cr": "net_profit"
}, inplace=True)

balance_df.rename(columns={
    "company_id": "symbol"
}, inplace=True)

cashflow_df.rename(columns={
    "company_id": "symbol",
    "net_cash_flow": "free_cash_flow"
}, inplace=True)

# ==========================================
# REQUIRED COLUMNS
# ==========================================

required_profit = ["symbol", "sales", "net_profit"]

required_balance = [
    "symbol",
    "borrowings",
    "debt_to_equity"
]

required_cashflow = [
    "symbol",
    "operating_activity",
    "free_cash_flow"
]

for col in required_profit:
    if col not in profit_df.columns:
        profit_df[col] = 0

for col in required_balance:
    if col not in balance_df.columns:
        balance_df[col] = 0

for col in required_cashflow:
    if col not in cashflow_df.columns:
        cashflow_df[col] = 0

# ==========================================
# GROUP DATA
# ==========================================

profit_group = profit_df.groupby("symbol").agg({
    "sales": "mean",
    "net_profit": "mean"
}).reset_index()

balance_group = balance_df.groupby("symbol").agg({
    "borrowings": "mean",
    "debt_to_equity": "mean"
}).reset_index()

cashflow_group = cashflow_df.groupby("symbol").agg({
    "operating_activity": "mean",
    "free_cash_flow": "mean"
}).reset_index()

# ==========================================
# MERGE TABLES
# ==========================================

ml_df = profit_group.merge(
    balance_group,
    on="symbol",
    how="left"
)

ml_df = ml_df.merge(
    cashflow_group,
    on="symbol",
    how="left"
)

# ==========================================
# FILL NULLS
# ==========================================

ml_df.fillna(0, inplace=True)

# ==========================================
# CREATE HEALTH SCORE
# ==========================================

ml_df["overall_score"] = (
    (
        ml_df["net_profit"].rank(pct=True) * 30
    ) +
    (
        ml_df["sales"].rank(pct=True) * 25
    ) +
    (
        (1 - ml_df["debt_to_equity"].rank(pct=True)) * 25
    ) +
    (
        ml_df["free_cash_flow"].rank(pct=True) * 20
    )
)

# Convert to 0-100
ml_df["overall_score"] = ml_df["overall_score"].round(2)

# ==========================================
# CREATE HEALTH LABELS
# ==========================================

def health_label(score):

    if score >= 85:
        return "EXCELLENT"

    elif score >= 70:
        return "GOOD"

    elif score >= 50:
        return "AVERAGE"

    elif score >= 35:
        return "WEAK"

    else:
        return "POOR"

ml_df["health_label"] = ml_df["overall_score"].apply(health_label)

# ==========================================
# FINAL COLUMNS
# ==========================================

ml_df = ml_df[
    [
        "symbol",
        "overall_score",
        "health_label"
    ]
]

# ==========================================
# SAVE TO POSTGRESQL
# ==========================================

ml_df.to_sql(
    "fact_ml_scores",
    engine,
    if_exists="replace",
    index=False
)

print("✅ fact_ml_scores created successfully")