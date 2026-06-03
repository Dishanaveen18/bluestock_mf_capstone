import os
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def clean_nav_data():
    print("🧹 Cleaning nav_history data...")
    # Update filename if your raw historical data file uses a different title
    file_path = RAW_DIR / "nav_history.csv"
    if not file_path.exists():
        print("nav_history.csv not found in data/raw. Skipping.")
        return

    df = pd.read_csv(file_path)
    
    # 1. Standardize column names and parse dates
    df.columns = df.columns.str.lower().str.strip()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date', 'amfi_code'])
    df['amfi_code'] = df['amfi_code'].astype(int)
    df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
    
    # Drop records where NAV is zero or negative
    df = df[df['nav'] > 0]
    
    # 2. Reindex and Forward Fill (ffill) to handle weekends/holidays per fund
    cleaned_frames = []
    for amfi, group in df.groupby('amfi_code'):
        group = group.drop_duplicates(subset=['date']).set_index('date').sort_index()
        
        # Generate full unbroken calendar range
        full_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq='D')
        group = group.reindex(full_range)
        
        # Repair column gaps using forward-fill
        group['nav'] = group['nav'].ffill()
        group['amfi_code'] = group['amfi_code'].ffill().astype(int)
        
        # Calculate daily return metric required by rubric
        group['daily_return'] = group['nav'].pct_change().fillna(0)
        
        group = group.reset_index().rename(columns={'index': 'nav_date'})
        cleaned_frames.append(group)
        
    final_nav = pd.concat(cleaned_frames, ignore_index=True)
    final_nav.to_csv(PROCESSED_DIR / "clean_nav.csv", index=False)
    print(f"Successfully created clean_nav.csv with {len(final_nav)} records.")

def clean_transaction_data():
    print("🧹 Cleaning investor_transactions data...")
    file_path = RAW_DIR / "investor_transactions.csv"
    if not file_path.exists():
        print("investor_transactions.csv not found. Skipping.")
        return
        
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower().str.strip()
    
    # Standardize string categories
    if 'transaction_type' in df.columns:
        df['transaction_type'] = df['transaction_type'].str.upper().str.strip()
        
    # Validate mathematical logic rules
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df[df['amount'] > 0]
    
    if 'date' in df.columns:
        df['transaction_date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.drop(columns=['date'])
        
    df.to_csv(PROCESSED_DIR / "clean_transactions.csv", index=False)
    print("Successfully generated clean_transactions.csv")

def clean_performance_data():
    print("Cleaning scheme_performance data...")
    file_path = RAW_DIR / "scheme_performance.csv"
    if not file_path.exists():
        print(" scheme_performance.csv not found. Skipping.")
        return
        
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower().str.strip()
    
    # Rule validation logic
    df['sharpe_ratio'] = pd.to_numeric(df['sharpe_ratio'], errors='coerce')
    df['negative_sharpe_flag'] = np.where(df['sharpe_ratio'] < 0, 1, 0)
    
    df.to_csv(PROCESSED_DIR / "clean_performance.csv", index=False)
    print("Successfully generated clean_performance.csv")

if __name__ == "__main__":
    clean_nav_data()
    clean_transaction_data()
    clean_performance_data()