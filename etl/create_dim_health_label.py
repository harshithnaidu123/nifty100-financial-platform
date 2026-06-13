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

labels = pd.DataFrame({
    "label_name": [
        "EXCELLENT",
        "GOOD",
        "AVERAGE",
        "WEAK",
        "POOR"
    ]
})

labels.to_sql(
    "dim_health_label",
    engine,
    if_exists="replace",
    index=False
)

print("✅ dim_health_label created")