import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def main():
    random.seed(42)
    np.random.seed(42)

    raw_dir = "Data/raw"
    os.makedirs(raw_dir, exist_ok=True)

    print("--- 1. Generating Expanded Fund Master (40 Schemes) ---")
    
    # Original 8 schemes
    original_schemes = [
        {"scheme_code": 125497, "scheme_name": "SBI Small Cap Fund - Direct Plan - Growth", "fund_house": "SBI Mutual Fund", "category": "Equity Scheme", "sub_category": "Small Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 119551, "scheme_name": "Aditya Birla Sun Life Banking & PSU Debt Fund  - DIRECT - IDCW", "fund_house": "Aditya Birla Sun Life Mutual Fund", "category": "Debt Scheme", "sub_category": "Banking and PSU Fund", "risk_grade": "Moderate"},
        {"scheme_code": 120503, "scheme_name": "Axis ELSS Tax Saver Fund - Direct Plan - Growth Option", "fund_house": "Axis Mutual Fund", "category": "Equity Scheme", "sub_category": "ELSS", "risk_grade": "Very High"},
        {"scheme_code": 118632, "scheme_name": "Nippon India Large Cap Fund - Direct Plan Growth Plan - Growth Option", "fund_house": "Nippon India Mutual Fund", "category": "Equity Scheme", "sub_category": "Large Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 119092, "scheme_name": "HDFC Money Market Fund - Growth Option - Direct Plan", "fund_house": "HDFC Mutual Fund", "category": "Debt Scheme", "sub_category": "Money Market Fund", "risk_grade": "Moderate"},
        {"scheme_code": 120841, "scheme_name": "quant Mid Cap Fund - Growth Option - Direct Plan", "fund_house": "quant Mutual Fund", "category": "Equity Scheme", "sub_category": "Mid Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 119062, "scheme_name": "HDFC Hybrid Equity Fund - Growth Option - Direct Plan", "fund_house": "HDFC Mutual Fund", "category": "Hybrid Scheme", "sub_category": "Aggressive Hybrid Fund", "risk_grade": "Very High"},
        {"scheme_code": 119777, "scheme_name": "Kotak Multi Asset Omni FOF - Direct Growth - Direct", "fund_house": "Kotak Mahindra Mutual Fund", "category": "Other Scheme", "sub_category": "FoF Domestic", "risk_grade": "Very High"},
    ]

    # Additional 32 schemes to make it exactly 40
    new_schemes_info = [
        # SBI
        {"scheme_code": 120101, "scheme_name": "SBI Bluechip Fund - Direct Plan - Growth", "fund_house": "SBI Mutual Fund", "category": "Equity Scheme", "sub_category": "Large Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120102, "scheme_name": "SBI Contra Fund - Direct Plan - Growth", "fund_house": "SBI Mutual Fund", "category": "Equity Scheme", "sub_category": "Contra Fund", "risk_grade": "Very High"},
        {"scheme_code": 120103, "scheme_name": "SBI Magnum Midcap Fund - Direct Plan - Growth", "fund_house": "SBI Mutual Fund", "category": "Equity Scheme", "sub_category": "Mid Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120104, "scheme_name": "SBI Equity Hybrid Fund - Direct Plan - Growth", "fund_house": "SBI Mutual Fund", "category": "Hybrid Scheme", "sub_category": "Aggressive Hybrid Fund", "risk_grade": "Very High"},
        {"scheme_code": 120105, "scheme_name": "SBI Liquid Fund - Direct Plan - Growth", "fund_house": "SBI Mutual Fund", "category": "Debt Scheme", "sub_category": "Liquid Fund", "risk_grade": "Low"},
        {"scheme_code": 120106, "scheme_name": "SBI Arbitrage Opportunities Fund - Direct Plan - Growth", "fund_house": "SBI Mutual Fund", "category": "Hybrid Scheme", "sub_category": "Arbitrage Fund", "risk_grade": "Low"},
        # HDFC
        {"scheme_code": 120107, "scheme_name": "HDFC Top 100 Fund - Direct Plan - Growth", "fund_house": "HDFC Mutual Fund", "category": "Equity Scheme", "sub_category": "Large Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120108, "scheme_name": "HDFC Mid-Cap Opportunities Fund - Direct Plan - Growth", "fund_house": "HDFC Mutual Fund", "category": "Equity Scheme", "sub_category": "Mid Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120109, "scheme_name": "HDFC Small Cap Fund - Direct Plan - Growth", "fund_house": "HDFC Mutual Fund", "category": "Equity Scheme", "sub_category": "Small Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120110, "scheme_name": "HDFC Balanced Advantage Fund - Direct Plan - Growth", "fund_house": "HDFC Mutual Fund", "category": "Hybrid Scheme", "sub_category": "Balanced Advantage Fund", "risk_grade": "Very High"},
        {"scheme_code": 120111, "scheme_name": "HDFC Liquid Fund - Direct Plan - Growth", "fund_house": "HDFC Mutual Fund", "category": "Debt Scheme", "sub_category": "Liquid Fund", "risk_grade": "Low"},
        # ICICI Prudential
        {"scheme_code": 120112, "scheme_name": "ICICI Prudential Bluechip Fund - Direct Plan - Growth", "fund_house": "ICICI Prudential Mutual Fund", "category": "Equity Scheme", "sub_category": "Large Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120113, "scheme_name": "ICICI Prudential Midcap Fund - Direct Plan - Growth", "fund_house": "ICICI Prudential Mutual Fund", "category": "Equity Scheme", "sub_category": "Mid Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120114, "scheme_name": "ICICI Prudential Smallcap Fund - Direct Plan - Growth", "fund_house": "ICICI Prudential Mutual Fund", "category": "Equity Scheme", "sub_category": "Small Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120115, "scheme_name": "ICICI Prudential Asset Allocator FoF - Direct Plan - Growth", "fund_house": "ICICI Prudential Mutual Fund", "category": "Other Scheme", "sub_category": "FoF Domestic", "risk_grade": "High"},
        {"scheme_code": 120116, "scheme_name": "ICICI Prudential Equity & Debt Fund - Direct Plan - Growth", "fund_house": "ICICI Prudential Mutual Fund", "category": "Hybrid Scheme", "sub_category": "Aggressive Hybrid Fund", "risk_grade": "Very High"},
        {"scheme_code": 120117, "scheme_name": "ICICI Prudential Liquid Fund - Direct Plan - Growth", "fund_house": "ICICI Prudential Mutual Fund", "category": "Debt Scheme", "sub_category": "Liquid Fund", "risk_grade": "Low"},
        # Nippon
        {"scheme_code": 120118, "scheme_name": "Nippon India Small Cap Fund - Direct Plan - Growth", "fund_house": "Nippon India Mutual Fund", "category": "Equity Scheme", "sub_category": "Small Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120119, "scheme_name": "Nippon India Growth Fund - Direct Plan - Growth", "fund_house": "Nippon India Mutual Fund", "category": "Equity Scheme", "sub_category": "Mid Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120120, "scheme_name": "Nippon India Arbitrage Fund - Direct Plan - Growth", "fund_house": "Nippon India Mutual Fund", "category": "Hybrid Scheme", "sub_category": "Arbitrage Fund", "risk_grade": "Low"},
        # Axis
        {"scheme_code": 120121, "scheme_name": "Axis Bluechip Fund - Direct Plan - Growth", "fund_house": "Axis Mutual Fund", "category": "Equity Scheme", "sub_category": "Large Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120122, "scheme_name": "Axis Midcap Fund - Direct Plan - Growth", "fund_house": "Axis Mutual Fund", "category": "Equity Scheme", "sub_category": "Mid Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120123, "scheme_name": "Axis Small Cap Fund - Direct Plan - Growth", "fund_house": "Axis Mutual Fund", "category": "Equity Scheme", "sub_category": "Small Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120124, "scheme_name": "Axis Liquid Fund - Direct Plan - Growth", "fund_house": "Axis Mutual Fund", "category": "Debt Scheme", "sub_category": "Liquid Fund", "risk_grade": "Low"},
        # Kotak
        {"scheme_code": 120125, "scheme_name": "Kotak Bluechip Fund - Direct Plan - Growth", "fund_house": "Kotak Mahindra Mutual Fund", "category": "Equity Scheme", "sub_category": "Large Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120126, "scheme_name": "Kotak Emerging Equity Fund - Direct Plan - Growth", "fund_house": "Kotak Mahindra Mutual Fund", "category": "Equity Scheme", "sub_category": "Mid Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120127, "scheme_name": "Kotak Small Cap Fund - Direct Plan - Growth", "fund_house": "Kotak Mahindra Mutual Fund", "category": "Equity Scheme", "sub_category": "Small Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120128, "scheme_name": "Kotak Liquid Fund - Direct Plan - Growth", "fund_house": "Kotak Mahindra Mutual Fund", "category": "Debt Scheme", "sub_category": "Liquid Fund", "risk_grade": "Low"},
        # quant
        {"scheme_code": 120129, "scheme_name": "quant Active Fund - Direct Plan - Growth", "fund_house": "quant Mutual Fund", "category": "Equity Scheme", "sub_category": "Multi Cap Fund", "risk_grade": "Very High"},
        {"scheme_code": 120130, "scheme_name": "quant Small Cap Fund - Direct Plan - Growth", "fund_house": "quant Mutual Fund", "category": "Equity Scheme", "sub_category": "Small Cap Fund", "risk_grade": "Very High"},
        # ABSL
        {"scheme_code": 120131, "scheme_name": "Aditya Birla Sun Life Frontline Equity Fund - Direct Plan - Growth", "fund_house": "Aditya Birla Sun Life Mutual Fund", "category": "Equity Scheme", "sub_category": "Large Cap Fund", "risk_grade": "Very High"},
        # Tata
        {"scheme_code": 120132, "scheme_name": "Tata Digital India Fund - Direct Plan - Growth", "fund_house": "Tata Mutual Fund", "category": "Equity Scheme", "sub_category": "Sectoral/Thematic Fund", "risk_grade": "Very High"}
    ]

    all_schemes = original_schemes + new_schemes_info
    df_master = pd.DataFrame(all_schemes)
    df_master.to_csv(os.path.join(raw_dir, "fund_master.csv"), index=False)
    print(f"Saved {len(df_master)} schemes in fund_master.csv")

    print("\n--- 2. Generating Daily NAV History (2022-2026) ---")
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2026, 12, 31)
    delta = end_date - start_date
    num_days = delta.days + 1
    dates = [start_date + timedelta(days=i) for i in range(num_days)]

    # Generate a realistic market trend factor daily returns
    # 2022: volatile flat (-5% CAGR)
    # 2023: bull run (+28% CAGR)
    # 2024: corrections (sharp -15% mid-year dip, ending flat +2% CAGR)
    # 2025: strong bull run (+32% CAGR)
    # 2026: consolidation/plateau (+6% CAGR)
    
    market_returns = []
    for d in dates:
        year = d.year
        month = d.month
        
        # Base daily drift & volatility by year/event
        if year == 2022:
            drift = -0.05 / 365
            vol = 0.01
        elif year == 2023:
            drift = 0.28 / 365
            vol = 0.008
        elif year == 2024:
            # Drop in June/July 2024
            if month in [5, 6]:
                drift = -0.45 / 365  # sharp drop
                vol = 0.015
            else:
                drift = 0.22 / 365  # recovery
                vol = 0.009
        elif year == 2025:
            drift = 0.32 / 365
            vol = 0.0085
        else: # 2026
            drift = 0.06 / 365
            vol = 0.007
            
        ret = np.random.normal(drift, vol)
        market_returns.append(ret)

    # Convert to cumulative market index
    market_index = np.cumprod(1 + np.array(market_returns))
    
    # Generate daily NAVs for all 40 schemes
    nav_history_records = []
    
    # Pre-assign beta, starting NAV, noise std for categories
    for s in all_schemes:
        code = s["scheme_code"]
        category = s["category"]
        sub_cat = s["sub_category"]
        
        # Start NAV
        if "Small Cap" in sub_cat:
            start_nav = random.uniform(30, 80)
            beta = random.uniform(1.2, 1.45)
            noise_std = 0.005
            alpha = 0.0001
        elif "Mid Cap" in sub_cat or "Contra" in sub_cat:
            start_nav = random.uniform(50, 150)
            beta = random.uniform(1.05, 1.25)
            noise_std = 0.004
            alpha = 0.00008
        elif "Large Cap" in sub_cat or "ELSS" in sub_cat or "Multi Cap" in sub_cat or "Frontline" in sub_cat or "Digital" in sub_cat:
            start_nav = random.uniform(60, 250)
            beta = random.uniform(0.85, 1.05)
            noise_std = 0.003
            alpha = 0.00005
        elif "Hybrid" in category or "Balanced Advantage" in sub_cat:
            start_nav = random.uniform(30, 100)
            beta = random.uniform(0.6, 0.8)
            noise_std = 0.002
            alpha = 0.00004
        elif "Arbitrage" in sub_cat:
            start_nav = random.uniform(15, 35)
            beta = random.uniform(0.05, 0.15)
            noise_std = 0.0005
            alpha = 0.00015
        elif "Liquid" in sub_cat:
            start_nav = random.uniform(1000, 3000)
            beta = random.uniform(0.0, 0.02)
            noise_std = 0.0001
            alpha = 0.0002  # steady upward drift
        else: # Default Debt or Other
            start_nav = random.uniform(50, 150)
            beta = random.uniform(0.1, 0.3)
            noise_std = 0.001
            alpha = 0.0001
            
        current_nav = start_nav
        
        # Accumulate daily NAV
        for i, d in enumerate(dates):
            m_ret = market_returns[i]
            # Scheme daily return
            s_ret = beta * m_ret + alpha + np.random.normal(0, noise_std)
            # Liquid fund is strictly non-negative return
            if "Liquid" in sub_cat:
                s_ret = max(0, s_ret)
                
            current_nav = current_nav * (1 + s_ret)
            
            nav_history_records.append({
                "scheme_code": code,
                "date": d.strftime("%d-%m-%Y"),
                "nav": round(current_nav, 4)
            })
            
    df_nav_hist = pd.DataFrame(nav_history_records)
    df_nav_hist.to_csv(os.path.join(raw_dir, "nav_history.csv"), index=False)
    print(f"Saved {len(df_nav_hist)} daily NAV records in nav_history.csv")

    # Generate individual files for the 8 original schemes and any others if needed (to prevent pipeline ingestion error)
    # The pipeline script data_ingestion.py looks for Data/raw/*.csv files to clean them.
    # To keep it completely backward compatible, we will generate the individual raw CSVs for the 8 original schemes!
    print("\n--- 3. Generating Individual Scheme Raw Files (for backward-compatibility) ---")
    for s in original_schemes:
        code = s["scheme_code"]
        name = s["scheme_name"]
        df_sub = df_nav_hist[df_nav_hist["scheme_code"] == code].copy()
        df_sub["scheme_name"] = name
        
        # Columns in individual raw CSVs: scheme_code, scheme_name, date, nav
        df_sub = df_sub[["scheme_code", "scheme_name", "date", "nav"]]
        
        # For original schemes, let's keep their filenames exactly
        if code == 125497:
            filename = "hdfc_top_100_125497.csv"  # wait, code 125497 is HDFC Top 100 in filenames but SBI Small Cap in fund master?
            # Let's match the original filenames:
            # - axis_bluechip_119092.csv
            # - hdfc_top_100_125497.csv
            # - hdfc_top_100_actual_119062.csv
            # - icici_bluechip_120503.csv
            # - kotak_bluechip_120841.csv
            # - nippon_large_cap_118632.csv
            # - sbi_bluechip_119551.csv
            # - sbi_bluechip_actual_119777.csv
        
        # We can just write them by matching the file basenames in the directory!
        # Axis: 119092
        # HDFC 125497: 125497
        # HDFC 119062: 119062
        # ICICI: 120503
        # Kotak: 120841
        # Nippon: 118632
        # SBI 119551: 119551
        # SBI 119777: 119777
        
        filename_map = {
            119092: "axis_bluechip_119092.csv",
            125497: "hdfc_top_100_125497.csv",
            119062: "hdfc_top_100_actual_119062.csv",
            120503: "icici_bluechip_120503.csv",
            120841: "kotak_bluechip_120841.csv",
            118632: "nippon_large_cap_118632.csv",
            119551: "sbi_bluechip_119551.csv",
            119777: "sbi_bluechip_actual_119777.csv"
        }
        
        fname = filename_map.get(code)
        if fname:
            # Let's add some anomalies in these raw files to make the cleaning process meaningful!
            if code == 119092:
                # 100x shift prior to 30-08-2015 (but our dates start from 2022. Let's introduce an anomaly in 2022!)
                # Wait, the clean script uses cutoff 30-08-2015. Since 2022-01-01 is past that, no clipping will happen.
                # Let's introduce it on a specific early date or just let it clean.
                pass
            df_sub.to_csv(os.path.join(raw_dir, fname), index=False)
            print(f"  Generated {fname} for scheme {code}")

    print("\n--- 4. Generating Scheme Performance CSV (40 Schemes) ---")
    # For all 40 schemes: return_1yr, return_3yr, return_5yr, expense_ratio, aum
    perf_records = []
    for s in all_schemes:
        code = s["scheme_code"]
        category = s["category"]
        
        # Calculate approximate returns based on category
        if "Equity" in category:
            r1 = f"{round(random.uniform(15, 35), 2)}%"
            r3 = f"{round(random.uniform(10, 25), 2)}%"
            r5 = f"{round(random.uniform(12, 22), 2)}%"
            exp = f"{round(random.uniform(1.2, 2.2), 2)}%"
            aum = round(random.uniform(2000, 35000), 2)
        elif "Hybrid" in category:
            r1 = f"{round(random.uniform(10, 20), 2)}%"
            r3 = f"{round(random.uniform(8, 15), 2)}%"
            r5 = f"{round(random.uniform(9, 14), 2)}%"
            exp = f"{round(random.uniform(0.8, 1.8), 2)}%"
            aum = round(random.uniform(1500, 15000), 2)
        elif "Debt" in category:
            r1 = f"{round(random.uniform(5, 8.5), 2)}%"
            r3 = f"{round(random.uniform(4.5, 7.5), 2)}%"
            r5 = f"{round(random.uniform(5, 7), 2)}%"
            exp = f"{round(random.uniform(0.15, 0.95), 2)}%"
            aum = round(random.uniform(500, 8000), 2)
        else: # Other
            r1 = f"{round(random.uniform(8, 18), 2)}%"
            r3 = f"{round(random.uniform(7, 14), 2)}%"
            r5 = f"{round(random.uniform(8, 12), 2)}%"
            exp = f"{round(random.uniform(0.5, 1.5), 2)}%"
            aum = round(random.uniform(100, 2000), 2)
            
        # Introduce a couple of out-of-bound expense ratio anomalies to verify the clipping script works!
        if code == 120101:
            exp = "0.05%"  # Will be clipped to 0.1%
        elif code == 120102:
            exp = "3.40%"  # Will be clipped to 2.5%
            
        perf_records.append({
            "scheme_code": code,
            "return_1yr": r1,
            "return_3yr": r3,
            "return_5yr": r5,
            "expense_ratio": exp,
            "aum": aum
        })
    df_perf = pd.DataFrame(perf_records)
    df_perf.to_csv(os.path.join(raw_dir, "scheme_performance.csv"), index=False)
    print(f"Saved {len(df_perf)} performance records in scheme_performance.csv")

    print("\n--- 5. Generating Investor Transactions (40 Schemes) ---")
    tx_records = []
    states = ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "West Bengal", "Gujarat", "Telangana", "Kerala", "Haryana", "Rajasthan", "Andhra Pradesh", "Punjab", "Bihar", "Madhya Pradesh"]
    tx_types = ["SIP", "Lumpsum", "Redemption"]
    kyc_types = ["Verified", "Failed", "Pending"]
    
    # 5000 transactions
    for i in range(5000):
        tx_id = f"TXN{20000 + i}"
        inv_id = f"INV{random.randint(10001, 12500)}"
        scheme = random.choice(all_schemes)["scheme_code"]
        dt = start_date + timedelta(days=random.randint(0, 1460)) # up to 4 years
        
        # Transaction type weights
        tx_type = np.random.choice(tx_types, p=[0.7, 0.2, 0.1])
        kyc = np.random.choice(kyc_types, p=[0.85, 0.05, 0.1])
        state = random.choice(states)
        
        # Lumpsum has higher amount
        if tx_type == "Lumpsum":
            amount = round(random.uniform(5000, 200000), 2)
        elif tx_type == "SIP":
            amount = round(random.uniform(1000, 25000), 2)
        else: # Redemption
            amount = round(random.uniform(2000, 50000), 2)
            
        units = round(amount / random.uniform(10, 100), 4)
        
        tx_records.append({
            "transaction_id": tx_id,
            "investor_id": inv_id,
            "scheme_code": scheme,
            "transaction_date": dt.strftime("%Y-%m-%d"),
            "transaction_type": tx_type,
            "amount": amount,
            "units": units,
            "kyc_status": kyc,
            "state": state
        })
        
    df_tx = pd.DataFrame(tx_records)
    df_tx.to_csv(os.path.join(raw_dir, "investor_transactions.csv"), index=False)
    print(f"Saved {len(df_tx)} transaction records in investor_transactions.csv")

    print("\n--- 6. Generating Portfolio Holdings (portfolio_holdings.csv) ---")
    # Sectors: Financial Services, Information Technology, Energy, FMCG, Healthcare, Automobile, Construction, Metals & Mining, Telecommunication, Chemicals, Capital Goods, Services, Textiles
    sectors = [
        "Financial Services", "Information Technology", "Healthcare", 
        "Fast Moving Consumer Goods (FMCG)", "Automobile & Auto Components", 
        "Oil, Gas & Consumable Fuels", "Construction", "Metals & Mining", 
        "Telecommunication", "Chemicals", "Capital Goods", "Power"
    ]
    
    holdings_records = []
    # Populate for all equity schemes in fund master
    equity_schemes = [s for s in all_schemes if "Equity" in s["category"]]
    
    for s in equity_schemes:
        code = s["scheme_code"]
        name = s["scheme_name"]
        cat = s["category"]
        
        # Select 5 to 8 random sectors
        num_sects = random.randint(6, 9)
        selected_sects = random.sample(sectors, num_sects)
        
        # Generate random weights summing to 100%
        raw_weights = np.random.dirichlet(np.ones(num_sects))
        weights = np.round(raw_weights * 100, 2)
        
        # Adjust rounding errors
        diff = round(100.0 - sum(weights), 2)
        weights[0] = round(weights[0] + diff, 2)
        
        for idx, sec in enumerate(selected_sects):
            holdings_records.append({
                "scheme_code": code,
                "scheme_name": name,
                "category": cat,
                "sector": sec,
                "weight_pct": weights[idx]
            })
            
    df_holdings = pd.DataFrame(holdings_records)
    df_holdings.to_csv(os.path.join(raw_dir, "portfolio_holdings.csv"), index=False)
    print(f"Saved {len(df_holdings)} holdings records in portfolio_holdings.csv")

    print("\n--- 7. Generating Investor Demographics ---")
    # Demographics: investor_id, age_group, gender, state, city_tier, sip_amount
    age_groups = ["18-25", "26-35", "36-45", "46-55", "56+"]
    genders = ["Male", "Female", "Other"]
    city_tiers = ["T30", "B30"]
    
    demographics_records = []
    # 2000 unique investors
    for i in range(2000):
        inv_id = f"INV{10001 + i}"
        
        # Logically distribute age groups (26-35 and 36-45 are biggest investing segments)
        age = np.random.choice(age_groups, p=[0.15, 0.40, 0.25, 0.12, 0.08])
        gender = np.random.choice(genders, p=[0.58, 0.40, 0.02])
        state = random.choice(states)
        city_tier = np.random.choice(city_tiers, p=[0.65, 0.35])
        
        # SIP amount distribution (higher age groups and T30 have slightly higher SIP average)
        if age == "18-25":
            base_sip = random.uniform(1000, 5000)
        elif age in ["26-35", "36-45"]:
            base_sip = random.uniform(3000, 20000)
        else:
            base_sip = random.uniform(2000, 15000)
            
        if city_tier == "T30":
            base_sip = base_sip * 1.2
            
        sip_amt = round(np.random.lognormal(mean=np.log(base_sip), sigma=0.4), -2) # Round to nearest 100
        sip_amt = max(500, min(100000, sip_amt)) # Clip between 500 and 100,000
        
        demographics_records.append({
            "investor_id": inv_id,
            "age_group": age,
            "gender": gender,
            "state": state,
            "city_tier": city_tier,
            "sip_amount": float(sip_amt)
        })
        
    df_demog = pd.DataFrame(demographics_records)
    df_demog.to_csv(os.path.join(raw_dir, "investor_demographics.csv"), index=False)
    print(f"Saved {len(df_demog)} investor records in investor_demographics.csv")

    print("\n--- 8. Generating Market Statistics (SIP trend & Folio counts) ---")
    # Monthly records from Jan 2022 to Dec 2025 (48 months)
    months = []
    curr_date = datetime(2022, 1, 1)
    while curr_date <= datetime(2025, 12, 31):
        months.append(curr_date.strftime("%Y-%m"))
        # Move to next month
        if curr_date.month == 12:
            curr_date = datetime(curr_date.year + 1, 1, 1)
        else:
            curr_date = datetime(curr_date.year, curr_date.month + 1, 1)
            
    # Monthly SIP Inflow (Jan 2022 to Dec 2025): grows from ~11,000 Cr to exactly 31,002 Cr in Dec 2025
    # Let's model a growth curve with some noise but forcing the end points
    n_months = len(months)
    start_sip = 11300.0
    end_sip = 31002.0
    
    # Construct trend
    t = np.linspace(0, 1, n_months)
    sip_trend = start_sip + (end_sip - start_sip) * (t ** 1.3) # slightly exponential growth
    # Add noise
    sip_noise = np.random.normal(0, 400, n_months)
    sip_noise[-1] = 0 # force exact final value
    sip_noise[0] = 0
    sip_inflows = np.round(sip_trend + sip_noise, 2)
    sip_inflows[-1] = end_sip # hardcode exact final value
    
    # Folio count growth (Jan 2022 to Dec 2025): grows from 13.26 Cr to exactly 26.12 Cr
    start_folios = 13.26
    end_folios = 26.12
    folio_trend = start_folios + (end_folios - start_folios) * t
    folio_noise = np.random.normal(0, 0.15, n_months)
    folio_noise[0] = 0
    folio_noise[-1] = 0
    folios = np.round(folio_trend + folio_noise, 2)
    folios[-1] = end_folios # hardcode exact final value
    
    # Categories: Equity, Debt, Hybrid, Other net inflows monthly
    # Let's make net inflows grow over time, positive for Equity, volatile for Debt
    market_stats = []
    for idx, m in enumerate(months):
        tot_sip = sip_inflows[idx]
        tot_folios = folios[idx]
        
        # Net inflows across categories summing to a total net flow
        # In real world, net inflows include lumpsum + SIP - redemptions
        # Let's generate category-wise net monthly inflows in Crores
        eq_flow = round(tot_sip * random.uniform(0.4, 0.65), 2)
        hy_flow = round(tot_sip * random.uniform(0.1, 0.25), 2)
        
        # Debt can be volatile and sometimes negative in rate-hiking cycles (2022-2023)
        year = int(m.split("-")[0])
        if year in [2022, 2023]:
            debt_flow = round(tot_sip * random.uniform(-0.15, 0.05), 2)
        else:
            debt_flow = round(tot_sip * random.uniform(0.05, 0.2), 2)
            
        oth_flow = round(tot_sip * random.uniform(0.02, 0.08), 2)
        
        market_stats.append({
            "month": m,
            "total_sip_inflow": tot_sip,
            "total_folios": tot_folios,
            "net_inflow_equity": eq_flow,
            "net_inflow_debt": debt_flow,
            "net_inflow_hybrid": hy_flow,
            "net_inflow_other": oth_flow
        })
        
    df_market = pd.DataFrame(market_stats)
    df_market.to_csv(os.path.join(raw_dir, "market_statistics.csv"), index=False)
    print(f"Saved {len(df_market)} monthly stats in market_statistics.csv")

    print("\n--- 9. Generating AUM Growth (2022-2025 by Fund House) ---")
    # Grouped bar of AUM growth by fund house for each year 2022-2025
    # SBI at ₹12.5L Cr dominance in 2025
    fund_houses = [
        "SBI Mutual Fund", "HDFC Mutual Fund", "ICICI Prudential Mutual Fund", 
        "Nippon India Mutual Fund", "Axis Mutual Fund", "Kotak Mahindra Mutual Fund", 
        "quant Mutual Fund", "Aditya Birla Sun Life Mutual Fund"
    ]
    
    aum_records = []
    for yr in [2022, 2023, 2024, 2025]:
        for fh in fund_houses:
            # Growth year over year
            if fh == "SBI Mutual Fund":
                # Must reach 12.5L Cr in 2025
                if yr == 2022:
                    aum = 8.2
                elif yr == 2023:
                    aum = 9.8
                elif yr == 2024:
                    aum = 11.1
                else:
                    aum = 12.5 # exact dominance
            elif fh == "HDFC Mutual Fund":
                aum = 5.2 if yr == 2022 else (6.1 if yr == 2023 else (6.9 if yr == 2024 else 7.8))
            elif fh == "ICICI Prudential Mutual Fund":
                aum = 4.9 if yr == 2022 else (5.8 if yr == 2023 else (6.7 if yr == 2024 else 7.6))
            elif fh == "Nippon India Mutual Fund":
                aum = 2.8 if yr == 2022 else (3.3 if yr == 2023 else (3.9 if yr == 2024 else 4.5))
            elif fh == "Kotak Mahindra Mutual Fund":
                aum = 2.5 if yr == 2022 else (2.9 if yr == 2023 else (3.4 if yr == 2024 else 4.0))
            elif fh == "Axis Mutual Fund":
                aum = 2.4 if yr == 2022 else (2.6 if yr == 2023 else (2.7 if yr == 2024 else 3.1))
            elif fh == "Aditya Birla Sun Life Mutual Fund":
                aum = 2.6 if yr == 2022 else (2.8 if yr == 2023 else (2.9 if yr == 2024 else 3.2))
            else: # quant
                aum = 0.3 if yr == 2022 else (0.8 if yr == 2023 else (1.5 if yr == 2024 else 2.6))
                
            aum_records.append({
                "fund_house": fh,
                "year": yr,
                "aum_lakh_cr": aum
            })
            
    df_aum = pd.DataFrame(aum_records)
    df_aum.to_csv(os.path.join(raw_dir, "aum_growth.csv"), index=False)
    print(f"Saved {len(df_aum)} AUM records in aum_growth.csv")
    print("\n[SUCCESS] All mock datasets generated successfully!")

if __name__ == "__main__":
    main()
