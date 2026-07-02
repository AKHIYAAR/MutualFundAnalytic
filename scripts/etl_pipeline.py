import os
import sys
import sqlite3
import pandas as pd
import numpy as np
import logging
import shutil

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def parse_date(date_str):
    if not isinstance(date_str, str):
        return pd.NaT
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d/%m/%y", "%Y-%m-%d %H:%M:%S"):
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            continue
    try:
        return pd.to_datetime(date_str)
    except:
        return pd.NaT

def clean_return_val(val):
    if val is None:
        return np.nan
    if not isinstance(val, str):
        if pd.isna(val):
            return np.nan
        return float(val)
    val_clean = val.strip().replace('%', '')
    if val_clean.upper() in ['N/A', 'NA', 'NULL', '']:
        return np.nan
    try:
        return float(val_clean)
    except ValueError:
        return np.nan

def clean_expense_ratio(val, scheme_code=None):
    if val is None:
        return np.nan
    if not isinstance(val, str):
        if pd.isna(val):
            return np.nan
        ratio = float(val)
    else:
        val_clean = val.strip().replace('%', '')
        if val_clean.upper() in ['N/A', 'NA', 'NULL', '']:
            return np.nan
        try:
            ratio = float(val_clean)
        except ValueError:
            return np.nan
            
    # Clip to [0.1, 2.5] bounds to satisfy SQLite CHECK constraint
    if ratio < 0.1:
        ratio = 0.1
    elif ratio > 2.5:
        ratio = 2.5
    return ratio

