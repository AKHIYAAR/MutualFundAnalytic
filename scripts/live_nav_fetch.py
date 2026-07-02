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
    # Resolve paths relative to project root
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    raw_dir = os.path.join(base_dir, 'Data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    
    master_path = os.path.join(raw_dir, 'fund_master.csv')
    if os.path.exists(master_path):
        try:
            df_m = pd.read_csv(master_path)
            if len(df_m) >= 40:
                print("Expanded dataset of 40 schemes detected in Data/raw/fund_master.csv.")
                print("Skipping live API fetch to preserve 2022-2026 synchronized market cycle simulation.")
                return
        except Exception as e:
            print(f"Error checking fund_master.csv: {e}")
    
    prompt_schemes = {
        125497: "hdfc_top_100_125497.csv",
        119551: "sbi_bluechip_119551.csv",
        120503: "icici_bluechip_120503.csv",
        118632: "nippon_large_cap_118632.csv",
        119092: "axis_bluechip_119092.csv",
        120841: "kotak_bluechip_120841.csv"
    }
    
    actual_schemes = {
        119062: "hdfc_top_100_actual_119062.csv",
        119777: "sbi_bluechip_actual_119777.csv"
    }
    
    all_schemes = {**prompt_schemes, **actual_schemes}
    
    master_records = []
    history_dfs = []
    
    for code, filename in all_schemes.items():
        data_json = fetch_scheme_data(code)
        if not data_json:
            print(f"Critical: Failed to fetch scheme {code} after multiple retries.")
            continue
            
        meta = data_json.get('meta', {})
        nav_list = data_json.get('data', [])
        
        if not nav_list:
            continue
            
        df = pd.DataFrame(nav_list)
        df['scheme_code'] = code
        df['scheme_name'] = meta.get('scheme_name', '')
        df = df[['scheme_code', 'scheme_name', 'date', 'nav']]
        
        filepath = os.path.join(raw_dir, filename)
        df.to_csv(filepath, index=False)
        print(f"Saved {len(df)} rows to {filepath}")
        
        df_hist = pd.DataFrame(nav_list)
        df_hist['scheme_code'] = code
        df_hist = df_hist[['scheme_code', 'date', 'nav']]
        history_dfs.append(df_hist)
        
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
        
    df_master = pd.DataFrame(master_records)
    df_master.to_csv(master_path, index=False)
    print(f"Generated Data/raw/fund_master.csv with {len(df_master)} records.")
    
    df_history = pd.concat(history_dfs, ignore_index=True)
    history_path = os.path.join(raw_dir, 'nav_history.csv')
    df_history.to_csv(history_path, index=False)
    print(f"Generated Data/raw/nav_history.csv with {len(df_history)} records.")

if __name__ == "__main__":
    main()
