import sqlite3
import pandas as pd
import numpy as np
import sys
import os

def load_data_and_recommend(risk_appetite: str):
    db_path = os.path.join(os.path.dirname(__file__), 'Data', 'processed', 'mutual_funds.db')
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}.")
        return None
    
    conn = sqlite3.connect(db_path)
    
    # 1. Fetch schemes and categories
    funds_df = pd.read_sql_query("SELECT scheme_code, scheme_name, category, risk_grade FROM dim_fund", conn)
    
    # 2. Fetch daily NAV and compute returns
    nav_df = pd.read_sql_query("SELECT scheme_code, date_key as date, nav FROM fact_nav", conn)
    conn.close()
    
    # Ensure correct sorting and datetime conversion
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    nav_df = nav_df.sort_values(['scheme_code', 'date'])
    
    # Compute returns
    nav_df['return'] = nav_df.groupby('scheme_code')['nav'].pct_change()
    returns_df = nav_df.dropna(subset=['return'])
    
    # 3. Calculate Sharpe ratio for all funds
    fund_sharpes = []
    for code, grp in returns_df.groupby('scheme_code'):
        returns = grp['return']
        mean_ret = returns.mean()
        std_ret = returns.std(ddof=0)
        # Annualized Sharpe: (mean / std) * sqrt(252)
        sharpe = (mean_ret / std_ret) * np.sqrt(252) if std_ret > 0 else np.nan
        fund_sharpes.append({
            'scheme_code': int(code),
            'Sharpe_Ratio': float(sharpe)
        })
    sharpe_df = pd.DataFrame(fund_sharpes)
    funds_with_sharpe = funds_df.merge(sharpe_df, on='scheme_code', how='left')
    
    # 4. Map risk appetite to risk grades
    risk_appetite = risk_appetite.strip().lower()
    if risk_appetite == 'low':
        target_grades = ['Low']
    elif risk_appetite == 'moderate':
        target_grades = ['Moderate']
    elif risk_appetite == 'high':
        # Include High and Very High
        target_grades = ['High', 'Very High']
    else:
        print(f"Error: Invalid risk appetite '{risk_appetite}'. Must be Low, Moderate, or High.")
        return None
    
    # Filter matching funds
    recommended = funds_with_sharpe[funds_with_sharpe['risk_grade'].isin(target_grades)].copy()
    
    # Sort by Sharpe Ratio descending
    recommended = recommended.sort_values('Sharpe_Ratio', ascending=False)
    
    # Take top 3
    top_3 = recommended.head(3)
    return top_3

def main():
    if len(sys.argv) > 1:
        risk_appetite = sys.argv[1]
    else:
        print("Simple Fund Recommender")
        print("=======================")
        risk_appetite = input("Enter your risk appetite (Low / Moderate / High): ")
    
    recommendations = load_data_and_recommend(risk_appetite)
    
    if recommendations is not None and not recommendations.empty:
        print(f"\nTop 3 Fund Recommendations for '{risk_appetite.upper()}' Risk Appetite:")
        print("=" * 90)
        
        # Display as Markdown-formatted table
        print(f"| {'Scheme Code':<12} | {'Scheme Name':<50} | {'Category':<15} | {'Risk Grade':<12} | {'Sharpe Ratio':<12} |")
        print(f"|{'-'*14}|{'-'*52}|{'-'*17}|{'-'*14}|{'-'*14}|")
        for _, row in recommendations.iterrows():
            name = row['scheme_name']
            if len(name) > 47:
                name = name[:44] + "..."
            print(f"| {row['scheme_code']:<12} | {name:<50} | {row['category']:<15} | {row['risk_grade']:<12} | {row['Sharpe_Ratio']:12.4f} |")
        print("=" * 90)
    elif recommendations is not None:
        print(f"No funds found matching '{risk_appetite}' risk appetite.")

if __name__ == '__main__':
    main()
