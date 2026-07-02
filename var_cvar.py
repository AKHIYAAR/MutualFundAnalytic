import pandas as pd
import numpy as np
import os
from data_loader import load_returns, load_transactions, load_fund_metadata

def compute_var_cvar(returns_df: pd.DataFrame) -> pd.DataFrame:
    """Compute 95% VaR (5th percentile) and CVaR for each scheme.

    Parameters
    ----------
    returns_df : pd.DataFrame
        DataFrame with columns ``scheme_code``, ``date`` (datetime), ``return``.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ``scheme_code``, ``VaR_95``, ``CVaR``.
    """
    returns_df = returns_df.dropna(subset=['return'])
    results = []
    for scheme, grp in returns_df.groupby('scheme_code'):
        var_95 = grp['return'].quantile(0.05)
        cvar = grp.loc[grp['return'] <= var_95, 'return'].mean()
        results.append({'scheme_code': scheme, 'VaR_95': var_95, 'CVaR': cvar})
    return pd.DataFrame(results)

def main():
    nav_path = os.path.join(os.path.dirname(__file__), 'Data', 'raw', 'nav_history.csv')
    nav_df = pd.read_csv(nav_path, parse_dates=['date'])
    nav_df['scheme_code'] = pd.to_numeric(nav_df['scheme_code'], errors='coerce')
    nav_df = nav_df.dropna(subset=['scheme_code', 'date', 'nav'])
    nav_df = nav_df.sort_values(['scheme_code', 'date'])
    nav_df['return'] = nav_df.groupby('scheme_code')['nav'].pct_change()
    returns_df = nav_df.dropna(subset=['return'])
    var_cvar_df = compute_var_cvar(returns_df)
    out_path = os.path.join(os.path.dirname(__file__), 'var_cvar_report.csv')
    var_cvar_df.to_csv(out_path, index=False)
    print(f"VaR/CVaR report saved to {out_path}")

if __name__ == '__main__':
    main()
