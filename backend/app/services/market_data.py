import os
import yfinance as yf
import pandas as pd


DEFAULT_STOCKS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
]


def download_stock_data(
    ticker: str,
    start_date: str = "2019-01-01",
    end_date: str = "2026-01-01",
) -> pd.DataFrame:

    try:
        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            auto_adjust=False,
            progress=False,
        )

        if data.empty:
            raise ValueError(
                f"No market data found for {ticker}"
            )

        data = data.reset_index()

        # Handle yfinance multi-level columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [
                column[0] for column in data.columns
            ]

        data["Ticker"] = ticker

        return data

    except Exception as error:
        raise RuntimeError(
            f"Failed to download {ticker}: {error}"
        )


def save_stock_data(
    ticker: str,
    data: pd.DataFrame,
    output_dir: str = "../../data/raw",
):
    os.makedirs(output_dir, exist_ok=True)

    filename = ticker.replace(".NS", "") + ".csv"

    filepath = os.path.join(
        output_dir,
        filename,
    )

    data.to_csv(filepath, index=False)

    return filepath


def download_all_stocks(
    stocks=None,
    start_date="2019-01-01",
    end_date="2026-01-01",
):
    if stocks is None:
        stocks = DEFAULT_STOCKS

    results = []

    for ticker in stocks:

        print(f"Downloading {ticker}...")

        try:
            data = download_stock_data(
                ticker=ticker,
                start_date=start_date,
                end_date=end_date,
            )

            filepath = save_stock_data(
                ticker,
                data,
            )

            results.append({
                "ticker": ticker,
                "rows": len(data),
                "file": filepath,
                "status": "success",
            })

            print(
                f"✓ {ticker}: "
                f"{len(data)} rows"
            )

        except Exception as error:

            results.append({
                "ticker": ticker,
                "rows": 0,
                "file": None,
                "status": "failed",
                "error": str(error),
            })

            print(
                f"✗ {ticker}: {error}"
            )

    return results