def run_etl():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    db_dir = os.path.join(base_dir, 'data', 'db')
    schema_path = os.path.join(base_dir, 'sql', 'schema.sql')
    
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(db_dir, exist_ok=True)
    
    db_path = os.path.join(db_dir, 'bluestock_mf.db')
    # Set up file handler for logging
    file_handler = logging.FileHandler(os.path.join(base_dir, 'logs', 'etl_pipeline.log'))
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(file_handler)
    logging.info(f"Using database: {db_path}")
    
    # 1. Verify raw CSV files are present
    raw_files = ['fund_master.csv', 'nav_history.csv', 'investor_transactions.csv', 'investor_demographics.csv', 'portfolio_holdings.csv', 'scheme_performance.csv']
    for rf in raw_files:
        path = os.path.join(raw_dir, rf)
        if not os.path.exists(path):
            logging.error(f"Required raw file missing: {path}")
            return False
            
    # 2. Ingest and Clean fund_master.csv
    logging.info("Processing fund_master.csv...")
    df_fund = pd.read_csv(os.path.join(raw_dir, 'fund_master.csv'))
    df_fund.to_csv(os.path.join(processed_dir, 'fund_master.csv'), index=False)
    
    # 3. Ingest and Clean nav_history.csv (with reindexing/forward-fill & decimal shifts)
    logging.info("Processing nav_history.csv...")
    df_nav = pd.read_csv(os.path.join(raw_dir, 'nav_history.csv'))
    df_nav['parsed_date'] = df_nav['date'].apply(parse_date)
    df_nav = df_nav.dropna(subset=['parsed_date'])
    df_nav['nav'] = pd.to_numeric(df_nav['nav'], errors='coerce')
    
    # Handle specific decimal anomalies
    # Correct 100x shift for scheme 119092 prior to 30-08-2015
    cutoff_date = pd.to_datetime('30-08-2015', format='%d-%m-%Y')
    mask_119092 = (df_nav['scheme_code'] == 119092) & (df_nav['parsed_date'] < cutoff_date)
    df_nav.loc[mask_119092, 'nav'] = df_nav.loc[mask_119092, 'nav'] * 100
    
    # Correct zero/null NAV for scheme 120503 on 07-04-2013 via linear interpolation
    df_nav.loc[(df_nav['scheme_code'] == 120503) & (df_nav['nav'] <= 0.0), 'nav'] = np.nan
    
    # Reindex and forward-fill NAV per scheme to handle weekends/holidays
    cleaned_nav_dfs = []
    for code, group in df_nav.groupby('scheme_code'):
        group_sorted = group.copy().sort_values('parsed_date')
        min_date = group_sorted['parsed_date'].min()
        max_date = group_sorted['parsed_date'].max()
        full_range = pd.date_range(start=min_date, end=max_date, freq='D')
        
        group_sorted = group_sorted.set_index('parsed_date')
        group_reindexed = group_sorted.reindex(full_range)
        group_reindexed.index.name = 'parsed_date'
        group_reindexed = group_reindexed.reset_index()
        
        group_reindexed['scheme_code'] = code
        group_reindexed['nav'] = group_reindexed['nav'].ffill().bfill()
        group_reindexed['date'] = group_reindexed['parsed_date'].dt.strftime('%d-%m-%Y')
        group_reindexed['date_key'] = group_reindexed['parsed_date'].dt.strftime('%Y-%m-%d')
        
        group_reindexed = group_reindexed[['scheme_code', 'date', 'nav', 'date_key']]
        cleaned_nav_dfs.append(group_reindexed)
        
    df_nav_clean = pd.concat(cleaned_nav_dfs, ignore_index=True)
    df_nav_clean[['scheme_code', 'date', 'nav']].to_csv(os.path.join(processed_dir, 'nav_history.csv'), index=False)
    
    # 4. Ingest and Clean transactions
    logging.info("Processing investor_transactions.csv...")
    df_tx = pd.read_csv(os.path.join(raw_dir, 'investor_transactions.csv'))
    df_tx['parsed_date'] = df_tx['transaction_date'].apply(parse_date)
    df_tx['date_key'] = df_tx['parsed_date'].dt.strftime('%Y-%m-%d')
    df_tx.drop(columns=['parsed_date', 'transaction_date'], inplace=True)
    df_tx.to_csv(os.path.join(processed_dir, 'investor_transactions.csv'), index=False)
    
    # 5. Ingest other datasets and clean performance
    logging.info("Processing other secondary datasets...")
    # Clean scheme_performance.csv
    df_perf = pd.read_csv(os.path.join(raw_dir, 'scheme_performance.csv'))
    for col in ['return_1yr', 'return_3yr', 'return_5yr']:
        df_perf[col] = df_perf[col].apply(clean_return_val)
    df_perf['expense_ratio'] = df_perf.apply(lambda row: clean_expense_ratio(row['expense_ratio'], row['scheme_code']), axis=1)
    df_perf.to_csv(os.path.join(processed_dir, 'scheme_performance.csv'), index=False)
    
    # Process other EDA files
    for other_f in ['investor_demographics.csv', 'portfolio_holdings.csv', 'market_statistics.csv', 'aum_growth.csv']:
        path = os.path.join(raw_dir, other_f)
        if os.path.exists(path):
            shutil_df = pd.read_csv(path)
            shutil_df.to_csv(os.path.join(processed_dir, other_f), index=False)
            
    # 6. Database Loading via schema.sql
    logging.info("Setting up SQLite database schema...")
    conn = sqlite3.connect(db_path)
    
    if os.path.exists(schema_path):
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()
            
        cursor = conn.cursor()
        tables_to_drop = [
            'fact_aum', 'fact_performance', 'fact_transactions', 'fact_nav',
            'dim_date', 'dim_fund', 'fact_holdings', 'dim_investor',
            'fact_market_stats', 'fact_aum_growth'
        ]
        for t in tables_to_drop:
            cursor.execute(f"DROP TABLE IF EXISTS {t};")
            
        for statement in schema_sql.split(";"):
            if statement.strip():
                cursor.execute(statement + ";")
        conn.commit()
        logging.info("SQLite database schema applied.")
    else:
        logging.error(f"Database schema file missing: {schema_path}")
        conn.close()
        return False
        
    # 7. Loading Tables
    logging.info("Loading cleaned DataFrames into SQLite...")
    
    # dim_fund
    df_fund.to_sql('dim_fund', conn, if_exists='append', index=False)
    
    # dim_investor
    df_demog = pd.read_csv(os.path.join(processed_dir, 'investor_demographics.csv'))
    df_demog.to_sql('dim_investor', conn, if_exists='append', index=False)
    
    # fact_nav
    df_nav_fact = df_nav_clean[['scheme_code', 'date_key', 'nav']].copy()
    df_nav_fact.to_sql('fact_nav', conn, if_exists='append', index=False)
    
    # fact_transactions
    df_tx_fact = df_tx[[
        'transaction_id', 'investor_id', 'scheme_code', 'date_key',
        'transaction_type', 'amount', 'units', 'kyc_status', 'state'
    ]]
    df_tx_fact.to_sql('fact_transactions', conn, if_exists='append', index=False)
    
    # fact_holdings
    df_holdings = pd.read_csv(os.path.join(processed_dir, 'portfolio_holdings.csv'))
    df_holdings_fact = df_holdings[['scheme_code', 'sector', 'weight_pct']].copy()
    df_holdings_fact.to_sql('fact_holdings', conn, if_exists='append', index=False)
    
    # fact_performance
    df_perf_fact = df_perf[['scheme_code', 'return_1yr', 'return_3yr', 'return_5yr', 'expense_ratio']].copy()
    df_perf_fact.to_sql('fact_performance', conn, if_exists='append', index=False)
    
    # fact_market_stats
    df_market = pd.read_csv(os.path.join(processed_dir, 'market_statistics.csv'))
    df_market.to_sql('fact_market_stats', conn, if_exists='append', index=False)
    
    # fact_aum_growth
    df_aum_growth = pd.read_csv(os.path.join(processed_dir, 'aum_growth.csv'))
    df_aum_growth.to_sql('fact_aum_growth', conn, if_exists='append', index=False)
    
    # Build dim_date
    unique_dates_nav = set(df_nav_clean['date_key'].dropna().unique())
    unique_dates_tx = set(df_tx['date_key'].dropna().unique())
    all_unique_dates = sorted(list(unique_dates_nav.union(unique_dates_tx)))
    
    dim_date_records = []
    for dt_str in all_unique_dates:
        dt = pd.to_datetime(dt_str, format='%Y-%m-%d')
        dim_date_records.append({
            "date_key": dt_str,
            "date": dt_str,
            "day": dt.day,
            "month": dt.month,
            "year": dt.year,
            "quarter": (dt.month - 1) // 3 + 1,
            "day_of_week": dt.strftime('%A'),
            "is_weekend": 1 if dt.weekday() >= 5 else 0
        })
    df_dim_date = pd.DataFrame(dim_date_records)
    df_dim_date.to_sql('dim_date', conn, if_exists='append', index=False)
    
    # fact_aum
    latest_date_key = df_dim_date['date_key'].max()
    df_aum_fact = df_perf[['scheme_code', 'aum']].copy()
    df_aum_fact.rename(columns={"aum": "aum_amount"}, inplace=True)
    df_aum_fact['date_key'] = latest_date_key
    df_aum_fact = df_aum_fact[['scheme_code', 'date_key', 'aum_amount']]
    df_aum_fact.to_sql("fact_aum", conn, if_exists="append", index=False)
    
    # 8. Row Count Verification
    logging.info("Verifying row counts...")
    expected_counts = {
        "dim_fund": len(df_fund),
        "dim_date": len(df_dim_date),
        "fact_nav": len(df_nav_fact),
        "fact_transactions": len(df_tx_fact),
        "fact_performance": len(df_perf_fact),
        "fact_aum": len(df_aum_fact),
        "dim_investor": len(df_demog),
        "fact_holdings": len(df_holdings_fact),
        "fact_market_stats": len(df_market),
        "fact_aum_growth": len(df_aum_growth)
    }
    
    cursor = conn.cursor()
    for table, expected in expected_counts.items():
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        db_count = cursor.fetchone()[0]
        if db_count == expected:
            logging.info(f"Table {table:18}: Expected = {expected:5}, Database = {db_count:5} -> PASSED")
        else:
            logging.error(f"Table {table:18}: Expected = {expected:5}, Database = {db_count:5} -> FAILED")
            conn.close()
            return False
            
    conn.close()
    logging.info("ETL Pipeline completed successfully. SQLite database matches local schema completely.")
    return True

if __name__ == '__main__':
    try:
        success = run_etl()
        sys.exit(0 if success else 1)
    except Exception as e:
        logging.exception("Unexpected error during ETL execution")
        sys.exit(2)
