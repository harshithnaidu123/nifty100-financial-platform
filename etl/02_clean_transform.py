# ==============================
# CLEAN CASH FLOW DATA
# ==============================

import pandas as pd

# Load raw cashflow CSV
cashflow_df = pd.read_csv("data/raw/cashflow.csv")

# Clean column names
cashflow_df.columns = [
    col.strip().lower().replace(" ", "_")
    for col in cashflow_df.columns
]

print("\n==== CASHFLOW COLUMNS ====\n")
print(cashflow_df.columns.tolist())

# ==============================
# AUTO-DETECT COLUMN NAMES
# ==============================

# Detect operating activity column
operating_col = next(
    (
        col for col in cashflow_df.columns
        if "operating" in col
    ),
    None
)

# Detect investing activity column
investing_col = next(
    (
        col for col in cashflow_df.columns
        if "investing" in col
    ),
    None
)

# Detect financing activity column
financing_col = next(
    (
        col for col in cashflow_df.columns
        if "financing" in col
    ),
    None
)

# Detect free cash flow column
free_cash_col = next(
    (
        col for col in cashflow_df.columns
        if "net_cash" in col
        or "free_cash" in col
    ),
    None
)

# Rename detected columns
rename_dict = {}

if operating_col:
    rename_dict[operating_col] = "operating_activity"

if investing_col:
    rename_dict[investing_col] = "investing_activity"

if financing_col:
    rename_dict[financing_col] = "financing_activity"

if free_cash_col:
    rename_dict[free_cash_col] = "free_cash_flow"

cashflow_df.rename(columns=rename_dict, inplace=True)

# ==============================
# NUMERIC CLEANING
# ==============================

cashflow_numeric_cols = [
    "operating_activity",
    "investing_activity",
    "financing_activity",
    "free_cash_flow"
]

for col in cashflow_numeric_cols:

    if col in cashflow_df.columns:

        cashflow_df[col] = (
            cashflow_df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False)
            .str.replace("--", "", regex=False)
            .str.replace("Cr.", "", regex=False)
            .str.strip()
        )

        cashflow_df[col] = pd.to_numeric(
            cashflow_df[col],
            errors="coerce"
        )

# Fill missing values
cashflow_df = cashflow_df.fillna(0)

# Remove duplicates
cashflow_df = cashflow_df.drop_duplicates()

# Save cleaned file
cashflow_df.to_csv(
    "data/clean/clean_cashflow.csv",
    index=False
)

print("\n✅ Clean cashflow data saved successfully")
print(cashflow_df.head())