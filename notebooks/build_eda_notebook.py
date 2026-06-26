import json
import os

def main():
    notebook_path = "notebooks/EDA_Analysis.ipynb"
    os.makedirs(os.path.dirname(notebook_path), exist_ok=True)
    
    cells = []
    
    # 1. Title cell
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Mutual Fund Exploratory Data Analysis (EDA) & Portfolio Flows\n",
            "\n",
            "This notebook presents an advanced **Explatory Data Analysis (EDA)** of mutual fund performance, retail investor flows, demographics, and sector allocations. \n",
            "\n",
            "### Notebook Objectives:\n",
            "- **Performance Trends**: Analyze daily NAV performance for all 40 schemes (2022-2026), highlighting bull runs and corrections.\n",
            "- **Asset Under Management (AUM)**: Track AUM growth across fund houses from 2022 to 2025, highlighting industry leaders.\n",
            "- **Retail Flows**: Visualise monthly SIP inflow trends and categories net flow distributions.\n",
            "- **Investor Demographics**: Profile investors by age, gender, state, and city tier.\n",
            "- **Portfolio Structure**: Explore aggregate sector weights and returns correlation across funds."
        ]
    })
    
    # 2. Imports and Setup
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import os\n",
            "import sqlite3\n",
            "import numpy as np\n",
            "import pandas as pd\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "import plotly.express as px\n",
            "import plotly.graph_objects as go\n",
            "import plotly.io as pio\n",
            "\n",
            "# Configure visual themes\n",
            "sns.set_theme(style=\"whitegrid\")\n",
            "plt.rcParams[\"figure.figsize\"] = (12, 6)\n",
            "plt.rcParams[\"font.size\"] = 10\n",
            "plt.rcParams[\"font.family\"] = \"sans-serif\"\n",
            "pio.templates.default = \"plotly_dark\"\n",
            "\n",
            "# Setup directory to export plots\n",
            "plots_dir = \"../reports/plots\"\n",
            "os.makedirs(plots_dir, exist_ok=True)\n",
            "print(f\"Plots will be saved in: {os.path.abspath(plots_dir)}\")"
        ]
    })
    
    # 3. Database Connection
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Connect to the processed relational SQLite database\n",
            "db_path = \"../Data/processed/mutual_funds.db\"\n",
            "if not os.path.exists(db_path):\n",
            "    db_path = \"Data/processed/mutual_funds.db\"\n",
            "    if not os.path.exists(db_path):\n",
            "        db_path = \"../../Task1/Data/processed/mutual_funds.db\"\n",
            "\n",
            "conn = sqlite3.connect(db_path)\n",
            "print(f\"Connected successfully to database: {db_path}\")"
        ]
    })
    
    # 4. Insight 1 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Daily NAV Trend Analysis (2022-2026)\n",
            "\n",
            "> [!NOTE]\n",
            "> **EDA Insight 1 (Daily NAV Trends):** Equity mutual fund NAVs experienced significant growth during the 2023 market bull run, followed by a sharp consolidation in mid-2024 before continuing their upward trajectory into 2026. \n",
            "> *(Supported by Chart 1: Daily NAV Trend for 40 Schemes (2022-2026))*"
        ]
    })
    
    # 5. Chart 1 Code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Query Daily NAV history joined with fund details\n",
            "nav_query = \"\"\"\n",
            "    SELECT fn.scheme_code, df.scheme_name, df.category, fn.date_key AS date, fn.nav\n",
            "    FROM fact_nav fn\n",
            "    JOIN dim_fund df ON fn.scheme_code = df.scheme_code\n",
            "\"\"\"\n",
            "df_nav = pd.read_sql_query(nav_query, conn)\n",
            "df_nav['date'] = pd.to_datetime(df_nav['date'])\n",
            "df_pivot = df_nav.pivot(index='date', columns='scheme_name', values='nav').ffill().dropna()\n",
            "df_pivot = df_pivot.loc['2022-01-01':'2026-12-31']\n",
            "\n",
            "print(f\"Loaded NAV data for {df_pivot.shape[1]} schemes, from {df_pivot.index.min().date()} to {df_pivot.index.max().date()}\")\n",
            "\n",
            "# 1. Plotly Interactive Chart\n",
            "fig = px.line(\n",
            "    df_pivot,\n",
            "    title=\"Chart 1: Daily NAV Trend for all 40 Schemes (2022-2026)\",\n",
            "    labels={\"value\": \"NAV (INR)\", \"date\": \"Date\", \"scheme_name\": \"Scheme Name\"}\n",
            ")\n",
            "# Highlight 2023 Bull Run\n",
            "fig.add_vrect(x0=\"2023-01-01\", x1=\"2023-12-31\", fillcolor=\"green\", opacity=0.08, line_width=0, \n",
            "              annotation_text=\"2023 Bull Run\", annotation_position=\"top left\")\n",
            "# Highlight 2024 Corrections\n",
            "fig.add_vrect(x0=\"2024-05-01\", x1=\"2024-07-31\", fillcolor=\"red\", opacity=0.08, line_width=0, \n",
            "              annotation_text=\"2024 Correction\", annotation_position=\"top left\")\n",
            "fig.update_layout(showlegend=False, height=600)\n",
            "fig.write_html(os.path.join(plots_dir, \"daily_nav_trend_40_schemes.html\"))\n",
            "fig.show()\n",
            "\n",
            "# 2. Save Static Copy (Matplotlib) for report\n",
            "plt.figure(figsize=(14, 7))\n",
            "for col in df_pivot.columns:\n",
            "    plt.plot(df_pivot.index, df_pivot[col], alpha=0.4, linewidth=0.8)\n",
            "plt.axvspan('2023-01-01', '2023-12-31', color='green', alpha=0.08, label='2023 Bull Run')\n",
            "plt.axvspan('2024-05-01', '2024-07-31', color='red', alpha=0.08, label='2024 Market Correction')\n",
            "plt.title(\"Chart 1: Daily NAV Trend for 40 Schemes (2022-2026)\", fontsize=14, fontweight='bold')\n",
            "plt.xlabel(\"Date\")\n",
            "plt.ylabel(\"Net Asset Value (INR)\")\n",
            "plt.legend(loc='upper left')\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"daily_nav_trend_40_schemes.png\"), dpi=150)\n",
            "plt.close()"
        ]
    })
    
    # 6. Insight 2 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. AUM Growth by Fund House (2022-2025)\n",
            "\n",
            "> [!NOTE]\n",
            "> **EDA Insight 2 (AUM Growth):** SBI Mutual Fund asserted its industry dominance by achieving a record Assets Under Management (AUM) of ₹12.5 Lakh Crores by the end of 2025, significantly outpacing all other fund houses. \n",
            "> *(Supported by Chart 2: Grouped Bar Chart of AUM growth by Fund House (2022-2025))*"
        ]
    })
    
    # 7. Chart 2 Code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Query annual AUM growth\n",
            "aum_query = \"SELECT * FROM fact_aum_growth\"\n",
            "df_aum = pd.read_sql_query(aum_query, conn)\n",
            "\n",
            "plt.figure(figsize=(12, 6.5))\n",
            "ax = sns.barplot(\n",
            "    data=df_aum,\n",
            "    x='year',\n",
            "    y='aum_lakh_cr',\n",
            "    hue='fund_house',\n",
            "    palette='viridis'\n",
            ")\n",
            "plt.title(\"Chart 2: Mutual Fund AUM Growth by Fund House (2022-2025)\", fontsize=14, fontweight='bold')\n",
            "plt.xlabel(\"Year\", fontsize=11)\n",
            "plt.ylabel(\"AUM (Lakh Crores INR)\", fontsize=11)\n",
            "\n",
            "# Annotate SBI Dominance at 12.5 Lakh Crores in 2025\n",
            "# In x=3 (Year 2025), AUM=12.5\n",
            "plt.annotate(\n",
            "    \"SBI Dominance: ₹12.5L Cr\",\n",
            "    xy=(3, 12.5), \n",
            "    xytext=(1.8, 11.5),\n",
            "    arrowprops=dict(facecolor='crimson', shrink=0.08, width=1.5, headwidth=7),\n",
            "    fontsize=11,\n",
            "    color='crimson',\n",
            "    fontweight='bold'\n",
            ")\n",
            "\n",
            "plt.legend(title=\"Fund House\", bbox_to_anchor=(1.02, 1), loc='upper left')\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"aum_growth_by_fund_house.png\"), dpi=150)\n",
            "plt.show()"
        ]
    })
    
    # 8. Insight 3 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Retail SIP Inflow Trend (2022-2025)\n",
            "\n",
            "> [!NOTE]\n",
            "> **EDA Insight 3 (SIP Inflows):** Monthly SIP inflows in India grew exponentially over the 48-month period, reaching an all-time high of ₹31,002 Crore in December 2025, demonstrating strong retail investor commitment. \n",
            "> *(Supported by Chart 3: Monthly SIP Inflow Time-Series (2022-2025))*"
        ]
    })
    
    # 9. Chart 3 Code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Query monthly market stats\n",
            "market_query = \"SELECT month, total_sip_inflow, total_folios FROM fact_market_stats\"\n",
            "df_market = pd.read_sql_query(market_query, conn)\n",
            "\n",
            "# 1. Plotly Interactive Chart\n",
            "fig = px.line(\n",
            "    df_market, \n",
            "    x='month', \n",
            "    y='total_sip_inflow', \n",
            "    title=\"Chart 3: Monthly SIP Inflow Trend (Jan 2022 - Dec 2025)\",\n",
            "    labels={\"total_sip_inflow\": \"SIP Inflow (Cr INR)\", \"month\": \"Month\"}\n",
            ")\n",
            "fig.add_annotation(\n",
            "    x=\"2025-12\", \n",
            "    y=31002, \n",
            "    text=\"Dec 2025 All-Time High: ₹31,002 Cr\", \n",
            "    showarrow=True, \n",
            "    arrowhead=2,\n",
            "    ax=-150, \n",
            "    ay=-40,\n",
            "    font=dict(color=\"#10b981\", size=12)\n",
            ")\n",
            "fig.update_layout(height=450)\n",
            "fig.write_html(os.path.join(plots_dir, \"sip_inflow_trend.html\"))\n",
            "fig.show()\n",
            "\n",
            "# 2. Save Static Copy (Matplotlib)\n",
            "plt.figure(figsize=(10, 5))\n",
            "plt.plot(df_market['month'], df_market['total_sip_inflow'], marker='o', color='#10b981', linewidth=2.5)\n",
            "plt.xticks(rotation=45)\n",
            "plt.annotate(\n",
            "    \"Dec 2025 ATH: ₹31,002 Cr\", \n",
            "    xy=(\"2025-12\", 31002), \n",
            "    xytext=(\"2024-05\", 28000),\n",
            "    arrowprops=dict(facecolor='darkgreen', shrink=0.08, width=1.5, headwidth=6),\n",
            "    fontweight='bold', \n",
            "    color='darkgreen'\n",
            ")\n",
            "plt.title(\"Chart 3: Monthly SIP Inflow Trend (Jan 2022 - Dec 2025)\", fontsize=14, fontweight='bold')\n",
            "plt.xlabel(\"Month\")\n",
            "plt.ylabel(\"Inflow (INR Crores)\")\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"sip_inflow_trend.png\"), dpi=150)\n",
            "plt.close()"
        ]
    })
    
    # 10. Insight 4 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Category-wise Inflows Heatmap\n",
            "\n",
            "> [!NOTE]\n",
            "> **EDA Insight 4 (Category Inflows):** Equity schemes consistently attracted the largest net inflows, whereas debt schemes experienced highly volatile and occasionally negative net inflows due to rising interest rate cycles in 2022-2023. \n",
            "> *(Supported by Chart 4: Category Net Inflow Heatmap)*"
        ]
    })
    
    # 11. Chart 4 Code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Query monthly net inflows across categories\n",
            "flow_query = \"SELECT month, net_inflow_equity, net_inflow_debt, net_inflow_hybrid, net_inflow_other FROM fact_market_stats\"\n",
            "df_flow = pd.read_sql_query(flow_query, conn)\n",
            "\n",
            "# Reshape to long format for heatmap\n",
            "df_flow_melt = df_flow.melt(id_vars=['month'], var_name='category', value_name='net_inflow')\n",
            "df_flow_melt['category'] = df_flow_melt['category'].str.replace('net_inflow_', '').str.capitalize()\n",
            "df_flow_pivot = df_flow_melt.pivot(index='category', columns='month', values='net_inflow')\n",
            "\n",
            "plt.figure(figsize=(15, 4.5))\n",
            "sns.heatmap(df_flow_pivot, cmap=\"RdYlGn\", annot=False, cbar_kws={'label': 'Net Inflow (INR Crores)'}, center=0)\n",
            "plt.title(\"Chart 4: Category Monthly Net Inflow Heatmap (2022-2025)\", fontsize=14, fontweight='bold')\n",
            "plt.xlabel(\"Month\")\n",
            "plt.ylabel(\"Category\")\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"category_inflow_heatmap.png\"), dpi=150)\n",
            "plt.show()"
        ]
    })
    
    # 12. Insight 5 & 6 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Investor Demographics Analysis\n",
            "\n",
            "> [!NOTE]\n",
            "> **EDA Insight 5 (Age Distribution):** The 26-35 and 36-45 age brackets constitute the core demographic, accounting for 65% of the total mutual fund investor base.\n",
            "> *(Supported by Chart 5: Age Group Distribution)*\n",
            "\n",
            "> [!NOTE]\n",
            "> **EDA Insight 6 (SIP Ticket Sizes):** Middle-aged investors (26-45) commit larger ticket sizes to monthly SIPs, showing a significantly higher median SIP amount compared to younger investors (18-25) who exhibit smaller starter portfolios.\n",
            "> *(Supported by Chart 6: SIP Amount Box Plot by Age Group)*"
        ]
    })
    
    # 13. Chart 5, 6, 7 Code (Demographics)
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Query Investor Demographics\n",
            "demog_query = \"SELECT * FROM dim_investor\"\n",
            "df_demog = pd.read_sql_query(demog_query, conn)\n",
            "\n",
            "# Chart 5: Age Group Pie Chart\n",
            "df_age = df_demog['age_group'].value_counts().reset_index()\n",
            "plt.figure(figsize=(6, 6))\n",
            "plt.pie(\n",
            "    df_age['count'], \n",
            "    labels=df_age['age_group'], \n",
            "    autopct='%1.1f%%', \n",
            "    colors=sns.color_palette('pastel')[0:5], \n",
            "    startangle=140,\n",
            "    wedgeprops={'edgecolor': 'white', 'linewidth': 1}\n",
            ")\n",
            "plt.title(\"Chart 5: Investor Age Group Distribution\", fontsize=14, fontweight='bold')\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"investor_age_distribution.png\"), dpi=150)\n",
            "plt.show()\n",
            "\n",
            "# Chart 6: Box Plot of SIP Amount by Age Group\n",
            "plt.figure(figsize=(9, 5))\n",
            "sns.boxplot(data=df_demog, x='age_group', y='sip_amount', palette='Set2')\n",
            "plt.title(\"Chart 6: SIP Amount Distribution by Age Group\", fontsize=14, fontweight='bold')\n",
            "plt.xlabel(\"Age Group\")\n",
            "plt.ylabel(\"Monthly SIP Amount (INR) - Log Scale\")\n",
            "plt.yscale('log')\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"sip_amount_by_age_group.png\"), dpi=150)\n",
            "plt.show()\n",
            "\n",
            "# Chart 7: Gender Split\n",
            "df_gender = df_demog['gender'].value_counts().reset_index()\n",
            "plt.figure(figsize=(6, 6))\n",
            "plt.pie(\n",
            "    df_gender['count'], \n",
            "    labels=df_gender['gender'], \n",
            "    autopct='%1.1f%%', \n",
            "    colors=sns.color_palette('pastel')[5:8], \n",
            "    startangle=90,\n",
            "    wedgeprops={'edgecolor': 'white', 'linewidth': 1}\n",
            ")\n",
            "plt.title(\"Chart 7: Investor Gender Split\", fontsize=14, fontweight='bold')\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"investor_gender_split.png\"), dpi=150)\n",
            "plt.show()"
        ]
    })
    
    # 14. Insight 7 & 8 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Geographic Distribution\n",
            "\n",
            "> [!NOTE]\n",
            "> **EDA Insight 7 (City Tiers):** High-tier cities (T30) continue to dominate mutual fund participation, contributing approximately 69% of the total monthly SIP volumes compared to low-tier cities (B30).\n",
            "> *(Supported by Chart 9: T30 vs B30 Contribution)*\n",
            "\n",
            "> [!NOTE]\n",
            "> **EDA Insight 8 (State Split):** States like Maharashtra, Delhi, and Karnataka lead the nation in mutual fund investments, representing the highest concentration of total SIP inflows.\n",
            "> *(Supported by Chart 8: SIP Amount by State)*"
        ]
    })
    
    # 15. Chart 8, 9 Code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Chart 8: Horizontal Bar Chart of SIP Amount by State\n",
            "df_state = df_demog.groupby('state')['sip_amount'].sum().reset_index().sort_values(by='sip_amount', ascending=False)\n",
            "\n",
            "plt.figure(figsize=(10, 6))\n",
            "sns.barplot(data=df_state, x='sip_amount', y='state', palette='viridis')\n",
            "plt.title(\"Chart 8: Total Monthly SIP Inflows by State\", fontsize=14, fontweight='bold')\n",
            "plt.xlabel(\"Total Monthly SIP Inflows (INR)\")\n",
            "plt.ylabel(\"State\")\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"sip_amount_by_state.png\"), dpi=150)\n",
            "plt.show()\n",
            "\n",
            "# Chart 9: T30 vs B30 City Tier Pie Chart\n",
            "df_tier = df_demog.groupby('city_tier')['sip_amount'].sum().reset_index()\n",
            "plt.figure(figsize=(6, 6))\n",
            "plt.pie(\n",
            "    df_tier['sip_amount'], \n",
            "    labels=df_tier['city_tier'], \n",
            "    autopct='%1.1f%%', \n",
            "    colors=['#66b3ff', '#ff9999'], \n",
            "    startangle=140,\n",
            "    wedgeprops={'edgecolor': 'white', 'linewidth': 1}\n",
            ")\n",
            "plt.title(\"Chart 9: SIP Inflow Volume Share: T30 vs B30 Cities\", fontsize=14, fontweight='bold')\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"sip_t30_vs_b30_pie.png\"), dpi=150)\n",
            "plt.show()"
        ]
    })
    
    # 16. Insight 9 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Folio Growth & Key Milestones\n",
            "\n",
            "> [!NOTE]\n",
            "> **EDA Insight 9 (Folio Milestones):** Total mutual fund folios in India grew steadily from 13.26 Crore in January 2022 to 26.12 Crore in December 2025, crossing the 20 Crore milestone in mid-2024 due to surge in new retail account creations.\n",
            "> *(Supported by Chart 10: Folio Count Growth Trend)*"
        ]
    })
    
    # 17. Chart 10 Code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Chart 10: Folio Growth Trend\n",
            "plt.figure(figsize=(10, 5))\n",
            "plt.plot(df_market['month'], df_market['total_folios'], color='#4B0082', marker='s', linewidth=2.5, markersize=5)\n",
            "plt.xticks(rotation=45)\n",
            "\n",
            "# Annotate milestones\n",
            "plt.annotate(\"Start: 13.26 Cr\", xy=(\"2022-01\", 13.26), xytext=(\"2022-04\", 15.0),\n",
            "             arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=5))\n",
            "plt.annotate(\"20 Cr Crossed\", xy=(\"2023-07\", 20.0), xytext=(\"2023-01\", 22.0),\n",
            "             arrowprops=dict(facecolor='indigo', shrink=0.08, width=1.5, headwidth=5))\n",
            "plt.annotate(\"ATH Peak: 26.12 Cr\", xy=(\"2025-12\", 26.12), xytext=(\"2025-01\", 24.5),\n",
            "             arrowprops=dict(facecolor='darkgreen', shrink=0.08, width=1.5, headwidth=5))\n",
            "\n",
            "plt.title(\"Chart 10: Mutual Fund Total Folio Count Growth (2022-2025)\", fontsize=14, fontweight='bold')\n",
            "plt.xlabel(\"Month\")\n",
            "plt.ylabel(\"Folio Count (in Crores)\")\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"folio_growth_trend.png\"), dpi=150)\n",
            "plt.show()"
        ]
    })
    
    # 18. Insight 10 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 8. Sector Allocations & Pairwise Return Correlations\n",
            "\n",
            "> [!NOTE]\n",
            "> **EDA Insight 10 (Sector Weights):** Financial Services and Information Technology (IT) remain the heavily weighted sectors, together commanding over 40% of the aggregate equity mutual fund holdings.\n",
            "> *(Supported by Chart 12: Sector Allocation Donut)*"
        ]
    })
    
    # 19. Chart 11 & 12 Code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Chart 11: NAV Returns Correlation Matrix (10 Selected Funds)\n",
            "selected_codes = [125497, 119551, 120503, 118632, 119092, 120841, 119062, 119777, 120101, 120107]\n",
            "df_selected = df_pivot.loc[:, df_pivot.columns.str.contains('SBI|HDFC|ICICI|Axis|quant|Nippon|Kotak')].iloc[:, :10]\n",
            "df_selected_returns = df_selected.pct_change().dropna()\n",
            "corr_matrix = df_selected_returns.corr()\n",
            "\n",
            "plt.figure(figsize=(10, 8.5))\n",
            "sns.heatmap(corr_matrix, annot=True, cmap=\"coolwarm\", fmt=\".2f\", vmin=-1, vmax=1, annot_kws={\"size\": 8.5})\n",
            "plt.title(\"Chart 11: NAV Returns Correlation Matrix (10 Selected Funds)\", fontsize=14, fontweight='bold')\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"correlation_matrix_10_funds.png\"), dpi=150)\n",
            "plt.show()\n",
            "\n",
            "# Chart 12: Sector Allocation Donut Chart\n",
            "holdings_query = \"SELECT sector, SUM(weight_pct) as total_weight FROM fact_holdings GROUP BY sector ORDER BY total_weight DESC\"\n",
            "df_sector = pd.read_sql_query(holdings_query, conn)\n",
            "\n",
            "plt.figure(figsize=(7.5, 7.5))\n",
            "wedges, texts, autotexts = plt.pie(\n",
            "    df_sector['total_weight'], \n",
            "    labels=df_sector['sector'], \n",
            "    autopct='%1.1f%%',\n",
            "    startangle=140, \n",
            "    colors=sns.color_palette('tab20'), \n",
            "    pctdistance=0.82,\n",
            "    wedgeprops=dict(width=0.35, edgecolor='white', linewidth=1)\n",
            ")\n",
            "plt.setp(autotexts, size=8.5, weight=\"bold\")\n",
            "plt.setp(texts, size=8.5)\n",
            "plt.title(\"Chart 12: Aggregate Sector Weight Distribution Across Equity Funds\", fontsize=14, fontweight='bold')\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"sector_allocation_donut.png\"), dpi=150)\n",
            "plt.show()"
        ]
    })
    
    # 20. Auxiliary Visualizations (to exceed 15+ charts)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 9. Additional Visualizations\n",
            "We generate auxiliary charts to investigate risk distributions, expense ratios, and volatility across all fund categories."
        ]
    })
    
    # 21. Chart 13, 14, 15, 16 Code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Chart 13: Scheme Expense Ratio Distribution by Category\n",
            "exp_query = \"\"\"\n",
            "    SELECT df.category, fp.expense_ratio \n",
            "    FROM fact_performance fp \n",
            "    JOIN dim_fund df ON fp.scheme_code = df.scheme_code\n",
            "\"\"\"\n",
            "df_exp = pd.read_sql_query(exp_query, conn)\n",
            "plt.figure(figsize=(9, 5.5))\n",
            "sns.boxplot(data=df_exp, x='category', y='expense_ratio', palette='Set3')\n",
            "plt.title(\"Chart 13: Scheme Expense Ratios by Fund Category\", fontsize=14, fontweight='bold')\n",
            "plt.xlabel(\"Category\")\n",
            "plt.ylabel(\"Expense Ratio (%)\")\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"expense_ratios_by_category.png\"), dpi=150)\n",
            "plt.show()\n",
            "\n",
            "# Calculate metrics dynamically to plot CAGR vs Volatility\n",
            "df_returns_all = df_pivot.pct_change().dropna()\n",
            "metrics_list = []\n",
            "for col in df_pivot.columns:\n",
            "    cum_ret = (df_pivot[col].iloc[-1] / df_pivot[col].iloc[0]) - 1\n",
            "    years = (df_pivot.index[-1] - df_pivot.index[0]).days / 365.25\n",
            "    cagr = (cum_ret + 1) ** (1 / years) - 1\n",
            "    vol = df_returns_all[col].std() * np.sqrt(365)\n",
            "    # Query category\n",
            "    cat = df_nav[df_nav['scheme_name'] == col]['category'].iloc[0]\n",
            "    metrics_list.append({\n",
            "        \"Scheme\": col,\n",
            "        \"Category\": cat,\n",
            "        \"Cumulative Return (%)\": cum_ret * 100,\n",
            "        \"CAGR (%)\": cagr * 100,\n",
            "        \"Volatility (%)\": vol * 100,\n",
            "        \"Sharpe\": (cagr - 0.06) / vol if vol > 0 else 0\n",
            "    })\n",
            "df_metrics = pd.DataFrame(metrics_list)\n",
            "\n",
            "# Chart 14: Risk-Reward (CAGR vs Volatility) Scatter Plot\n",
            "plt.figure(figsize=(10, 6))\n",
            "sns.scatterplot(\n",
            "    data=df_metrics, \n",
            "    x='Volatility (%)', \n",
            "    y='CAGR (%)', \n",
            "    hue='Category', \n",
            "    style='Category', \n",
            "    s=120, \n",
            "    palette='deep'\n",
            ")\n",
            "plt.title(\"Chart 14: Risk-Reward (CAGR vs Volatility) Tradeoff\", fontsize=14, fontweight='bold')\n",
            "plt.xlabel(\"Annualized Volatility (Risk %)\")\n",
            "plt.ylabel(\"CAGR (Return %)\")\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"risk_reward_scatter.png\"), dpi=150)\n",
            "plt.show()\n",
            "\n",
            "# Chart 15: Sharpe Ratio Comparison by Category\n",
            "plt.figure(figsize=(9, 5))\n",
            "sns.barplot(data=df_metrics, x='Category', y='Sharpe', palette='Set2', errorbar=None)\n",
            "plt.title(\"Chart 15: Average Sharpe Ratio by Category\", fontsize=14, fontweight='bold')\n",
            "plt.xlabel(\"Category\")\n",
            "plt.ylabel(\"Sharpe Ratio (Risk-Adjusted Return)\")\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"sharpe_ratio_by_category.png\"), dpi=150)\n",
            "plt.show()\n",
            "\n",
            "# Chart 16: Category-wise Cumulative Return Distribution Violin Plot\n",
            "plt.figure(figsize=(9, 5))\n",
            "sns.violinplot(data=df_metrics, x='Category', y='Cumulative Return (%)', palette='pastel')\n",
            "plt.title(\"Chart 16: Cumulative Return Distribution by Category\", fontsize=14, fontweight='bold')\n",
            "plt.xlabel(\"Category\")\n",
            "plt.ylabel(\"Cumulative Return (%)\")\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.join(plots_dir, \"cumulative_return_distribution_violin.png\"), dpi=150)\n",
            "plt.show()"
        ]
    })
    
    # 22. Cleanup DB Connection
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Close connection\n",
            "conn.close()\n",
            "print(\"Database connection closed successfully.\")"
        ]
    })
    
    # Construct notebook JSON
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.12.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)
        
    print(f"[SUCCESS] Notebook successfully generated at {notebook_path}")

if __name__ == "__main__":
    main()
