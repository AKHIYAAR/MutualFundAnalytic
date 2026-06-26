# Mutual Fund Analytics Project

## Project Overview

The **Mutual Fund Analytics Project** is an end-to-end data analytics solution designed to analyze, compare, and visualize mutual fund performance using historical NAV data, fund metadata, and live market information. The project leverages Python, SQL, APIs, data visualization libraries, and dashboarding tools to provide actionable insights into fund performance, risk, and investment trends.

### Project Goals

* Collect and integrate mutual fund data from multiple sources.
* Fetch live NAV data using MFAPI.
* Perform data cleaning, preprocessing, and validation.
* Analyze fund performance across categories and fund houses.
* Calculate key financial metrics and risk indicators.
* Build interactive dashboards for investors and analysts.
* Generate reports and insights for investment decision-making.

---

# Day 1: Project Setup, Data Ingestion & Data Validation

## Objective

Establish the project foundation by setting up the development environment, organizing project files, importing datasets, integrating external APIs, and performing an initial assessment of data quality.

---

## 1. Project Structure Creation

A well-organized folder structure is essential for scalability and maintainability.

### Folder Structure

```text
MutualFundAnalytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── sql/
│
├── dashboard/
│
├── reports/
│
├── data_ingestion.py
├── live_nav_fetch.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Purpose of Each Folder

| Folder         | Purpose                                           |
| -------------- | ------------------------------------------------- |
| data/raw       | Original datasets collected from external sources |
| data/processed | Cleaned and transformed datasets                  |
| notebooks      | Jupyter notebooks for EDA and experimentation     |
| sql            | Database scripts and SQL queries                  |
| dashboard      | Dashboard application files                       |
| reports        | Data quality reports and analytical reports       |

---

## 2. Git and GitHub Initialization

Version control is established to track project changes.

### Commands

```bash
git init
git remote add origin <repository-url>
```

### Benefits

* Track project progress
* Enable collaboration
* Maintain backup of work
* Manage version history

---

## 3. Python Environment Setup

### Libraries Installed

```bash
pip install pandas numpy matplotlib seaborn plotly sqlalchemy requests scipy jupyter
```

### Purpose of Libraries

| Library    | Purpose                        |
| ---------- | ------------------------------ |
| Pandas     | Data manipulation and analysis |
| NumPy      | Numerical computations         |
| Matplotlib | Data visualization             |
| Seaborn    | Statistical visualization      |
| Plotly     | Interactive charts             |
| SQLAlchemy | Database connectivity          |
| Requests   | API integration                |
| SciPy      | Statistical analysis           |
| Jupyter    | Exploratory analysis           |

### Generate Requirements File

```bash
pip freeze > requirements.txt
```

---

## 4. Data Ingestion

All provided CSV datasets are imported into Python using Pandas.

### Activities

* Read all datasets
* Verify successful loading
* Store metadata
* Create ingestion logs

### Validation Performed

For every dataset:

```python
df.shape
df.dtypes
df.head()
```

### Additional Checks

```python
df.isnull().sum()
df.duplicated().sum()
```

### Outputs

* Total rows and columns
* Data type distribution
* Missing values report
* Duplicate records report

---

## 5. Live NAV Data Collection

To supplement historical datasets, real-time NAV data is fetched using MFAPI.

### API Endpoint

```text
https://api.mfapi.in/mf/125497
```

### Information Collected

* Scheme Name
* Scheme Code
* NAV Value
* NAV Date
* Historical NAV Series

### Storage

Saved to:

```text
data/raw/HDFC_Top100_Live_NAV.csv
```

---

## 6. Multi-Fund NAV Collection

Historical NAV data collected for:

| Fund                | AMFI Code |
| ------------------- | --------- |
| HDFC Top 100 Direct | 125497    |
| SBI Bluechip        | 119551    |
| ICICI Bluechip      | 120503    |
| Nippon Large Cap    | 118632    |
| Axis Bluechip       | 119092    |
| Kotak Bluechip      | 120841    |

### Purpose

* Cross-fund comparison
* Performance benchmarking
* Trend analysis

---

## 7. Fund Master Exploration

Analyze the fund master dataset to understand the mutual fund universe.

### Analysis Performed

#### Fund Houses

Examples:

* HDFC Mutual Fund
* SBI Mutual Fund
* ICICI Prudential Mutual Fund
* Nippon India Mutual Fund
* Kotak Mutual Fund

#### Categories

Examples:

* Equity
* Debt
* Hybrid
* Solution Oriented

#### Sub-Categories

Examples:

* Large Cap
* Mid Cap
* Small Cap
* Multi Cap
* ELSS

#### Risk Grades

Examples:

* Low
* Moderate
* Moderately High
* High
* Very High

---

## 8. Data Quality Validation

### Checks Performed

#### Missing Values

Identify incomplete records.

#### Duplicate Records

Detect duplicate scheme entries.

#### Invalid Data Types

Verify:

* Dates
* Numeric NAV values
* Scheme codes

#### Scheme Code Validation

Compare:

```text
fund_master.scheme_code
vs
nav_history.scheme_code
```

### Data Quality Report

Created in:

```text
reports/data_quality_summary.md
```

---

## Deliverables

* Project Structure
* GitHub Repository
* requirements.txt
* data_ingestion.py
* live_nav_fetch.py
* Data Quality Report

---

# Day 2: Data Cleaning, Exploratory Data Analysis & Mutual Fund Performance Analytics

## Objective

Transform raw datasets into analysis-ready datasets and uncover meaningful insights using exploratory data analysis techniques.

---

## 1. Data Cleaning

### Missing Value Treatment

Methods used:

* Mean Imputation
* Median Imputation
* Mode Replacement
* Record Removal

### Duplicate Removal

```python
df.drop_duplicates()
```

### Date Standardization

Convert:

```python
pd.to_datetime()
```

### Data Type Correction

Examples:

* NAV → float
* Dates → datetime
* Scheme Code → integer

### Export Clean Dataset

```text
data/processed/
```

---

## 2. Exploratory Data Analysis (EDA)

### Fund Distribution Analysis

Questions Answered:

* Which fund house offers the most schemes?
* Which category dominates the market?
* Which risk category is most common?

### Visualizations Created

* Bar Charts
* Pie Charts
* Histograms
* Box Plots
* Heatmaps

---

## 3. NAV Trend Analysis

### Objectives

Analyze historical NAV growth.

### Insights

* Long-term growth patterns
* Volatility periods
* Market corrections

### Visualizations

* NAV Time Series
* Rolling Average Charts

---

## 4. Fund House Comparison

Compare:

* Number of schemes
* Average NAV
* Growth trends
* Category diversification

---

## 5. Return Analysis

### Calculations

#### Absolute Return

```text
(Current NAV - Initial NAV)
/ Initial NAV × 100
```

#### CAGR

```text
[(Ending Value / Beginning Value)
^(1 / Years)] - 1
```

#### Annualized Returns

Evaluate long-term performance.

---

## 6. Category-Level Analysis

Compare:

* Large Cap Funds
* Mid Cap Funds
* Small Cap Funds
* Hybrid Funds

### Metrics

* Average Return
* Average Risk
* Fund Count

---

## Deliverables

* Cleaned Datasets
* EDA Notebook
* Performance Analysis Notebook
* Visualizations
* EDA Report

---

# Day 3: Risk Analytics, SQL Integration, Dashboard Development & Reporting

## Objective

Perform advanced financial analysis, create a database-driven workflow, and build a dashboard for decision-making.

---

## 1. SQL Database Integration

### Database Creation

Store processed datasets.

### Tables

* fund_master
* nav_history
* category_master
* risk_master
* performance_metrics

### Benefits

* Efficient querying
* Scalability
* Faster analysis

---

## 2. Advanced Risk Analytics

### Volatility

Measures NAV fluctuations.

### Sharpe Ratio

```text
(Return - Risk Free Rate)
/ Standard Deviation
```

Measures risk-adjusted return.

### Sortino Ratio

Focuses only on downside risk.

### Beta

Measures market sensitivity.

### Alpha

Measures excess returns relative to benchmark.

---

## 3. Benchmark Comparison

Compare mutual funds against benchmark indices.

### Metrics

* Relative Returns
* Tracking Error
* Outperformance Rate

---

## 4. Dashboard Development

### Dashboard Features

#### Fund Search

Search funds using scheme code.

#### NAV Visualization

Interactive trend analysis.

#### Fund Comparison

Compare multiple schemes simultaneously.

#### Risk-Return Scatter Plot

Visualize investment opportunities.

#### Category Analytics

Category-wise performance analysis.

### Tools

* Plotly
* Dash / Streamlit
* SQL Backend

---

## 5. Business Insights & Recommendations

Generate investment insights such as:

* Top-performing funds
* Most consistent performers
* High-risk, high-return opportunities
* Category leaders
* Fund house rankings

---

## 6. Final Reporting

Reports generated:

### Technical Report

Includes:

* Architecture
* Data pipeline
* Methodology

### Business Report

Includes:

* Key findings
* Performance rankings
* Risk assessments

### Dashboard Documentation

Explains dashboard functionality and usage.

---

# Final Deliverables

## Source Code

* data_ingestion.py
* live_nav_fetch.py
* data_cleaning.py
* performance_analysis.py
* risk_analysis.py

## Data Assets

* Raw datasets
* Processed datasets
* Live NAV data

## Documentation

* README.md
* Data Quality Report
* EDA Report
* Final Analytics Report

## Database Assets

* SQL Scripts
* Database Schema

## Visualization Assets

* Charts
* Dashboards
* Comparative Analytics

## GitHub Milestones

### Day 1 Commit

```bash
git commit -m "Day 1: Data ingestion complete"
```

### Day 2 Commit

```bash
git commit -m "Day 2: Data cleaning and analytics complete"
```

### Day 3 Commit

```bash
git commit -m "Day 3: Dashboard and reporting complete"
```

### Day 3 (Continued): Advanced EDA & Interactive Visualizations

```bash
git commit -m "Day 3: Advanced EDA Analysis notebook with 16 charts, SQLite schema extension, pre-processing automation, and dynamic dashboard styling"
```

#### Objective
Expand the analytics database to support comprehensive demographic, geographic, and holdings analyses, construct a quantitative Jupyter notebook with 16 Plotly & Seaborn visualisations, and integrate dynamic style modifications into the local web application.

#### Key Enhancements
*   **40 Scheme Expansion**: Simulated a synchronized market cycle dataset across 40 funds (Equity, Debt, Hybrid, and Other) from 2022 to 2026.
*   **Database Scaling**: Modified `sql/schema.sql` and `sql_database_setup.py` to ingest:
    *   `dim_investor`: Investor demographic profiles (age groups, genders, monthly ticket sizes).
    *   `fact_holdings`: Individual fund sector allocations and weights.
    *   `fact_market_stats`: Monthly retail flows (SIP inflows & folios).
    *   `fact_aum_growth`: Grouped AUM by year (2022-2025).
*   **Quantitative Notebook (`notebooks/EDA_Analysis.ipynb`)**: Developed 16 detailed plots (Plotly/Seaborn) analyzing cumulative returns, monthly SIP timelines (peaking at ₹31,002 Cr in Dec 2025), folio growth (to 26.12 Cr), state-wise participation, correlation matrix of returns, and sector donuts.
*   **10 Documented Insights**: Authored markdown cells inside the notebook containing precise investment observations and direct chart references.
*   **Dynamic Color Assignment**: Rewrote color mapping in `dashboard/app.js` with a dynamic hashing function `getSchemeColor()` to render 40 schemes beautifully in the UI.

---

This completes the end-to-end Mutual Fund Analytics project lifecycle, covering data acquisition, preprocessing, exploratory analysis, financial performance evaluation, risk assessment, database star schema loading, quantitative reporting, and dynamic dashboard developments.

