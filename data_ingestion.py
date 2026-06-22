import os
import glob
import pandas as pd

def load_and_inspect_datasets():
    csv_files = glob.glob("data/raw/*.csv")
    print(f"Found {len(csv_files)} CSV files in data/raw/\n")
    
    inspection_results = {}
    
    for filepath in csv_files:
        filename = os.path.basename(filepath)
        print("=" * 60)
        print(f"Dataset: {filename}")
        print("=" * 60)
        try:
            df = pd.read_csv(filepath)
            print(f"Shape: {df.shape}")
            print("\nDtypes:")
            print(df.dtypes)
            print("\nHead:")
            print(df.head())
            print("\nAnomalies check:")
            
            missing = df.isnull().sum()
            has_missing = missing.any()
            missing_info = {}
            if has_missing:
                print("  - Missing values found:")
                for col, val in missing.items():
                    if val > 0:
                        print(f"    * {col}: {val} missing values")
                        missing_info[col] = val
            else:
                print("  - No missing values.")
                
            duplicates = int(df.duplicated().sum())
            if duplicates > 0:
                print(f"  - Duplicate rows found: {duplicates}")
            else:
                print("  - No duplicate rows.")
                
            inspection_results[filename] = {
                "shape": df.shape,
                "dtypes": {k: str(v) for k, v in df.dtypes.items()},
                "missing": missing_info,
                "duplicates": duplicates
            }
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            inspection_results[filename] = {"error": str(e)}
        print("\n" + "-" * 60 + "\n")
        
    return inspection_results

def explore_fund_master():
    fund_master_path = "data/raw/fund_master.csv"
    if not os.path.exists(fund_master_path):
        print("fund_master.csv not found. Skipping exploration.")
        return None
        
    print("=" * 60)
    print("Exploring Fund Master")
    print("=" * 60)
    df_master = pd.read_csv(fund_master_path)
    
    unique_houses = df_master['fund_house'].unique().tolist()
    unique_categories = df_master['category'].unique().tolist()
    unique_subcategories = df_master['sub_category'].unique().tolist()
    
    risk_col = 'risk_grade' if 'risk_grade' in df_master.columns else ('risk_level' if 'risk_level' in df_master.columns else None)
    unique_risk_grades = df_master[risk_col].unique().tolist() if risk_col else []
    
    print(f"Unique Fund Houses: {len(unique_houses)}")
    print(f"Unique Categories: {len(unique_categories)}")
    print(f"Unique Sub-Categories: {len(unique_subcategories)}")
    print(f"Unique Risk Grades: {len(unique_risk_grades)}")
    
    # Understand AMFI code structure
    code_col = 'scheme_code' if 'scheme_code' in df_master.columns else ('amfi_code' if 'amfi_code' in df_master.columns else None)
    if code_col:
        codes = df_master[code_col].astype(str)
        lengths = codes.str.len().value_counts()
        print("\nAMFI Code Length Distribution:")
        for length, count in lengths.items():
            print(f"  - {length} digits: {count} schemes")
            
    return {
        "fund_houses": unique_houses,
        "categories": unique_categories,
        "sub_categories": unique_subcategories,
        "risk_grades": unique_risk_grades,
        "code_column": code_col
    }

