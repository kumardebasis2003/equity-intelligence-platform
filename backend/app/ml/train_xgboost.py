import os

import joblib
import pandas as pd

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
)


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


MODEL_DIR = os.path.join(
    "models"
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


TARGET = "Target"


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    frames = []

    for stock in STOCKS:

        filepath = os.path.join(
            PROCESSED_DIR,
            f"{stock}_ml.csv",
        )

        print(
            f"Loading {stock}..."
        )

        if not os.path.exists(filepath):

            print(
                f"⚠️ File not found: {filepath}"
            )

            continue

        df = pd.read_csv(
            filepath
        )

        # Add stock name if not already present
        if "Ticker" not in df.columns:

            df["Ticker"] = (
                stock + ".NS"
            )

        frames.append(df)

    if not frames:

        raise ValueError(
            "No ML datasets found."
        )

    combined = pd.concat(
        frames,
        ignore_index=True,
    )

    combined["Date"] = pd.to_datetime(
        combined["Date"]
    )

    # Sort chronologically
    combined = combined.sort_values(
        "Date"
    ).reset_index(drop=True)

    return combined


# ============================================================
# TRAIN MODEL
# ============================================================

def train_model():

    print(
        "\n"
        "=============================================="
    )

    print(
        "      XGBOOST EQUITY SIGNAL MODEL"
    )

    print(
        "=============================================="
    )

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    print(
        "\nLoading ML dataset..."
    )

    df = load_data()

    print(
        f"\nTotal rows: {len(df)}"
    )

    # --------------------------------------------------------
    # Remove missing values
    # --------------------------------------------------------

    df = df.dropna(
        subset=FEATURES + [TARGET]
    ).copy()

    print(
        f"Rows after cleaning: {len(df)}"
    )

    # --------------------------------------------------------
    # Sort by time
    # --------------------------------------------------------

    df = df.sort_values(
        "Date"
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # Target distribution
    # --------------------------------------------------------

    print(
        "\nTarget distribution:"
    )

    target_counts = (
        df[TARGET]
        .value_counts()
        .sort_index()
    )

    print(
        target_counts
    )

    positive_total = (
        df[TARGET] == 1
    ).sum()

    negative_total = (
        df[TARGET] == 0
    ).sum()

    print(
        f"\nTotal negative samples: "
        f"{negative_total}"
    )

    print(
        f"Total positive samples: "
        f"{positive_total}"
    )

    # --------------------------------------------------------
    # Time-aware split
    # --------------------------------------------------------

    train_end = int(
        len(df) * 0.70
    )

    validation_end = int(
        len(df) * 0.85
    )

    train_df = df.iloc[
        :train_end
    ].copy()

    validation_df = df.iloc[
        train_end:validation_end
    ].copy()

    test_df = df.iloc[
        validation_end:
    ].copy()

    print(
        "\n"
        "=============================================="
    )

    print(
        "TIME-AWARE DATASET SPLIT"
    )

    print(
        "=============================================="
    )

    print(
        f"Train      : {len(train_df)}"
    )

    print(
        f"Validation : {len(validation_df)}"
    )

    print(
        f"Test       : {len(test_df)}"
    )

    print(
        f"\nTrain period:"
    )

    print(
        f"{train_df['Date'].min()} "
        f"→ "
        f"{train_df['Date'].max()}"
    )

    print(
        f"\nValidation period:"
    )

    print(
        f"{validation_df['Date'].min()} "
        f"→ "
        f"{validation_df['Date'].max()}"
    )

    print(
        f"\nTest period:"
    )

    print(
        f"{test_df['Date'].min()} "
        f"→ "
        f"{test_df['Date'].max()}"
    )

    # --------------------------------------------------------
    # Features and targets
    # --------------------------------------------------------

    X_train = train_df[
        FEATURES
    ]

    y_train = train_df[
        TARGET
    ]

    X_validation = validation_df[
        FEATURES
    ]

    y_validation = validation_df[
        TARGET
    ]

    X_test = test_df[
        FEATURES
    ]

    y_test = test_df[
        TARGET
    ]

    # --------------------------------------------------------
    # Class imbalance
    # --------------------------------------------------------

    train_negative = (
        y_train == 0
    ).sum()

    train_positive = (
        y_train == 1
    ).sum()

    if train_positive == 0:

        raise ValueError(
            "Training dataset contains "
            "no positive samples."
        )

    scale_pos_weight = (
        train_negative
        / train_positive
    )

    print(
        "\n"
        "=============================================="
    )

    print(
        "CLASS IMBALANCE"
    )

    print(
        "=============================================="
    )

    print(
        f"Training negative samples: "
        f"{train_negative}"
    )

    print(
        f"Training positive samples: "
        f"{train_positive}"
    )

    print(
        f"scale_pos_weight: "
        f"{scale_pos_weight:.4f}"
    )

    # --------------------------------------------------------
    # XGBoost model
    # --------------------------------------------------------

    model = XGBClassifier(

        n_estimators=400,

        max_depth=4,

        learning_rate=0.03,

        subsample=0.8,

        colsample_bytree=0.8,

        objective="binary:logistic",

        eval_metric="auc",

        scale_pos_weight=scale_pos_weight,

        random_state=42,

        n_jobs=-1,
    )

    # --------------------------------------------------------
    # Train
    # --------------------------------------------------------

    print(
        "\n"
        "=============================================="
    )

    print(
        "TRAINING XGBOOST"
    )

    print(
        "=============================================="
    )

    model.fit(
        X_train,
        y_train,

        eval_set=[
            (
                X_validation,
                y_validation,
            )
        ],

        verbose=False,
    )

    print(
        "✓ Training completed."
    )

    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    probabilities = (
        model.predict_proba(
            X_test
        )[:, 1]
    )

    # Standard 0.50 threshold
    predictions = (
        probabilities >= 0.50
    ).astype(int)

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0,
    )

    try:

        auc = roc_auc_score(
            y_test,
            probabilities,
        )

    except ValueError:

        auc = 0.0

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print(
        "\n"
        "=============================================="
    )

    print(
        "XGBOOST TEST RESULTS"
    )

    print(
        "=============================================="
    )

    print(
        f"Accuracy : {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall   : {recall:.4f}"
    )

    print(
        f"F1 Score : {f1:.4f}"
    )

    print(
        f"ROC AUC  : {auc:.4f}"
    )

    print(
        "\nClassification Report:"
    )

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )

    # --------------------------------------------------------
    # Prediction distribution
    # --------------------------------------------------------

    predicted_positive = (
        predictions == 1
    ).sum()

    predicted_negative = (
        predictions == 0
    ).sum()

    print(
        "\nPrediction distribution:"
    )

    print(
        f"Predicted 0: "
        f"{predicted_negative}"
    )

    print(
        f"Predicted 1: "
        f"{predicted_positive}"
    )

    # --------------------------------------------------------
    # Feature importance
    # --------------------------------------------------------

    importance = pd.DataFrame({

        "Feature": FEATURES,

        "Importance":
            model.feature_importances_,

    })

    importance = (
        importance
        .sort_values(
            "Importance",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    print(
        "\n"
        "=============================================="
    )

    print(
        "TOP 10 FEATURES"
    )

    print(
        "=============================================="
    )

    print(
        importance.head(10).to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Save feature importance
    # --------------------------------------------------------

    os.makedirs(
        MODEL_DIR,
        exist_ok=True,
    )

    importance_path = os.path.join(
        MODEL_DIR,
        "feature_importance.csv",
    )

    importance.to_csv(
        importance_path,
        index=False,
    )

    # --------------------------------------------------------
    # Save model
    # --------------------------------------------------------

    model_path = os.path.join(
        MODEL_DIR,
        "xgboost_stock_model.joblib",
    )

    joblib.dump(
        model,
        model_path,
    )

    print(
        "\n"
        "=============================================="
    )

    print(
        "MODEL SAVED"
    )

    print(
        "=============================================="
    )

    print(
        f"Model:"
    )

    print(
        model_path
    )

    print(
        f"\nFeature importance:"
    )

    print(
        importance_path
    )

    print(
        "\n✓ XGBoost pipeline completed."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    train_model()