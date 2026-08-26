import os

import joblib
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

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

MODEL_PATH = os.path.join(
    "models",
    "xgboost_stock_model.joblib",
)

OUTPUT_DIR = os.path.join(
    "data",
    "predictions",
)


# ============================================================
# FEATURES
# ============================================================

FEATURES = [
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
    "Price_SMA20_Ratio",
    "Price_SMA50_Ratio",
]


# ============================================================
# SIGNAL FUNCTION
# ============================================================

def generate_signal(probability):

    if probability >= 0.60:
        return "BUY"

    elif probability >= 0.40:
        return "HOLD"

    else:
        return "AVOID"


# ============================================================
# PROCESS STOCK
# ============================================================

def process_stock(
    model,
    stock_name,
):

    input_file = os.path.join(
        PROCESSED_DIR,
        f"{stock_name}_ml.csv",
    )

    if not os.path.exists(
        input_file
    ):

        print(
            f"❌ File not found: "
            f"{input_file}"
        )

        return None

    print(
        f"\nProcessing {stock_name}..."
    )

    df = pd.read_csv(
        input_file
    )

    # --------------------------------------------------------
    # Date
    # --------------------------------------------------------

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    # --------------------------------------------------------
    # Remove missing features
    # --------------------------------------------------------

    valid_df = df.dropna(
        subset=FEATURES
    ).copy()

    # --------------------------------------------------------
    # Features
    # --------------------------------------------------------

    X = valid_df[
        FEATURES
    ]

    # --------------------------------------------------------
    # Prediction probability
    # --------------------------------------------------------

    probabilities = (
        model.predict_proba(X)[:, 1]
    )

    valid_df[
        "Prediction_Probability"
    ] = probabilities

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    valid_df[
        "Prediction"
    ] = (
        probabilities >= 0.50
    ).astype(int)

    # --------------------------------------------------------
    # Trading signal
    # --------------------------------------------------------

    valid_df[
        "Signal"
    ] = valid_df[
        "Prediction_Probability"
    ].apply(
        generate_signal
    )

    # --------------------------------------------------------
    # Add ticker
    # --------------------------------------------------------

    valid_df["Ticker"] = (
        stock_name + ".NS"
    )

    # --------------------------------------------------------
    # Select output columns
    # --------------------------------------------------------

    output_columns = [
        "Date",
        "Ticker",
        "Close",
        "Future_Return_20D",
        "Target",
        "Prediction_Probability",
        "Prediction",
        "Signal",
    ]

    # Keep only columns that exist
    output_columns = [
        column
        for column in output_columns
        if column in valid_df.columns
    ]

    result = valid_df[
        output_columns
    ].copy()

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True,
    )

    output_file = os.path.join(
        OUTPUT_DIR,
        f"{stock_name}_predictions.csv",
    )

    result.to_csv(
        output_file,
        index=False,
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print(
        f"✓ Rows: {len(result)}"
    )

    print(
        f"✓ Saved: {output_file}"
    )

    print(
        "\nSignal distribution:"
    )

    print(
        result["Signal"]
        .value_counts()
    )

    return result


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n"
        "=============================================="
    )

    print(
        "       XGBOOST PREDICTION PIPELINE"
    )

    print(
        "=============================================="
    )

    # --------------------------------------------------------
    # Check model
    # --------------------------------------------------------

    if not os.path.exists(
        MODEL_PATH
    ):

        raise FileNotFoundError(
            f"Model not found: "
            f"{MODEL_PATH}"
        )

    print(
        f"\nLoading model:"
    )

    print(
        MODEL_PATH
    )

    model = joblib.load(
        MODEL_PATH
    )

    print(
        "✓ Model loaded."
    )

    # --------------------------------------------------------
    # Process all stocks
    # --------------------------------------------------------

    results = []

    for stock in STOCKS:

        result = process_stock(
            model=model,
            stock_name=stock,
        )

        if result is not None:

            results.append(
                result
            )

    # --------------------------------------------------------
    # Combined predictions
    # --------------------------------------------------------

    if results:

        combined = pd.concat(
            results,
            ignore_index=True,
        )

        combined = combined.sort_values(
            "Date"
        ).reset_index(
            drop=True
        )

        combined_file = os.path.join(
            OUTPUT_DIR,
            "all_predictions.csv",
        )

        combined.to_csv(
            combined_file,
            index=False,
        )

        print(
            "\n"
            "=============================================="
        )

        print(
            "COMBINED PREDICTION SUMMARY"
        )

        print(
            "=============================================="
        )

        print(
            f"Total predictions: "
            f"{len(combined)}"
        )

        print(
            "\nSignals:"
        )

        print(
            combined["Signal"]
            .value_counts()
        )

        print(
            "\nAverage probability:"
        )

        print(
            f"{combined['Prediction_Probability'].mean():.4f}"
        )

        print(
            "\nSaved:"
        )

        print(
            combined_file
        )

        print(
            "\n✓ Prediction pipeline completed."
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()