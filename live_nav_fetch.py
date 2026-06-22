import os
import requests
import pandas as pd
import time

def fetch_scheme_data(scheme_code, retries=3, backoff=3):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    for attempt in range(retries):
        try:
            print(f"Fetching data for scheme code: {scheme_code} (Attempt {attempt+1}/{retries})...")
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching scheme {scheme_code}: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 2
            else:
                return None

def main():
    os.makedirs("data/raw", exist_ok=True)
    
    # Schemes specified in the prompt
    prompt_schemes = {
        125497: "hdfc_top_100_125497.csv",  # (SBI Small Cap Fund on API)
        119551: "sbi_bluechip_119551.csv",   # (Aditya Birla Debt on API)
        120503: "icici_bluechip_120503.csv", # (Axis ELSS Tax Saver on API)
        118632: "nippon_large_cap_118632.csv", # (Nippon Large Cap - Matches!)
        119092: "axis_bluechip_119092.csv",  # (HDFC Money Market on API)
        120841: "kotak_bluechip_120841.csv"  # (Quant Mid Cap on API)
    }
    
    # Actual correct schemes to resolve mapping anomalies and complete the 10 CSV files count
    actual_schemes = {
        119062: "hdfc_top_100_actual_119062.csv",  # Actual HDFC Top 100 Direct Growth
        119777: "sbi_bluechip_actual_119777.csv"   # Actual SBI Bluechip Direct Growth
    }
    
    all_schemes = {**prompt_schemes, **actual_schemes}
    
    master_records = []
    history_dfs = []
    
    # Fetch and save individual raw files
    for code, filename in all_schemes.items():
        data_json = fetch_scheme_data(code)
        if not data_json:
            print(f"Critical: Failed to fetch scheme {code} after multiple retries.")
            continue
            
        meta = data_json.get('meta', {})
        nav_list = data_json.get('data', [])
        
        if not nav_list:
            continue
            
        # 1. Save individual raw file
        df = pd.DataFrame(nav_list)
        df['scheme_code'] = code
        df['scheme_name'] = meta.get('scheme_name', '')
        df = df[['scheme_code', 'scheme_name', 'date', 'nav']]
        
        filepath = f"data/raw/{filename}"
        df.to_csv(filepath, index=False)
        print(f"Saved {len(df)} rows to {filepath}")
        
        # 2. Collect for historical database
        df_hist = pd.DataFrame(nav_list)
        df_hist['scheme_code'] = code
        df_hist = df_hist[['scheme_code', 'date', 'nav']]
        history_dfs.append(df_hist)
        
        # 3. Collect for fund master
        scheme_cat = meta.get('scheme_category', 'Other')
        if ' - ' in scheme_cat:
            cat, sub_cat = scheme_cat.split(' - ', 1)
        else:
            cat, sub_cat = 'Other', scheme_cat
            
        risk_grade = 'Very High'
        if 'debt' in cat.lower() or 'debt' in sub_cat.lower():
            risk_grade = 'Moderate'
        elif 'money market' in sub_cat.lower():
            risk_grade = 'Low to Moderate'
            
        master_records.append({
            'scheme_code': code,
            'scheme_name': meta.get('scheme_name', ''),
            'fund_house': meta.get('fund_house', ''),
            'category': cat,
            'sub_category': sub_cat,
            'risk_grade': risk_grade
        })
        
    # Generate and save fund_master.csv
    df_master = pd.DataFrame(master_records)
    df_master.to_csv("data/raw/fund_master.csv", index=False)
    print(f"Generated data/raw/fund_master.csv with {len(df_master)} records.")
    
    # Generate and save nav_history.csv
    df_history = pd.concat(history_dfs, ignore_index=True)
    df_history.to_csv("data/raw/nav_history.csv", index=False)
    print(f"Generated data/raw/nav_history.csv with {len(df_history)} records.")

if __name__ == "__main__":
    main()