def validate_amfi_codes():
    fund_master_path = "data/raw/fund_master.csv"
    nav_history_path = "data/raw/nav_history.csv"
    
    if not os.path.exists(fund_master_path) or not os.path.exists(nav_history_path):
        print("fund_master.csv or nav_history.csv missing. Skipping code validation.")
        return None
        
    df_master = pd.read_csv(fund_master_path)
    df_history = pd.read_csv(nav_history_path)
    
    master_code_col = 'scheme_code' if 'scheme_code' in df_master.columns else ('amfi_code' if 'amfi_code' in df_master.columns else None)
    history_code_col = 'scheme_code' if 'scheme_code' in df_history.columns else ('amfi_code' if 'amfi_code' in df_history.columns else None)
    
    if not master_code_col or not history_code_col:
        print("Could not identify scheme code columns in datasets.")
        return None
        
    master_codes = set(df_master[master_code_col].unique())
    history_codes = set(df_history[history_code_col].unique())
    
    missing_in_history = master_codes - history_codes
    
    print("=" * 60)
    print("AMFI Code Validation")
    print("=" * 60)
    if missing_in_history:
        print(f"WARNING: {len(missing_in_history)} codes in fund_master are missing in nav_history!")
        print("Sample missing codes:", list(missing_in_history)[:10])
    else:
        print("SUCCESS: Every scheme code in fund_master exists in nav_history.")
        
    return {
        "master_unique_codes": len(master_codes),
        "history_unique_codes": len(history_codes),
        "missing_codes": list(missing_in_history)
    }

def generate_report(inspection, master_info, validation):
    os.makedirs("reports", exist_ok=True)
    report_path = "reports/data_quality_summary.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Mutual Fund Data Ingestion Quality Report\n\n")
        
        f.write("## 1. Dataset Shape and Types\n\n")
        f.write("| Dataset | Rows | Columns | Duplicates | Missing Values | Anomalies |\n")
        f.write("| --- | --- | --- | --- | --- | --- |\n")
        
        for name, info in inspection.items():
            if "error" in info:
                f.write(f"| {name} | Error | Error | - | - | {info['error']} |\n")
                continue
                
            shape = info["shape"]
            dups = info["duplicates"]
            missing = info["missing"]
            
            missing_str = ", ".join([f"{col}: {val}" for col, val in missing.items()]) if missing else "None"
            anomalies_str = []
            if dups > 0:
                anomalies_str.append(f"{dups} duplicates")
            if missing:
                anomalies_str.append("missing values")
            
            f.write(f"| {name} | {shape[0]} | {shape[1]} | {dups} | {missing_str} | {', '.join(anomalies_str) if anomalies_str else 'None'} |\n")
            
        f.write("\n")
        
        if master_info:
            f.write("## 2. Fund Master Exploration\n\n")
            f.write(f"- **Total Fund Houses:** {len(master_info['fund_houses'])}\n")
            f.write(f"- **Total Categories:** {len(master_info['categories'])}\n")
            f.write(f"- **Total Sub-categories:** {len(master_info['sub_categories'])}\n")
            f.write(f"- **Total Risk Grades:** {len(master_info['risk_grades'])}\n\n")
            
            f.write("### Scheme Categories:\n")
            for cat in master_info['categories']:
                f.write(f"- {cat}\n")
            f.write("\n")
            
            f.write("### Risk Grades:\n")
            for rg in master_info['risk_grades']:
                f.write(f"- {rg}\n")
            f.write("\n")
            
        if validation:
            f.write("## 3. AMFI Code Validation Results\n\n")
            f.write(f"- **Unique scheme codes in `fund_master`:** {validation['master_unique_codes']}\n")
            f.write(f"- **Unique scheme codes in `nav_history`:** {validation['history_unique_codes']}\n")
            
            missing = validation["missing_codes"]
            if missing:
                f.write(f"- **WARNING:** {len(missing)} codes in `fund_master` do not have any NAV history in `nav_history.csv`.\n")
                f.write("- **Status:** FAILED (Referential Integrity check failed)\n\n")
                f.write("### Sample Missing Codes:\n")
                for c in missing[:15]:
                    f.write(f"- `{c}`\n")
            else:
                f.write("- **Status:** PASSED (All codes exist in history)\n")
                
    print(f"Data quality report saved to {report_path}")

def main():
    inspection = load_and_inspect_datasets()
    master_info = explore_fund_master()
    validation = validate_amfi_codes()
    generate_report(inspection, master_info, validation)

if __name__ == "__main__":
    main()
