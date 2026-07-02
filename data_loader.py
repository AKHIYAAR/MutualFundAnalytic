import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def load_returns(csv_path: str = None) -> pd.DataFrame:
    """Load daily returns for all schemes.

    Parameters
    ----------
    csv_path: str, optional
        Path to CSV file containing daily returns. If None, defaults to
        ``data/returns.csv`` relative to the project root.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ``date``, ``scheme_id``, ``return``.
    """
    if csv_path is None:
        csv_path = os.path.join(DATA_DIR, 'returns.csv')
    df = pd.read_csv(csv_path, parse_dates=['date'])
    return df

def load_transactions(csv_path: str = None) -> pd.DataFrame:
    """Load SIP transaction records.

    Expected columns: ``investor_id``, ``date``, ``sip_amount``, ``fund_id``.
    """
    if csv_path is None:
        csv_path = os.path.join(DATA_DIR, 'transactions.csv')
    df = pd.read_csv(csv_path, parse_dates=['date'])
    return df

def load_fund_metadata(csv_path: str = None) -> pd.DataFrame:
    """Load fund metadata.

    Expected columns: ``fund_id``, ``risk_grade``, ``sector_weights`` (JSON string or
    serialized dict), ``sharpe_ratio``, ``aum`` and any other attributes.
    """
    if csv_path is None:
        csv_path = os.path.join(DATA_DIR, 'funds.csv')
    df = pd.read_csv(csv_path)
    # Parse sector_weights JSON if needed
    if 'sector_weights' in df.columns:
        import json
        df['sector_weights'] = df['sector_weights'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
    return df
