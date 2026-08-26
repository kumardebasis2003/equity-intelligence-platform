import pandas as pd

from app.ml.technical_indicators import (
    add_technical_indicators,
)


FILE_PATH = (
    "data/raw/RELIANCE.csv"
)


def main():

    print(
        "Loading market data..."
    )

    df = pd.read_csv(
        FILE_PATH
    )

    print(
        f"Original rows: {len(df)}"
    )

    df = add_technical_indicators(
        df
    )

    print(
        f"Rows after feature engineering: "
        f"{len(df)}"
    )

    print("\nTechnical Features:")

    features = [
        "Date",
        "Close",
        "Daily_Return",
        "SMA20",
        "SMA50",
        "EMA20",
        "RSI14",
        "MACD",
        "MACD_Signal",
        "MACD_Histogram",
        "BB_Middle",
        "BB_Upper",
        "BB_Lower",
        "BB_Width",
        "ATR14",
        "Momentum20",
        "Volatility20",
        "Volume_Change",
    ]

    print(
        df[features].tail(10)
    )


if __name__ == "__main__":
    main()