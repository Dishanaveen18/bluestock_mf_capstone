import os
import pandas as pd
from pathlib import Path

# This automatically finds where your project is sitting on your computer
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

def scan_raw_data():
    # Look inside data/raw and find all CSV files
    all_files = [f for f in os.listdir(RAW_DIR) if f.endswith('.csv')]
    
    if not all_files:
        print("No CSV files found! Please move your 10 raw CSV files into data/raw/")
        return

    print(f" Found {len(all_files)} files in data/raw/. Let's check them:\n")

    for file_name in all_files:
        file_path = RAW_DIR / file_name
        print(f"=== Analyzing File: {file_name} ===")
        
        # Load the file into a Pandas DataFrame table
        df = pd.read_csv(file_path)
        
        # 1. Print Shape (Rows and Columns)
        print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # 2. Print Column Names and Data Types
        print("\nData Types (.dtypes):")
        print(df.dtypes)
        
        # 3. Print the first 3 rows of data
        print("\nFirst few rows (.head()):")
        print(df.head(3))
        
        # 4. Check for obvious mistakes or empty missing spots
        missing_values = df.isnull().sum().sum()
        if missing_values > 0:
            print(f"Warning: This file has {missing_values} missing blank spaces!")
        else:
            print("Data looks structurally complete.")
            
        print("-" * 50 + "\n")

if __name__ == "__main__":
    scan_raw_data()