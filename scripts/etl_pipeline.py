# scripts/etl_pipeline.py
import sqlite3
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "db" / "bluestock_mf.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_DIR = BASE_DIR / "data" / "raw"

def build_database_infrastructure():
    print("Spawning structural database elements...")
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Establish base layout schemas via sqlite driver connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    with open(SCHEMA_PATH, 'r') as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database structural tables constructed cleanly.")

def populate_database_tables():
    print("Injecting tables into local storage tables...")
    engine = create_engine(f"sqlite:///{DB_PATH}")
    
    # 1. Populate dim_fund Lookup Table directly from master raw data list
    # Adjust filename to match whatever your provided master file path is named
    master_file = RAW_DIR / "fund_master.csv"
    if master_file.exists():
        df_master = pd.read_csv(master_file)
        df_master.columns = df_master.columns.str.lower().str.strip()
        df_master.to_sql('dim_fund', engine, if_exists='append', index=False)
        print("Added lookup indices into 'dim_fund'")

    # 2. Populate processed metrics fact data dataframes
    mappings = {
        'clean_nav.csv': 'fact_nav',
        'clean_transactions.csv': 'fact_transactions',
        'clean_performance.csv': 'fact_performance'
    }
    
    for filename, table_name in mappings.items():
        file_path = PROCESSED_DIR / filename
        if file_path.exists():
            df = pd.read_csv(file_path)
            # Match date column types to string formats compatible with SQLite
            for col in df.columns:
                if 'date' in col:
                    df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
            df.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"Injected rows from {filename} into database table '{table_name}'")

if __name__ == "__main__":
    build_database_infrastructure()
    populate_database_tables()
    print("\nDay 2 Database Initialization Complete!")