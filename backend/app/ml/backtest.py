import os

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

PREDICTIONS_FILE = os.path.join(
    "data",
    "predictions",
    "all_predictions.csv",
)

OUTPUT_DIR = os.path.join(
    "data",
    "backtest",
)

INITIAL_CAPITAL = 100000.0

HOLDING_PERIOD = 20

TRANSACTION_COST = 0.001

BUY_THRESHOLD = 0.60

RISK_FREE_RATE = 0.0


# ============================================================
# METRICS
# ============================================================

def calculate_cagr(
    initial_value,
    final_value,
    years,
):

    if initial_value <= 0:
        return 0.0

    if final_value <= 0:
        return -1.0

    if years <= 0:
        return 0.0

    return (
        (final_value / initial_value)
        ** (1 / years)
        - 1
    )


def calculate_sharpe(
    daily_returns,
):

    returns = pd.Series(
        daily_returns
    ).dropna()

    if len(returns) < 2:
        return 0.0

    volatility = returns.std()

    if volatility == 0:
        return 0.0

    annual_return = returns.mean() * 252

    annual_volatility = (
        volatility * np.sqrt(252)
    )

    return (
        annual_return
        - RISK_FREE_RATE
    ) / annual_volatility


def calculate_max_drawdown(
    equity_curve,
):

    equity = pd.Series(
        equity_curve
    )

    running_max = (
        equity.cummax()
    )

    drawdown = (
        equity / running_max
        - 1
    )

    return drawdown.min()


# ============================================================
# BACKTEST ONE STOCK
# ============================================================

