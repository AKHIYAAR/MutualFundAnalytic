import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize

def run_portfolio_optimization_and_simulation():
    # Setup paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(base_dir, 'Data', 'db', 'bluestock_mf.db')
    plots_dir = os.path.join(base_dir, 'reports', 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return
        
    conn = sqlite3.connect(db_path)
    
    # 1. Fetch returns for 5 key funds
    key_funds = [125497, 118632, 120503, 119092, 120841]
    
    query = """
        SELECT fn.scheme_code, df.scheme_name, fn.date_key AS date, fn.nav
        FROM fact_nav fn
        JOIN dim_fund df ON fn.scheme_code = df.scheme_code
        WHERE fn.scheme_code IN (?, ?, ?, ?, ?)
    """
    df = pd.read_sql_query(query, conn, params=key_funds)
    conn.close()
    
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['scheme_code', 'date'])
    df['return'] = df.groupby('scheme_code')['nav'].pct_change()
    df_returns = df.dropna(subset=['return'])
    
    # Pivot returns to get columns as scheme_codes
    pivot_returns = df_returns.pivot(index='date', columns='scheme_code', values='return').dropna()
    print("Pivoted returns shape:", pivot_returns.shape)
    
    # Mean annualized returns and covariance
    mean_daily_returns = pivot_returns.mean()
    cov_daily_matrix = pivot_returns.cov()
    
    ann_returns = mean_daily_returns * 252
    ann_cov = cov_daily_matrix * 252
    
    num_assets = len(key_funds)
    
    # Helper functions for portfolio optimization
    def portfolio_performance(weights, returns, cov_matrix):
        port_ret = np.sum(returns * weights)
        port_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return port_ret, port_std
        
    def neg_sharpe_ratio(weights, returns, cov_matrix, risk_free_rate=0.065):
        p_ret, p_std = portfolio_performance(weights, returns, cov_matrix)
        return -(p_ret - risk_free_rate) / p_std
        
    # Maximise Sharpe Ratio
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    initial_weights = num_assets * [1. / num_assets,]
    
    opt_sharpe = minimize(neg_sharpe_ratio, initial_weights, 
                          args=(ann_returns, ann_cov), 
                          method='SLSQP', bounds=bounds, constraints=constraints)
                          
    max_sharpe_weights = opt_sharpe.x
    max_sharpe_ret, max_sharpe_std = portfolio_performance(max_sharpe_weights, ann_returns, ann_cov)
    max_sharpe_ratio = (max_sharpe_ret - 0.065) / max_sharpe_std
    
    print("\nMaximum Sharpe Ratio Portfolio Weights:")
    for code, w in zip(pivot_returns.columns, max_sharpe_weights):
        print(f"  Scheme {code}: {w:.4f}")
    print(f"Expected Return: {max_sharpe_ret:.4f}, Volatility: {max_sharpe_std:.4f}, Sharpe: {max_sharpe_ratio:.4f}")
    
    # Minimise Volatility
    def portfolio_volatility(weights, returns, cov_matrix):
        return portfolio_performance(weights, returns, cov_matrix)[1]
        
    opt_var = minimize(portfolio_volatility, initial_weights, 
                       args=(ann_returns, ann_cov), 
                       method='SLSQP', bounds=bounds, constraints=constraints)
                       
    min_vol_weights = opt_var.x
    min_vol_ret, min_vol_std = portfolio_performance(min_vol_weights, ann_returns, ann_cov)
    min_vol_sharpe = (min_vol_ret - 0.065) / min_vol_std
    
    print("\nMinimum Variance Portfolio Weights:")
    for code, w in zip(pivot_returns.columns, min_vol_weights):
        print(f"  Scheme {code}: {w:.4f}")
    print(f"Expected Return: {min_vol_ret:.4f}, Volatility: {min_vol_std:.4f}, Sharpe: {min_vol_sharpe:.4f}")
    
    # Efficient Frontier curve
    frontier_y = np.linspace(min_vol_ret, ann_returns.max() * 0.98, 50)
    frontier_x = []
    
    for target_ret in frontier_y:
        cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                {'type': 'eq', 'fun': lambda x: portfolio_performance(x, ann_returns, ann_cov)[0] - target_ret})
        res = minimize(portfolio_volatility, initial_weights, 
                       args=(ann_returns, ann_cov), 
                       method='SLSQP', bounds=bounds, constraints=cons)
        frontier_x.append(res.fun)
        
    # Plot Markowitz Efficient Frontier
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    # Draw efficient frontier line
    plt.plot(frontier_x, frontier_y, 'g--', linewidth=2.5, label='Efficient Frontier')
    
    # Plot individual funds
    for code in key_funds:
        ret = ann_returns[code]
        vol = np.sqrt(ann_cov.loc[code, code])
        plt.scatter(vol, ret, marker='o', s=100, label=f"Fund {code}")
        
    # Plot Max Sharpe and Min Vol portfolios
    plt.scatter(max_sharpe_std, max_sharpe_ret, marker='*', color='red', s=200, label='Max Sharpe Ratio')
    plt.scatter(min_vol_std, min_vol_ret, marker='X', color='blue', s=200, label='Min Volatility')
    
    plt.title("Markowitz Efficient Frontier & Portfolio Optimisation (B4)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Annualised Volatility (Standard Deviation)", fontsize=12)
    plt.ylabel("Annualised Expected Return", fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'efficient_frontier.png'), dpi=300)
    plt.close()
    print("Saved efficient_frontier.png")
    
    # 2. Monte Carlo Simulation (B3) for SBI Small Cap Fund (125497)
    sbi_ret = pivot_returns[125497]
    sbi_mean = sbi_ret.mean()
    sbi_std = sbi_ret.std(ddof=0)
    
    # 5 years projection = 5 * 252 = 1260 days
    num_days = 1260
    num_simulations = 1000
    last_nav = df[df['scheme_code'] == 125497]['nav'].iloc[-1]
    
    # Simulate geometric Brownian motion paths
    sim_navs = np.zeros((num_days, num_simulations))
    sim_navs[0] = last_nav
    
    for sim in range(num_simulations):
        for day in range(1, num_days):
            # GBM Formula
            shock = np.random.normal(0, 1)
            sim_navs[day, sim] = sim_navs[day - 1, sim] * np.exp((sbi_mean - 0.5 * sbi_std**2) + sbi_std * shock)
            
    # Calculate median, 5th, and 95th percentiles
    median_path = np.median(sim_navs, axis=1)
    p5_path = np.percentile(sim_navs, 5, axis=1)
    p95_path = np.percentile(sim_navs, 95, axis=1)
    
    # Plot Monte Carlo projection
    plt.figure(figsize=(10, 6))
    time_axis = np.arange(num_days) / 252  # convert to years
    
    # Plot first 30 paths for visualization
    for i in range(30):
        plt.plot(time_axis, sim_navs[:, i], color='gray', alpha=0.1)
        
    plt.plot(time_axis, median_path, color='blue', linewidth=2.5, label='Median Projected NAV')
    plt.fill_between(time_axis, p5_path, p95_path, color='blue', alpha=0.15, label='90% Confidence Interval')
    
    plt.title(f"5-Year Monte Carlo NAV Simulation for SBI Small Cap Fund (B3)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Years of Simulation", fontsize=12)
    plt.ylabel("Projected Net Asset Value (NAV)", fontsize=12)
    plt.legend(loc='upper left', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'monte_carlo_simulation.png'), dpi=300)
    plt.close()
    print("Saved monte_carlo_simulation.png")

if __name__ == '__main__':
    run_portfolio_optimization_and_simulation()
