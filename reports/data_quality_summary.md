# Mutual Fund Data Ingestion Quality Report

## 1. Dataset Shape and Types

| Dataset | Rows | Columns | Duplicates | Missing Values | Anomalies |
| --- | --- | --- | --- | --- | --- |
| axis_bluechip_119092.csv | 3579 | 4 | 0 | None | None |
| fund_master.csv | 8 | 6 | 0 | None | None |
| hdfc_top_100_125497.csv | 3105 | 4 | 0 | None | None |
| hdfc_top_100_actual_119062.csv | 3313 | 4 | 0 | None | None |
| icici_bluechip_120503.csv | 3321 | 4 | 0 | None | None |
| kotak_bluechip_120841.csv | 3315 | 4 | 0 | None | None |
| nav_history.csv | 26491 | 3 | 0 | None | None |
| nippon_large_cap_118632.csv | 3312 | 4 | 0 | None | None |
| sbi_bluechip_119551.csv | 3250 | 4 | 0 | None | None |
| sbi_bluechip_actual_119777.csv | 3296 | 4 | 0 | None | None |

## 2. Fund Master Exploration

- **Total Fund Houses:** 7
- **Total Categories:** 4
- **Total Sub-categories:** 8
- **Total Risk Grades:** 2

### Scheme Categories:
- Equity Scheme
- Debt Scheme
- Hybrid Scheme
- Other Scheme

### Risk Grades:
- Very High
- Moderate

## 3. AMFI Code Validation Results

- **Unique scheme codes in `fund_master`:** 8
- **Unique scheme codes in `nav_history`:** 8
- **Status:** PASSED (All codes exist in history)
