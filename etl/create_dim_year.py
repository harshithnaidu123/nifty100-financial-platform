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

# Load profit loss data
df = pd.read_csv("data/clean/clean_profit_loss.csv")

# Clean columns
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Create year table
year_df = df[["year"]].drop_duplicates()

# Add year_id
year_df["year_id"] = range(1, len(year_df) + 1)

# Reorder columns
year_df = year_df[["year_id", "year"]]

# Save
year_df.to_sql(
    "dim_year",
    engine,
    if_exists="replace",
    index=False
)

print("✅ dim_year created successfully")