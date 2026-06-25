# Mutual Fund Analytics Database Data Dictionary

This data dictionary documents the structure, column definitions, data types, business definitions, constraints, index optimizations, and source references for the SQLite star schema database (`Data/processed/mutual_funds.db`).

---

## 1. Dimension Tables

### 1.1 `dim_fund`
Stores metadata and details about the mutual fund schemes.

*   **Database Constraints:**
    *   `scheme_code` CHECK constraint: `scheme_code > 0`

| Column Name | Data Type | Key Type | Database Constraints / Rules | Business Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `scheme_code` | INTEGER | Primary Key | `CHECK (scheme_code > 0)` | AMFI Mutual Fund code identifier (unique). | `Data/processed/fund_master.csv` |
| `scheme_name` | TEXT | - | NOT NULL | Full marketing and legal name of the mutual fund scheme. | `Data/processed/fund_master.csv` |
| `fund_house` | TEXT | - | NOT NULL | Asset Management Company (AMC) managing the fund. | `Data/processed/fund_master.csv` |
| `category` | TEXT | - | NOT NULL | High-level asset class category (Equity, Debt, Hybrid, etc). | `Data/processed/fund_master.csv` |
| `sub_category`| TEXT | - | NOT NULL | Specific classification (e.g. Small Cap, Money Market). | `Data/processed/fund_master.csv` |
| `risk_grade` | TEXT | - | NOT NULL | Risk rating evaluated for the fund (e.g. Very High, Moderate). | `Data/processed/fund_master.csv` |

---

### 1.2 `dim_date`
Represents the calendar dimension, supporting date-based hierarchies.

*   **Database Constraints:**
    *   `day` CHECK constraint: `day BETWEEN 1 AND 31`
    *   `month` CHECK constraint: `month BETWEEN 1 AND 12`
    *   `year` CHECK constraint: `year > 0`
    *   `quarter` CHECK constraint: `quarter BETWEEN 1 AND 4`
    *   `is_weekend` CHECK constraint: `is_weekend IN (0, 1)`

| Column Name | Data Type | Key Type | Database Constraints / Rules | Business Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `date_key` | TEXT | Primary Key | - | Date formatted as 'YYYY-MM-DD' representing the day. | Programmatically generated |
| `date` | TEXT | - | NOT NULL | Same as date_key, representing ISO formatted date string. | Programmatically generated |
| `day` | INTEGER | - | `CHECK (day BETWEEN 1 AND 31)` | Calendar day of month (1-31). | Programmatically generated |
| `month` | INTEGER | - | `CHECK (month BETWEEN 1 AND 12)` | Calendar month number (1-12). | Programmatically generated |
| `year` | INTEGER | - | `CHECK (year > 0)` | Calendar year (e.g. 2026). | Programmatically generated |
| `quarter` | INTEGER | - | `CHECK (quarter BETWEEN 1 AND 4)` | Calendar quarter of the year (1-4). | Programmatically generated |
| `day_of_week` | TEXT | - | NOT NULL | Full name of the weekday (e.g. Monday, Tuesday). | Programmatically generated |
| `is_weekend` | INTEGER | - | `CHECK (is_weekend IN (0, 1))` | Boolean flag (1 = Saturday or Sunday, 0 = Weekday). | Programmatically generated |

---

## 2. Fact Tables

### 2.1 `fact_nav`
Stores daily historical Net Asset Value (NAV) details for each fund scheme.

*   **Database Constraints:**
    *   `nav` CHECK constraint: `nav > 0`
*   **Database Indexes:**
    *   `idx_fact_nav_scheme_date` on `(scheme_code, date_key)` for rapid joins and sorting.

| Column Name | Data Type | Key Type | Database Constraints / Rules | Business Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `nav_id` | INTEGER | Primary Key | Auto-incremented | Auto-incremented unique record identifier. | Internal DB |
| `scheme_code` | INTEGER | Foreign Key | NOT NULL (Refs `dim_fund`) | Fund identifier. | `Data/processed/nav_history.csv` |
| `date_key` | TEXT | Foreign Key | NOT NULL (Refs `dim_date`) | Date identifier. | `Data/processed/nav_history.csv` |
| `nav` | REAL | - | `CHECK (nav > 0)` | Net Asset Value (NAV) per unit of the scheme on the date. | `Data/processed/nav_history.csv` |

---

