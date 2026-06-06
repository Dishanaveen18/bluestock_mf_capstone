# scripts/etl_pipeline.py
import os
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text

# 1. Setup paths relative to your project layout
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "bluestock_mf.db"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "schema.sql"

engine = create_engine(f"sqlite:///{DB_PATH}")

print("--- 🛠️ Initializing Schema Setup via Python Engine ---")

# 2. Read the raw schema.sql file content directly using Python
if SCHEMA_PATH.exists():
    with open(SCHEMA_PATH, 'r') as file:
        schema_sql = file.read()
    
    # Execute the raw SQL schema statements inside your database file safely
    with engine.connect() as conn:
        # SQLite allows executing multiple statements if split correctly
        for statement in schema_sql.split(';'):
            clean_statement = statement.strip()
            if clean_statement:
                conn.execute(text(clean_statement))
        conn.commit()
    print(" ✅ Database tables dropped and recreated cleanly from sql/schema.sql")
else:
    print(f"❌ ERROR: Cannot find schema file at {SCHEMA_PATH.resolve()}")

# --- Your existing pandas dataframe loading code follows below ---
# df_nav = pd.read_csv(PROJECT_ROOT / "data/processed/clean_nav.csv")
# df_nav.to_sql('fact_nav', engine, if_exists='append', index=False)