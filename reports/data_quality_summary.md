# Mutual Fund Data Ingestion & Quality Report

## 1. Raw Dataset Properties

| Dataset | Rows | Columns | Duplicates | Missing Values | Anomalies (Daily Return > 50%) |
| --- | --- | --- | --- | --- | --- |
| axis_bluechip_119092.csv | 1826 | 4 | 0 | None | None |
| fund_master.csv | 40 | 6 | 0 | None | None |
| hdfc_top_100_125497.csv | 1826 | 4 | 0 | None | None |
| hdfc_top_100_actual_119062.csv | 1826 | 4 | 0 | None | None |
| icici_bluechip_120503.csv | 1826 | 4 | 0 | None | None |
| kotak_bluechip_120841.csv | 1826 | 4 | 0 | None | None |
| nav_history.csv | 73040 | 3 | 0 | None | None |
| nippon_large_cap_118632.csv | 1826 | 4 | 0 | None | None |
| sbi_bluechip_119551.csv | 1826 | 4 | 0 | None | None |
| sbi_bluechip_actual_119777.csv | 1826 | 4 | 0 | None | None |

## 2. Detailed Raw Data Anomalies Identified

No extreme anomalies detected in individual raw historical NAV files.


## 3. Cleaned Datasets Verification (Data/processed/)

The raw anomalies were corrected and saved to the `Data/processed/` folder for database ingestion. Below is the quality check on the cleaned files:

| Cleaned Dataset | Rows | Columns | Remaining Anomalies | Actions Taken |
| --- | --- | --- | --- | --- |
| axis_bluechip_119092.csv | 1826 | 4 | 0 | Multiplied NAV entries before 30-08-2015 by 100 to fix 100x shift. |
| hdfc_top_100_125497.csv | 1826 | 4 | 0 | Checked / No action needed |
| hdfc_top_100_actual_119062.csv | 1826 | 4 | 0 | Checked / No action needed |
| icici_bluechip_120503.csv | 1826 | 4 | 0 | Interpolated zero-NAV on 07-04-2013 using neighboring entries. |
| kotak_bluechip_120841.csv | 1826 | 4 | 0 | Checked / No action needed |
| nippon_large_cap_118632.csv | 1826 | 4 | 0 | Checked / No action needed |
| sbi_bluechip_119551.csv | 1826 | 4 | 0 | Checked / No action needed |
| sbi_bluechip_actual_119777.csv | 1826 | 4 | 0 | Checked / No action needed |
| nav_history.csv | 73040 | 3 | 0 | Applied both 100x shift and zero-NAV corrections per scheme. |
| fund_master.csv | 40 | 6 | 0 | Checked / No action needed |

## 4. Fund Master Exploration

- **Total Fund Houses:** 9
- **Total Categories:** 4
- **Total Sub-categories:** 14
- **Total Risk Grades:** 4

### Scheme Categories:
- Equity Scheme
- Debt Scheme
- Hybrid Scheme
- Other Scheme

### Risk Grades:
- Very High
- Moderate
- Low
- High

## 5. AMFI Code Validation Results

- **Unique scheme codes in `fund_master`:** 40
- **Unique scheme codes in `nav_history`:** 40
- **Status:** PASSED (All codes exist in history)
