import pandas as pd
import numpy as np
from typing import Tuple
import statsmodels.api as sm


def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    """Calculate annualised Sharpe ratio.

    Parameters
    ----------
    returns : pd.Series
        Daily returns (as decimal, e.g., 0.001 for 0.1%).
    risk_free_rate : float, optional
        Daily risk‑free rate (default 0). Use same frequency as ``returns``.
    """
    excess = returns - risk_free_rate
    mean_excess = excess.mean()
    std_excess = excess.std(ddof=0)
    if std_excess == 0:
        return np.nan
    return np.sqrt(252) * mean_excess / std_excess


def beta_coefficient(returns: pd.Series, benchmark: pd.Series) -> float:
    """Calculate Beta of a fund relative to a benchmark index.

    Both series must be aligned on the same dates.
    """
    if len(returns) != len(benchmark):
        raise ValueError("Length mismatch between fund and benchmark returns")
    X = sm.add_constant(benchmark.values)
    model = sm.OLS(returns.values, X).fit()
    return model.params[1]


def var_cvar(returns: pd.Series, confidence: float = 0.95) -> Tuple[float, float]:
    """Return VaR (percentile) and CVaR (expected shortfall) for a given confidence level.

    Parameters
    ----------
    returns : pd.Series
        Daily returns.
    confidence : float, default 0.95
        Confidence level for VaR (e.g., 0.95 for 5th percentile).
    """
    var = returns.quantile(1 - confidence)
    cvar = returns[returns <= var].mean()
    return var, cvar


def hhi(sector_weights: dict) -> float:
    """Herfindahl‑Hirschman Index for a fund's sector concentration.

    ``sector_weights`` should map sector name to weight (as a proportion, e.g., 0.25).
    """
    weights = np.array(list(sector_weights.values()))
    return float((weights ** 2).sum())
