import os

import pandas as pd

from app.ml.technical_indicators import (
    add_technical_indicators,
)


STOCKS = [
    "RELIANCE",
    "TCS",
    "INFY",
    "HDFCBANK",
    "ICICIBANK",
]


RAW_DIR = os.path.join(
    "data",
    "raw",
)

PROCESSED_DIR = os.path.join(
    "data",
    "processed",
)


def process_stock(stock_name):

    input_file = os.path.join(
        RAW_DIR,
        f"{stock_name}.csv",
    )

    output_file = os.path.join(
        PROCESSED_DIR,
        f"{stock_name}_features.csv",
    )

    print(
        f"\nProcessing {stock_name}..."
    )

    if not os.path.exists(
        input_file
    ):

        print(
            f"File not found: "
            f"{input_file}"
        )

        return

    df = pd.read_csv(
        input_file
    )

    df = add_technical_indicators(
        df
    )

    # Add ticker
    df["Ticker"] = (
        stock_name + ".NS"
    )

    os.makedirs(
        PROCESSED_DIR,
        exist_ok=True,
    )

    df.to_csv(
        output_file,
        index=False,
    )

    print(
        f"✓ Saved {len(df)} rows"
    )

    print(
        f"✓ {output_file}"
    )


def main():

    for stock in STOCKS:

        process_stock(
            stock
        )

    print(
        "\nFeature engineering "
        "completed."
    )


if __name__ == "__main__":
    main()