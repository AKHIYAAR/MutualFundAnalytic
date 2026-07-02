import os
import sqlite3
import pandas as pd
import datetime

def generate_weekly_html_report():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(base_dir, 'Data', 'db', 'bluestock_mf.db')
    report_path = os.path.join(base_dir, 'reports', 'weekly_performance_summary.html')
    
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return
        
    conn = sqlite3.connect(db_path)
    
    # 1. Fetch Top 5 Funds by 3-Year Return
    query_top_funds = """
        SELECT df.scheme_code, df.scheme_name, df.category, fp.return_3yr, fp.expense_ratio
        FROM fact_performance fp
        JOIN dim_fund df ON fp.scheme_code = df.scheme_code
        ORDER BY fp.return_3yr DESC
        LIMIT 5
    """
    df_top = pd.read_sql_query(query_top_funds, conn)
    
    # 2. Fetch Latest Inflow/Outflow Statistics
    query_flows = """
        SELECT SUM(amount) as total_amount, transaction_type
        FROM fact_transactions
        GROUP BY transaction_type
    """
    df_flows = pd.read_sql_query(query_flows, conn)
    
    sip_total = df_flows[df_flows['transaction_type'] == 'SIP']['total_amount'].values[0] if not df_flows[df_flows['transaction_type'] == 'SIP'].empty else 0
    lump_total = df_flows[df_flows['transaction_type'] == 'Lumpsum']['total_amount'].values[0] if not df_flows[df_flows['transaction_type'] == 'Lumpsum'].empty else 0
    red_total = df_flows[df_flows['transaction_type'] == 'Redemption']['total_amount'].values[0] if not df_flows[df_flows['transaction_type'] == 'Redemption'].empty else 0
    
    # 3. Aggregate Demographic info
    query_demo = "SELECT COUNT(DISTINCT investor_id) as total_investors, AVG(sip_amount) as avg_sip FROM dim_investor"
    df_demo = pd.read_sql_query(query_demo, conn)
    total_investors = df_demo['total_investors'].values[0]
    avg_sip = df_demo['avg_sip'].values[0]
    
    conn.close()
    
    # Create HTML Content
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Bluestocks Weekly Mutual Fund Performance Summary</title>
  <style>
    body {{
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      background-color: #f3f4f6;
      color: #1f2937;
      margin: 0;
      padding: 20px;
    }}
    .container {{
      max-width: 600px;
      background: #ffffff;
      margin: 0 auto;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    .header {{
      text-align: center;
      border-bottom: 2px solid #3b82f6;
      padding-bottom: 20px;
      margin-bottom: 30px;
    }}
    .header h1 {{
      color: #1d4ed8;
      margin: 0;
      font-size: 24px;
    }}
    .header p {{
      color: #6b7280;
      margin: 5px 0 0 0;
      font-size: 14px;
    }}
    .section-title {{
      font-size: 18px;
      font-weight: bold;
      color: #111827;
      border-left: 4px solid #10b981;
      padding-left: 10px;
      margin-top: 30px;
      margin-bottom: 15px;
    }}
    .metric-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 15px;
      margin-bottom: 25px;
    }}
    .metric-card {{
      background: #f9fafb;
      padding: 15px;
      border-radius: 6px;
      border: 1px solid #e5e7eb;
      text-align: center;
    }}
    .metric-value {{
      font-size: 20px;
      font-weight: bold;
      color: #059669;
    }}
    .metric-label {{
      font-size: 12px;
      color: #6b7280;
      margin-top: 5px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 25px;
    }}
    th {{
      background-color: #3b82f6;
      color: white;
      text-align: left;
      padding: 10px;
      font-size: 13px;
    }}
    td {{
      border-bottom: 1px solid #e5e7eb;
      padding: 10px;
      font-size: 13px;
    }}
    tr:hover {{
      background-color: #f9fafb;
    }}
    .footer {{
      text-align: center;
      margin-top: 40px;
      font-size: 11px;
      color: #9ca3af;
      border-top: 1px solid #e5e7eb;
      padding-top: 20px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Weekly Portfolio & Flows Performance Report</h1>
      <p>Date Generated: {datetime.date.today().strftime('%B %d, %Y')}</p>
    </div>
    
    <div class="section-title">Key Portfolio Metrics</div>
    <div class="metric-grid">
      <div class="metric-card">
        <div class="metric-value">₹ {sip_total:,.2f}</div>
        <div class="metric-label">Total SIP Inflow Volume</div>
      </div>
      <div class="metric-card">
        <div class="metric-value">₹ {lump_total:,.2f}</div>
        <div class="metric-label">Total Lumpsum Volume</div>
      </div>
      <div class="metric-card">
        <div class="metric-value">{total_investors:,}</div>
        <div class="metric-label">Active Investors</div>
      </div>
      <div class="metric-card">
        <div class="metric-value">₹ {avg_sip:,.2f}</div>
        <div class="metric-label">Average Profile SIP Size</div>
      </div>
    </div>
    
    <div class="section-title">Top 5 Performing Schemes (3-Yr Return)</div>
    <table>
      <thead>
        <tr>
          <th>Scheme Code</th>
          <th>Scheme Name</th>
          <th>Category</th>
          <th>3-Yr Return</th>
          <th>Expense Ratio</th>
        </tr>
      </thead>
      <tbody>
    """
    
    for _, row in df_top.iterrows():
        html_content += f"""
        <tr>
          <td>{row['scheme_code']}</td>
          <td>{row['scheme_name']}</td>
          <td>{row['category']}</td>
          <td style="font-weight: bold; color: #059669;">{row['return_3yr']:.2f}%</td>
          <td>{row['expense_ratio']:.2f}%</td>
        </tr>
        """
        
    html_content += f"""
      </tbody>
    </table>
    
    <div class="section-title">Net Financial Flows Summary</div>
    <div class="metric-card" style="margin-bottom: 25px;">
      <div class="metric-value" style="color: #ef4444;">₹ {red_total:,.2f}</div>
      <div class="metric-label">Total Redemption (Outflow) Volume</div>
    </div>
    
    <div class="footer">
      <p>This is an automated investment analytics report. For inquiries, contact support@bluestocks.com</p>
      <p>&copy; {datetime.date.today().year} Bluestocks Inc. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
"""
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Weekly HTML report saved to: {report_path}")

if __name__ == '__main__':
    generate_weekly_html_report()
