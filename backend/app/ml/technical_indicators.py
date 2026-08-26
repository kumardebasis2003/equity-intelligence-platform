import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import (
    BollingerBands,
    AverageTrueRange,
)


def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add technical indicators to OHLCV data.

    Required columns:
    Date, Open, High, Low, Close, Volume
    """

    df = df.copy()

    # ---------------------------------------------------------
    # Basic cleaning
    # ---------------------------------------------------------

    df["Date"] = pd.to_datetime(df["Date"])

    df = df.sort_values("Date")

    df = df.drop_duplicates(
        subset=["Date"]
    )

    # ---------------------------------------------------------
    # Daily return
    # ---------------------------------------------------------

    df["Daily_Return"] = (
        df["Close"].pct_change()
    )

    # ---------------------------------------------------------
    # Simple Moving Averages
    # ---------------------------------------------------------

    df["SMA20"] = (
        df["Close"]
        .rolling(window=20)
        .mean()
    )

    df["SMA50"] = (
        df["Close"]
        .rolling(window=50)
        .mean()
    )

    # ---------------------------------------------------------
    # Exponential Moving Average
    # ---------------------------------------------------------

    df["EMA20"] = (
        df["Close"]
        .ewm(
            span=20,
            adjust=False
        )
        .mean()
    )

    # ---------------------------------------------------------
    # RSI
    # ---------------------------------------------------------

    rsi = RSIIndicator(
        close=df["Close"],
        window=14,
    )

    df["RSI14"] = rsi.rsi()

    # ---------------------------------------------------------
    # MACD
    # ---------------------------------------------------------

    macd = MACD(
        close=df["Close"],
        window_slow=26,
        window_fast=12,
        window_sign=9,
    )

    df["MACD"] = macd.macd()

    df["MACD_Signal"] = (
        macd.macd_signal()
    )

    df["MACD_Histogram"] = (
        macd.macd_diff()
    )

    # ---------------------------------------------------------
    # Bollinger Bands
    # ---------------------------------------------------------

    bollinger = BollingerBands(
        close=df["Close"],
        window=20,
        window_dev=2,
    )

    df["BB_Middle"] = (
        bollinger.bollinger_mavg()
    )

    df["BB_Upper"] = (
        bollinger.bollinger_hband()
    )

    df["BB_Lower"] = (
        bollinger.bollinger_lband()
    )

    df["BB_Width"] = (
        bollinger.bollinger_wband()
    )

    # ---------------------------------------------------------
    # ATR
    # ---------------------------------------------------------

    atr = AverageTrueRange(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14,
    )

    df["ATR14"] = atr.average_true_range()

    # ---------------------------------------------------------
    # Momentum
    # ---------------------------------------------------------

    df["Momentum20"] = (
        df["Close"]
        / df["Close"].shift(20)
        - 1
    )

    # ---------------------------------------------------------
    # Volatility
    # ---------------------------------------------------------

    df["Volatility20"] = (
        df["Daily_Return"]
        .rolling(window=20)
        .std()
        * (252 ** 0.5)
    )

    # ---------------------------------------------------------
    # Volume change
    # ---------------------------------------------------------

    df["Volume_Change"] = (
        df["Volume"].pct_change()
    )

    # ---------------------------------------------------------
    # Price relative to moving averages
    # ---------------------------------------------------------

    df["Price_SMA20_Ratio"] = (
        df["Close"] / df["SMA20"]
    )

    df["Price_SMA50_Ratio"] = (
        df["Close"] / df["SMA50"]
    )

    # ---------------------------------------------------------
    # Remove rows created by rolling calculations
    # ---------------------------------------------------------

    df = df.dropna().reset_index(
        drop=True
    )

    return df