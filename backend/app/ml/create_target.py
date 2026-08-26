import os

import pandas as pd


STOCKS = [
    "RELIANCE",
    "TCS",
    "INFY",
    "HDFCBANK",
    "ICICIBANK",
]


PROCESSED_DIR = os.path.join(
    "data",
    "processed",
)


HORIZON = 20

TARGET_RETURN = 0.05


def create_target(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # Future 20-day return
    df["Future_Return_20D"] = (
        df["Close"].shift(-HORIZON)
        / df["Close"]
        - 1
    )

    # Binary target
    df["Target"] = (
        df["Future_Return_20D"]
        >= TARGET_RETURN
    ).astype(int)

    # Remove rows where future price
    # is unavailable
    df = df.dropna(
        subset=[
            "Future_Return_20D"
        ]
    )

    return df


def process_stock(stock_name):

    input_file = os.path.join(
        PROCESSED_DIR,
        f"{stock_name}_features.csv",
    )

    output_file = os.path.join(
        PROCESSED_DIR,
        f"{stock_name}_ml.csv",
    )

    print(
        f"\nProcessing {stock_name}..."
    )

    if not os.path.exists(input_file):

        print(
            f"❌ File not found: "
            f"{input_file}"
        )

        return

    df = pd.read_csv(
        input_file
    )

    df = create_target(df)

    df.to_csv(
        output_file,
        index=False,
    )

    positive = (
        df["Target"].sum()
    )

    negative = (
        len(df) - positive
    )

    print(
        f"Rows: {len(df)}"
    )

    print(
        f"Positive: {positive}"
    )

    print(
        f"Negative: {negative}"
    )

    print(
        f"Saved: {output_file}"
    )


def main():

    for stock in STOCKS:

        process_stock(stock)

    print(
        "\nTarget creation completed."
    )


if __name__ == "__main__":
    main()