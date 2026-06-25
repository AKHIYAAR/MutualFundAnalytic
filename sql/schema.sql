-- Schema for Mutual Fund SQLite Star Schema

-- 1. Dimension: Fund details
CREATE TABLE IF NOT EXISTS dim_fund (
    scheme_code INTEGER PRIMARY KEY CHECK (scheme_code > 0),
    scheme_name TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    category TEXT NOT NULL,
    sub_category TEXT NOT NULL,
    risk_grade TEXT NOT NULL
);

-- 2. Dimension: Date hierarchy
CREATE TABLE IF NOT EXISTS dim_date (
    date_key TEXT PRIMARY KEY, -- 'YYYY-MM-DD'
    date TEXT NOT NULL,        -- 'YYYY-MM-DD'
    day INTEGER NOT NULL CHECK (day BETWEEN 1 AND 31),
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    year INTEGER NOT NULL CHECK (year > 0),
    quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    day_of_week TEXT NOT NULL,
    is_weekend INTEGER NOT NULL CHECK (is_weekend IN (0, 1))
);

-- 3. Fact: Daily NAV history
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code INTEGER NOT NULL,
    date_key TEXT NOT NULL,
    nav REAL NOT NULL CHECK (nav > 0),
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

-- 4. Fact: Investor transactions
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id TEXT PRIMARY KEY,
    investor_id TEXT NOT NULL,
    scheme_code INTEGER NOT NULL,
    date_key TEXT NOT NULL,
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('SIP', 'Lumpsum', 'Redemption')),
    amount REAL NOT NULL CHECK (amount > 0),
    units REAL NOT NULL CHECK (units > 0),
    kyc_status TEXT NOT NULL CHECK (kyc_status IN ('Verified', 'Failed', 'Pending')),
    state TEXT NOT NULL,
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

-- 5. Fact: Scheme performance metrics
CREATE TABLE IF NOT EXISTS fact_performance (
    scheme_code INTEGER PRIMARY KEY,
    return_1yr REAL,
    return_3yr REAL,
    return_5yr REAL,
    expense_ratio REAL CHECK (expense_ratio >= 0.1 AND expense_ratio <= 2.5),
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code)
);

-- 6. Fact: Scheme AUM (Assets Under Management)
CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code INTEGER NOT NULL,
    date_key TEXT NOT NULL,
    aum_amount REAL NOT NULL CHECK (aum_amount > 0), -- In Crores
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

-- 7. Indexes for optimization
CREATE INDEX IF NOT EXISTS idx_fact_nav_scheme_date ON fact_nav(scheme_code, date_key);
CREATE INDEX IF NOT EXISTS idx_fact_tx_scheme_date ON fact_transactions(scheme_code, date_key);
CREATE INDEX IF NOT EXISTS idx_fact_aum_scheme_date ON fact_aum(scheme_code, date_key);
