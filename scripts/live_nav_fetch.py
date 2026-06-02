import requests
import pandas as pd
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

# A list of the specific mutual fund ID codes you were asked to fetch
FUNDS_TO_FETCH = {
    125497: "HDFC_Top_100_Direct",
    119551: "SBI_Bluechip",
    120503: "ICICI_Bluechip",
    118632: "Nippon_Large_Cap",
    119092: "Axis_Bluechip",
    120841: "Kotak_Bluechip"
}

def fetch_internet_data():
    print("📡 Starting API connection to mfapi.in...")
    
    for code, fund_name in FUNDS_TO_FETCH.items():
        # The web link to fetch data for this specific fund code
        url = f"https://api.mfapi.in/mf/{code}"
        print(f"Fetching updates for {fund_name} (Code: {code})...")
        
        try:
            response = requests.get(url, timeout=10)
            
            # If the web request succeeds (Status 200 means OK)
            if response.status_code == 200:
                json_data = response.json()
                nav_records = json_data.get('data', [])
                
                # Turn the web data into a spreadsheet matrix
                df = pd.DataFrame(nav_records)
                
                # Add extra columns so we know which fund this data belongs to
                df['scheme_code'] = code
                df['scheme_name'] = fund_name
                
                # Rearrange columns beautifully
                df = df[['scheme_code', 'scheme_name', 'date', 'nav']]
                
                # Save it as a raw CSV file
                output_file = RAW_DIR / f"api_nav_{code}.csv"
                df.to_csv(output_file, index=False)
                print(f"Saved {len(df)} rows to {output_file.name}")
            else:
                print(f"Could not download data for code {code}. Error code: {response.status_code}")
                
        except Exception as e:
            print(f"An error occurred with connection: {e}")
            
        # Wait 1 second before asking for the next file so the website doesn't block us
        time.sleep(1)

if __name__ == "__main__":
    fetch_internet_data()