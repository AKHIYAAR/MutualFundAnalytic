# Mutual Fund Portfolio Analysis Report

This report provides a financial analysis of the historical Net Asset Value (NAV) performance, risk metrics, and drawdowns for the ingested mutual fund schemes.

## 1. Executive Performance Metrics Table

| Scheme Name | Cumulative Return | Annualized Return | Annualized Volatility | Sharpe Ratio | Max Drawdown |
| --- | --- | --- | --- | --- | --- |
| Aditya Birla Sun Life Banking & PSU Debt Fund  - DIRECT - IDCW | 2.64% | 0.21% | 8.78% | -0.61 | -36.65% |
| Axis ELSS Tax Saver Fund - Direct Plan - Growth Option | 555.43% | 16.1% | 15.18% | 0.66 | -33.51% |
| HDFC Hybrid Equity Fund - Growth Option - Direct Plan | 355.61% | 12.79% | 14.28% | 0.49 | -33.56% |
| HDFC Money Market Fund - Growth Option - Direct Plan | 139.19% | 7.17% | 0.61% | 1.52 | -1.39% |
| Kotak Multi Asset Omni FOF - Direct Growth - Direct | 597.09% | 16.67% | 9.63% | 1.03 | -22.83% |
| Nippon India Large Cap Fund - Direct Plan Growth Plan - Growth Option | 605.44% | 16.78% | 16.44% | 0.66 | -39.96% |
| SBI Small Cap Fund - Direct Plan - Growth | 1466.65% | 24.41% | 15.06% | 1.13 | -40.26% |
| quant Mid Cap Fund - Growth Option - Direct Plan | 669.33% | 17.58% | 15.73% | 0.73 | -33.43% |


## 2. Investment Growth Visualisation

The chart below illustrates the growth of an initial investment of 10,000 INR across all funds based on daily historical NAV data.

![Growth of 10k Investment](plots/growth_investment.png)

## 3. Risk-Reward Tradeoff Analysis

The chart below shows the risk (annualized volatility) vs. reward (annualized returns) of the funds. In general, higher returns are expected to carry higher risk (volatility).

![Risk Return Tradeoff](plots/risk_return_tradeoff.png)

## 4. Key Financial Observations

- **Highest Performing Scheme:** SBI Small Cap Fund - Direct Plan - Growth with an annualized return of 24.41%.
- **Lowest Volatility (Safest) Scheme:** HDFC Money Market Fund - Growth Option - Direct Plan with an annualized volatility of 0.61%.
- **Best Risk-Adjusted Returns (Highest Sharpe Ratio):** HDFC Money Market Fund - Growth Option - Direct Plan with a Sharpe ratio of 1.52.
- **Worst Peak-to-Trough Decline (Max Drawdown):** SBI Small Cap Fund - Direct Plan - Growth with a drawdown of -40.26%.
