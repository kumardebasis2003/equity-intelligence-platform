import os

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

RAW_DATA_DIR = os.path.join(
    "data",
    "raw",
)

OUTPUT_DIR = os.path.join(
    "data",
    "risk",
)

STOCKS = [
    "RELIANCE",
    "TCS",
    "INFY",
    "HDFCBANK",
    "ICICIBANK",
]

INITIAL_CAPITAL = 100000.0

RISK_FREE_RATE = 0.0

VAR_CONFIDENCE = 0.95


# ============================================================
# LOAD PRICE DATA
# ============================================================

def load_price_data():

    prices = {}

    for stock in STOCKS:

        filepath = os.path.join(
            RAW_DATA_DIR,
            f"{stock}.csv",
        )

        if not os.path.exists(filepath):

            print(
                f"⚠️ File not found: {filepath}"
            )

            continue

        df = pd.read_csv(
            filepath
        )

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

        df = df.sort_values(
            "Date"
        )

        df = df.set_index(
            "Date"
        )

        prices[stock] = df[
            "Close"
        ]

        print(
            f"✓ Loaded {stock}"
        )

    if not prices:

        raise ValueError(
            "No stock data found."
        )

    return pd.DataFrame(
        prices
    )


# ============================================================
# CALCULATE RETURNS
# ============================================================

def calculate_returns(
    prices,
):

    returns = prices.pct_change()

    returns = returns.dropna(
        how="all"
    )

    return returns


# ============================================================
# VOLATILITY
# ============================================================

def calculate_volatility(
    returns,
):

    daily_volatility = (
        returns.std()
    )

    annual_volatility = (
        daily_volatility
        * np.sqrt(252)
    )

    return annual_volatility


# ============================================================
# SHARPE RATIO
# ============================================================

def calculate_sharpe(
    returns,
):

    daily_mean = (
        returns.mean()
    )

    daily_std = (
        returns.std()
    )

    if daily_std == 0:

        return 0.0

    return (
        (
            daily_mean
            - RISK_FREE_RATE / 252
        )
        / daily_std
        * np.sqrt(252)
    )


# ============================================================
# MAXIMUM DRAWDOWN
# ============================================================

def calculate_max_drawdown(
    prices,
):

    cumulative = (
        1 + prices
        .pct_change()
        .fillna(0)
    ).cumprod()

    running_max = (
        cumulative.cummax()
    )

    drawdown = (
        cumulative
        / running_max
        - 1
    )

    return drawdown.min()


# ============================================================
# VALUE AT RISK
# ============================================================

def calculate_var(
    returns,
    confidence=0.95,
):

    var = np.percentile(
        returns.dropna(),
        (1 - confidence) * 100,
    )

    return var


# ============================================================
# RISK SCORE
# ============================================================

def calculate_risk_score(
    volatility,
    max_drawdown,
    var,
):

    score = 0

    # Annual volatility
    if volatility < 0.20:

        score += 1

    elif volatility < 0.35:

        score += 2

    else:

        score += 3

    # Maximum drawdown
    drawdown = abs(
        max_drawdown
    )

    if drawdown < 0.10:

        score += 1

    elif drawdown < 0.25:

        score += 2

    else:

        score += 3

    # VaR
    var_loss = abs(var)

    if var_loss < 0.015:

        score += 1

    elif var_loss < 0.03:

        score += 2

    else:

        score += 3

    if score <= 4:

        return "LOW"

    elif score <= 6:

        return "MEDIUM"

    else:

        return "HIGH"


# ============================================================
# PORTFOLIO ANALYSIS
# ============================================================