### 2.2 `fact_transactions`
Stores granular investor buy/sell activity.

*   **Database Constraints:**
    *   `transaction_type` CHECK constraint: `transaction_type IN ('SIP', 'Lumpsum', 'Redemption')`
    *   `amount` CHECK constraint: `amount > 0`
    *   `units` CHECK constraint: `units > 0`
    *   `kyc_status` CHECK constraint: `kyc_status IN ('Verified', 'Failed', 'Pending')`
*   **Database Indexes:**
    *   `idx_fact_tx_scheme_date` on `(scheme_code, date_key)` for transaction analysis acceleration.

| Column Name | Data Type | Key Type | Database Constraints / Rules | Business Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `transaction_id` | TEXT | Primary Key | - | Unique transaction identifier (e.g. TXN10001). | `Data/processed/investor_transactions.csv` |
| `investor_id` | TEXT | - | NOT NULL | Unique identifier representing the investor. | `Data/processed/investor_transactions.csv` |
| `scheme_code` | INTEGER | Foreign Key | NOT NULL (Refs `dim_fund`) | Reference to the fund invested in. | `Data/processed/investor_transactions.csv` |
| `date_key` | TEXT | Foreign Key | NOT NULL (Refs `dim_date`) | Date of transaction. | `Data/processed/investor_transactions.csv` |
| `transaction_type`| TEXT | - | `CHECK (type IN ('SIP', 'Lumpsum', 'Redemption'))` | Type of transaction (SIP, Lumpsum, or Redemption). | `Data/processed/investor_transactions.csv` |
| `amount` | REAL | - | `CHECK (amount > 0)` | Value of the transaction in Indian Rupees (INR). | `Data/processed/investor_transactions.csv` |
| `units` | REAL | - | `CHECK (units > 0)` | Fund units purchased or redeemed during the transaction. | `Data/processed/investor_transactions.csv` |
| `kyc_status` | TEXT | - | `CHECK (kyc_status IN ('Verified', 'Failed', 'Pending'))` | KYC compliance status (Verified, Failed, or Pending). | `Data/processed/investor_transactions.csv` |
| `state` | TEXT | - | NOT NULL | Investor's state of residence in India. | `Data/processed/investor_transactions.csv` |

---

### 2.3 `fact_performance`
Stores historical return rates and expense metrics for each scheme.

*   **Database Constraints:**
    *   `expense_ratio` CHECK constraint: `expense_ratio >= 0.1 AND expense_ratio <= 2.5`

| Column Name | Data Type | Key Type | Database Constraints / Rules | Business Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `scheme_code` | INTEGER | Primary Key | References `dim_fund(scheme_code)` | Fund scheme identifier. | `Data/processed/scheme_performance.csv` |
| `return_1yr` | REAL | - | - | 1-year historical annualized return percentage (e.g. 12.5). | `Data/processed/scheme_performance.csv` |
| `return_3yr` | REAL | - | - | 3-year historical annualized return percentage. | `Data/processed/scheme_performance.csv` |
| `return_5yr` | REAL | - | - | 5-year historical annualized return percentage. | `Data/processed/scheme_performance.csv` |
| `expense_ratio` | REAL | - | `CHECK (expense_ratio BETWEEN 0.1 AND 2.5)` | Annual fee percentage charged to manage the fund. | `Data/processed/scheme_performance.csv` |

---

### 2.4 `fact_aum`
Stores Assets Under Management (AUM) snapshots.

*   **Database Constraints:**
    *   `aum_amount` CHECK constraint: `aum_amount > 0`
*   **Database Indexes:**
    *   `idx_fact_aum_scheme_date` on `(scheme_code, date_key)` for rapid AUM analysis joins.

| Column Name | Data Type | Key Type | Database Constraints / Rules | Business Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `aum_id` | INTEGER | Primary Key | Auto-incremented | Auto-incremented unique record identifier. | Internal DB |
| `scheme_code` | INTEGER | Foreign Key | NOT NULL (Refs `dim_fund`) | Fund scheme identifier. | `Data/processed/scheme_performance.csv` |
| `date_key` | TEXT | Foreign Key | NOT NULL (Refs `dim_date`) | Date of AUM value snapshot. | Generated (latest date) |
| `aum_amount` | REAL | - | `CHECK (aum_amount > 0)` | Total Assets Under Management of the scheme in Crores INR. | `Data/processed/scheme_performance.csv` |
