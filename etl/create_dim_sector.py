import pandas as pd
from sqlalchemy import create_engine

DB_USER = "postgres"
DB_PASSWORD = "harshith123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nifty100warehouse"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Load companies data
df = pd.read_csv("data/clean/clean_companies.csv")

# Clean columns
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Keep only sector
sector_df = df[["sector"]].drop_duplicates()

# Rename column
sector_df.rename(columns={
    "sector": "sector_name"
}, inplace=True)

# Remove nulls
sector_df = sector_df.dropna()

# Save to PostgreSQL
sector_df.to_sql(
    "dim_sector",
    engine,
    if_exists="replace",
    index=False
)

print("✅ dim_sector created successfully")