def backtest_stock(
    df,
    ticker,
):

    df = df.copy()

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    df = df.sort_values(
        "Date"
    ).reset_index(
        drop=True
    )

    # --------------------------------------------------------
    # Test period only
    # --------------------------------------------------------

    # We use the final 15% of observations.
    test_start = int(
        len(df) * 0.85
    )

    test_df = df.iloc[
        test_start:
    ].copy()

    test_df = test_df.reset_index(
        drop=True
    )

    if len(test_df) < HOLDING_PERIOD + 1:

        return None

    # --------------------------------------------------------
    # Portfolio
    # --------------------------------------------------------

    capital = INITIAL_CAPITAL

    trades = []

    equity_records = []

    i = 0

    while i < len(test_df):

        row = test_df.iloc[i]

        current_date = row["Date"]

        current_price = float(
            row["Close"]
        )

        # ----------------------------------------------------
        # BUY SIGNAL
        # ----------------------------------------------------

        if (
            row["Prediction_Probability"]
            >= BUY_THRESHOLD
        ):

            exit_index = (
                i + HOLDING_PERIOD
            )

            if exit_index >= len(test_df):
                break

            exit_row = test_df.iloc[
                exit_index
            ]

            exit_price = float(
                exit_row["Close"]
            )

            # ------------------------------------------------
            # Transaction costs
            # ------------------------------------------------

            entry_cost = (
                current_price
                * TRANSACTION_COST
            )

            exit_cost = (
                exit_price
                * TRANSACTION_COST
            )

            # Gross return
            gross_return = (
                exit_price
                / current_price
                - 1
            )

            # Net return
            net_return = (
                gross_return
                - TRANSACTION_COST
                - TRANSACTION_COST
            )

            capital_before = capital

            capital = (
                capital
                * (1 + net_return)
            )

            trades.append({

                "Ticker": ticker,

                "Entry_Date":
                    current_date,

                "Exit_Date":
                    exit_row["Date"],

                "Entry_Price":
                    current_price,

                "Exit_Price":
                    exit_price,

                "Probability":
                    row[
                        "Prediction_Probability"
                    ],

                "Gross_Return":
                    gross_return,

                "Net_Return":
                    net_return,

                "Capital_Before":
                    capital_before,

                "Capital_After":
                    capital,
            })

            # ------------------------------------------------
            # Move forward 20 days
            # ------------------------------------------------

            # This prevents overlapping trades.
            i = exit_index + 1

        else:

            i += 1

        equity_records.append({

            "Date": current_date,

            "Equity": capital,
        })

    # --------------------------------------------------------
    # No trades
    # --------------------------------------------------------

    trades_df = pd.DataFrame(
        trades
    )

    equity_df = pd.DataFrame(
        equity_records
    )

    if trades_df.empty:

        return {
            "Ticker": ticker,
            "metrics": None,
            "trades": trades_df,
            "equity": equity_df,
        }

    # --------------------------------------------------------
    # Strategy metrics
    # --------------------------------------------------------

    total_return = (
        capital
        / INITIAL_CAPITAL
        - 1
    )

    start_date = pd.to_datetime(
        test_df["Date"].min()
    )

    end_date = pd.to_datetime(
        test_df["Date"].max()
    )

    years = (
        end_date - start_date
    ).days / 365.25

    cagr = calculate_cagr(
        INITIAL_CAPITAL,
        capital,
        years,
    )

    # --------------------------------------------------------
    # Daily equity returns
    # --------------------------------------------------------

    if not equity_df.empty:

        equity_df[
            "Daily_Return"
        ] = (
            equity_df["Equity"]
            .pct_change()
            .fillna(0)
        )

        sharpe = calculate_sharpe(
            equity_df["Daily_Return"]
        )

        max_drawdown = (
            calculate_max_drawdown(
                equity_df["Equity"]
            )
        )

    else:

        sharpe = 0.0
        max_drawdown = 0.0

    # --------------------------------------------------------
    # Win rate
    # --------------------------------------------------------

    winning_trades = (
        trades_df["Net_Return"] > 0
    ).sum()

    total_trades = len(
        trades_df
    )

    win_rate = (
        winning_trades
        / total_trades
    )

    average_trade = (
        trades_df["Net_Return"]
        .mean()
    )

    # --------------------------------------------------------
    # Buy & Hold benchmark
    # --------------------------------------------------------

    benchmark_start = float(
        test_df.iloc[0]["Close"]
    )

    benchmark_end = float(
        test_df.iloc[-1]["Close"]
    )

    benchmark_return = (
        benchmark_end
        / benchmark_start
        - 1
    )

    benchmark_cagr = calculate_cagr(
        INITIAL_CAPITAL,
        INITIAL_CAPITAL
        * (1 + benchmark_return),
        years,
    )

    metrics = {

        "Ticker": ticker,

        "Initial_Capital":
            INITIAL_CAPITAL,

        "Final_Capital":
            capital,

        "Strategy_Total_Return":
            total_return,

        "Strategy_CAGR":
            cagr,

        "Strategy_Sharpe":
            sharpe,

        "Strategy_Max_Drawdown":
            max_drawdown,

        "Strategy_Win_Rate":
            win_rate,

        "Total_Trades":
            total_trades,

        "Winning_Trades":
            winning_trades,

        "Average_Trade_Return":
            average_trade,

        "Buy_Hold_Return":
            benchmark_return,

        "Buy_Hold_CAGR":
            benchmark_cagr,
    }

    return {

        "Ticker": ticker,

        "metrics": metrics,

        "trades": trades_df,

        "equity": equity_df,
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n"
        "===================================================="
    )

    print(
        "       REALISTIC XGBOOST BACKTEST"
    )

    print(
        "===================================================="
    )

    print(
        f"\nInitial Capital: "
        f"₹{INITIAL_CAPITAL:,.2f}"
    )

    print(
        f"Holding Period: "
        f"{HOLDING_PERIOD} trading days"
    )

    print(
        f"Buy Threshold: "
        f"{BUY_THRESHOLD:.2f}"
    )

    print(
        f"Transaction Cost: "
        f"{TRANSACTION_COST:.2%}"
    )

    # --------------------------------------------------------
    # Load predictions
    # --------------------------------------------------------

    if not os.path.exists(
        PREDICTIONS_FILE
    ):

        raise FileNotFoundError(
            PREDICTIONS_FILE
        )

    df = pd.read_csv(
        PREDICTIONS_FILE
    )

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    print(
        f"\nTotal rows: "
        f"{len(df)}"
    )

    # --------------------------------------------------------
    # Output directory
    # --------------------------------------------------------

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True,
    )

    all_metrics = []

    all_trades = []

    # --------------------------------------------------------
    # Stock backtests
    # --------------------------------------------------------

    for ticker in sorted(
        df["Ticker"].unique()
    ):

        print(
            "\n"
            + "-" * 60
        )

        print(
            f"Backtesting: {ticker}"
        )

        stock_df = df[
            df["Ticker"] == ticker
        ].copy()

        result = backtest_stock(
            stock_df,
            ticker,
        )

        if result is None:

            print(
                "❌ Not enough data"
            )

            continue

        metrics = result[
            "metrics"
        ]

        trades = result[
            "trades"
        ]

        if metrics is None:

            print(
                "⚠️ No BUY trades"
            )

            continue

        all_metrics.append(
            metrics
        )

        all_trades.append(
            trades
        )

        print(
            f"Trades: "
            f"{metrics['Total_Trades']}"
        )

        print(
            f"Strategy Return: "
            f"{metrics['Strategy_Total_Return']:.2%}"
        )

        print(
            f"Strategy CAGR: "
            f"{metrics['Strategy_CAGR']:.2%}"
        )

        print(
            f"Strategy Sharpe: "
            f"{metrics['Strategy_Sharpe']:.2f}"
        )

        print(
            f"Max Drawdown: "
            f"{metrics['Strategy_Max_Drawdown']:.2%}"
        )

        print(
            f"Win Rate: "
            f"{metrics['Strategy_Win_Rate']:.2%}"
        )

        print(
            f"Buy & Hold Return: "
            f"{metrics['Buy_Hold_Return']:.2%}"
        )

    # --------------------------------------------------------
    # Save metrics
    # --------------------------------------------------------

    if all_metrics:

        metrics_df = pd.DataFrame(
            all_metrics
        )

        metrics_file = os.path.join(
            OUTPUT_DIR,
            "realistic_backtest_metrics.csv",
        )

        metrics_df.to_csv(
            metrics_file,
            index=False,
        )

        print(
            "\n"
            "===================================================="
        )

        print(
            "FINAL BACKTEST RESULTS"
        )

        print(
            "===================================================="
        )

        columns = [

            "Ticker",

            "Strategy_Total_Return",

            "Strategy_CAGR",

            "Strategy_Sharpe",

            "Strategy_Max_Drawdown",

            "Strategy_Win_Rate",

            "Total_Trades",

            "Buy_Hold_Return",

            "Buy_Hold_CAGR",
        ]

        print(
            metrics_df[
                columns
            ].to_string(
                index=False
            )
        )

        print(
            f"\nSaved:"
        )

        print(
            metrics_file
        )

    # --------------------------------------------------------
    # Save trades
    # --------------------------------------------------------

    if all_trades:

        trades_df = pd.concat(
            all_trades,
            ignore_index=True,
        )

        trades_file = os.path.join(
            OUTPUT_DIR,
            "realistic_backtest_trades.csv",
        )

        trades_df.to_csv(
            trades_file,
            index=False,
        )

        print(
            f"\nTrades saved:"
        )

        print(
            trades_file
        )

    print(
        "\n✓ Realistic backtest completed."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()