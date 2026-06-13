import pandas as pd
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
# LOAD COMPANY DATA
# ==========================================

df = pd.read_csv("data/clean/clean_companies.csv")

# ==========================================
# CLEAN COLUMN NAMES
# ==========================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# ==========================================
# FIX COLUMN NAMES
# ==========================================

df.rename(columns={
    "company_id": "symbol"
}, inplace=True)

# ==========================================
# CREATE PROS & CONS
# ==========================================

pros_cons = []

for symbol in df["symbol"]:

    # PROS
    pros_cons.append({
        "symbol": symbol,
        "category": "Profitability",
        "text": "Strong profit growth over recent years",
        "is_pro": True
    })

    pros_cons.append({
        "symbol": symbol,
        "category": "Cash Flow",
        "text": "Healthy operating cash flow",
        "is_pro": True
    })

    # CONS
    pros_cons.append({
        "symbol": symbol,
        "category": "Debt",
        "text": "Debt levels should be monitored carefully",
        "is_pro": False
    })

    pros_cons.append({
        "symbol": symbol,
        "category": "Growth",
        "text": "Revenue growth fluctuates in some years",
        "is_pro": False
    })

# ==========================================
# CREATE DATAFRAME
# ==========================================

pros_cons_df = pd.DataFrame(pros_cons)

# ==========================================
# SAVE TO POSTGRESQL
# ==========================================

pros_cons_df.to_sql(
    "fact_pros_cons",
    engine,
    if_exists="replace",
    index=False
)

print("✅ fact_pros_cons created successfully")