def analyze_portfolio(
    returns,
):

    # Equal-weight portfolio
    weights = np.array(
        [1 / len(returns.columns)]
        * len(returns.columns)
    )

    portfolio_returns = (
        returns
        .dropna()
        .dot(weights)
    )

    portfolio_volatility = (
        portfolio_returns.std()
        * np.sqrt(252)
    )

    portfolio_sharpe = (
        calculate_sharpe(
            portfolio_returns
        )
    )

    portfolio_var = (
        calculate_var(
            portfolio_returns,
            VAR_CONFIDENCE,
        )
    )

    portfolio_equity = (
        INITIAL_CAPITAL
        * (
            1 + portfolio_returns
        ).cumprod()
    )

    portfolio_drawdown = (
        calculate_max_drawdown(
            portfolio_equity
        )
    )

    portfolio_total_return = (
        portfolio_equity.iloc[-1]
        / INITIAL_CAPITAL
        - 1
    )

    return {
        "portfolio_returns":
            portfolio_returns,

        "portfolio_equity":
            portfolio_equity,

        "volatility":
            portfolio_volatility,

        "sharpe":
            portfolio_sharpe,

        "var":
            portfolio_var,

        "max_drawdown":
            portfolio_drawdown,

        "total_return":
            portfolio_total_return,
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n"
        "======================================================"
    )

    print(
        "          PORTFOLIO RISK ANALYSIS"
    )

    print(
        "======================================================"
    )

    # --------------------------------------------------------
    # Load prices
    # --------------------------------------------------------

    print(
        "\nLoading price data..."
    )

    prices = load_price_data()

    print(
        f"\nPrice dataset:"
    )

    print(
        prices.shape
    )

    # --------------------------------------------------------
    # Returns
    # --------------------------------------------------------

    returns = calculate_returns(
        prices
    )

    print(
        f"\nReturn dataset:"
    )

    print(
        returns.shape
    )

    # --------------------------------------------------------
    # Individual stock risk
    # --------------------------------------------------------

    results = []

    for stock in returns.columns:

        stock_returns = returns[
            stock
        ].dropna()

        volatility = (
            calculate_volatility(
                stock_returns
            )
        )

        sharpe = (
            calculate_sharpe(
                stock_returns
            )
        )

        max_drawdown = (
            calculate_max_drawdown(
                prices[stock]
            )
        )

        var = (
            calculate_var(
                stock_returns,
                VAR_CONFIDENCE,
            )
        )

        risk_level = (
            calculate_risk_score(
                volatility,
                max_drawdown,
                var,
            )
        )

        results.append({

            "Ticker": stock,

            "Annual_Volatility":
                volatility,

            "Sharpe_Ratio":
                sharpe,

            "Max_Drawdown":
                max_drawdown,

            "VaR_95":
                var,

            "Risk_Level":
                risk_level,
        })

    risk_df = pd.DataFrame(
        results
    )

    # --------------------------------------------------------
    # Portfolio
    # --------------------------------------------------------

    portfolio = (
        analyze_portfolio(
            returns
        )
    )

    # --------------------------------------------------------
    # Correlation
    # --------------------------------------------------------

    correlation = (
        returns.corr()
    )

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Save stock risk
    # --------------------------------------------------------

    risk_file = os.path.join(
        OUTPUT_DIR,
        "stock_risk_metrics.csv",
    )

    risk_df.to_csv(
        risk_file,
        index=False,
    )

    # --------------------------------------------------------
    # Save correlation
    # --------------------------------------------------------

    correlation_file = os.path.join(
        OUTPUT_DIR,
        "correlation_matrix.csv",
    )

    correlation.to_csv(
        correlation_file
    )

    # --------------------------------------------------------
    # Save portfolio equity
    # --------------------------------------------------------

    equity_file = os.path.join(
        OUTPUT_DIR,
        "portfolio_equity.csv",
    )

    portfolio[
        "portfolio_equity"
    ].rename(
        "Portfolio_Equity"
    ).to_csv(
        equity_file
    )

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    print(
        "\n"
        "======================================================"
    )

    print(
        "          INDIVIDUAL STOCK RISK"
    )

    print(
        "======================================================"
    )

    print(
        risk_df.to_string(
            index=False
        )
    )

    print(
        "\n"
        "======================================================"
    )

    print(
        "          CORRELATION MATRIX"
    )

    print(
        "======================================================"
    )

    print(
        correlation.round(3)
    )

    print(
        "\n"
        "======================================================"
    )

    print(
        "          PORTFOLIO RISK"
    )

    print(
        "======================================================"
    )

    print(
        f"Initial Capital : "
        f"₹{INITIAL_CAPITAL:,.2f}"
    )

    print(
        f"Final Capital   : "
        f"₹{portfolio['portfolio_equity'].iloc[-1]:,.2f}"
    )

    print(
        f"Total Return    : "
        f"{portfolio['total_return']:.2%}"
    )

    print(
        f"Volatility      : "
        f"{portfolio['volatility']:.2%}"
    )

    print(
        f"Sharpe Ratio    : "
        f"{portfolio['sharpe']:.2f}"
    )

    print(
        f"Maximum Drawdown: "
        f"{portfolio['max_drawdown']:.2%}"
    )

    print(
        f"VaR 95%         : "
        f"{portfolio['var']:.2%}"
    )

    print(
        "\nSaved files:"
    )

    print(
        risk_file
    )

    print(
        correlation_file
    )

    print(
        equity_file
    )

    print(
        "\n✓ Portfolio risk analysis completed."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()