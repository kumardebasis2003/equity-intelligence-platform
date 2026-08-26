import os

import pandas as pd
from sqlalchemy import select

from app.models.database import SessionLocal
from app.models.stock import Stock, PriceHistory


# ============================================================
# DATA DIRECTORY
# ============================================================

# Current file:
# backend/app/services/import_market_data.py
#
# We need:
# backend/data/raw/

DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "data",
        "raw",
    )
)


# ============================================================
# STOCK INFORMATION
# ============================================================

STOCK_INFO = {
    "RELIANCE": {
        "ticker": "RELIANCE.NS",
        "company_name": "Reliance Industries Limited",
        "sector": "Oil, Gas & Conglomerate",
    },

    "TCS": {
        "ticker": "TCS.NS",
        "company_name": "Tata Consultancy Services Limited",
        "sector": "Information Technology",
    },

    "INFY": {
        "ticker": "INFY.NS",
        "company_name": "Infosys Limited",
        "sector": "Information Technology",
    },

    "HDFCBANK": {
        "ticker": "HDFCBANK.NS",
        "company_name": "HDFC Bank Limited",
        "sector": "Banking",
    },

    "ICICIBANK": {
        "ticker": "ICICIBANK.NS",
        "company_name": "ICICI Bank Limited",
        "sector": "Banking",
    },
}


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:

    # Handle MultiIndex columns from yfinance
    if isinstance(df.columns, pd.MultiIndex):

        df.columns = [
            column[0]
            for column in df.columns
        ]

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    return df


# ============================================================
# IMPORT ONE STOCK
# ============================================================

def import_stock(
    session,
    stock_name: str,
    info: dict,
):

    filepath = os.path.join(
        DATA_DIR,
        f"{stock_name}.csv",
    )

    print("\n" + "=" * 60)
    print(f"Importing: {stock_name}")
    print(f"File: {filepath}")
    print("=" * 60)

    # --------------------------------------------------------
    # Check file
    # --------------------------------------------------------

    if not os.path.exists(filepath):

        print("❌ File not found")

        return {
            "ticker": info["ticker"],
            "status": "failed",
            "rows": 0,
            "error": "File not found",
        }

    # --------------------------------------------------------
    # Read CSV
    # --------------------------------------------------------

    try:

        df = pd.read_csv(filepath)

    except Exception as error:

        print(f"❌ CSV read error: {error}")

        return {
            "ticker": info["ticker"],
            "status": "failed",
            "rows": 0,
            "error": str(error),
        }

    # --------------------------------------------------------
    # Clean columns
    # --------------------------------------------------------

    df = clean_column_names(df)

    print(
        f"CSV rows found: {len(df)}"
    )

    # --------------------------------------------------------
    # Check required columns
    # --------------------------------------------------------

    required_columns = [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        print(
            "❌ Missing columns:",
            missing_columns,
        )

        return {
            "ticker": info["ticker"],
            "status": "failed",
            "rows": 0,
            "error": (
                f"Missing columns: "
                f"{missing_columns}"
            ),
        }

    # --------------------------------------------------------
    # Convert Date
    # --------------------------------------------------------

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce",
    ).dt.date

    # --------------------------------------------------------
    # Remove invalid rows
    # --------------------------------------------------------

    df = df.dropna(
        subset=[
            "Date",
            "Close",
        ]
    )

    print(
        f"Valid rows: {len(df)}"
    )

    # --------------------------------------------------------
    # Find or create stock
    # --------------------------------------------------------

    stock = session.scalar(
        select(Stock).where(
            Stock.ticker == info["ticker"]
        )
    )

    if stock is None:

        stock = Stock(
            ticker=info["ticker"],
            company_name=info["company_name"],
            exchange="NSE",
            sector=info["sector"],
        )

        session.add(stock)

        # Generate ID
        session.flush()

        print(
            f"✓ Created stock: "
            f"{info['ticker']}"
        )

    else:

        print(
            f"✓ Stock already exists: "
            f"{info['ticker']}"
        )

    # --------------------------------------------------------
    # Get existing dates
    # --------------------------------------------------------

    existing_dates = set(
        session.scalars(
            select(
                PriceHistory.date
            ).where(
                PriceHistory.stock_id
                == stock.id
            )
        ).all()
    )

    print(
        f"Existing records: "
        f"{len(existing_dates)}"
    )

    # --------------------------------------------------------
    # Prepare records
    # --------------------------------------------------------

    records = []

    for _, row in df.iterrows():

        trade_date = row["Date"]

        # Skip duplicates
        if trade_date in existing_dates:
            continue

        try:

            adjusted_close = None

            if "Adj Close" in df.columns:

                adjusted_close = row[
                    "Adj Close"
                ]

            record = PriceHistory(
                stock_id=stock.id,
                date=trade_date,

                open=row["Open"],
                high=row["High"],
                low=row["Low"],
                close=row["Close"],

                adjusted_close=adjusted_close,

                volume=row["Volume"],
            )

            records.append(record)

        except Exception as error:

            print(
                f"⚠️ Skipping row "
                f"{trade_date}: {error}"
            )

    # --------------------------------------------------------
    # Insert records
    # --------------------------------------------------------

    if records:

        session.add_all(records)

        print(
            f"✓ New records prepared: "
            f"{len(records)}"
        )

    else:

        print(
            "No new records to insert."
        )

    return {
        "ticker": info["ticker"],
        "status": "success",
        "rows": len(records),
        "error": None,
    }


# ============================================================
# IMPORT ALL STOCKS
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("     AI EQUITY RESEARCH PLATFORM")
    print("     MARKET DATA IMPORT")
    print("=" * 70)

    print(
        f"\nData directory:\n{DATA_DIR}"
    )

    # --------------------------------------------------------
    # Check data directory
    # --------------------------------------------------------

    if not os.path.exists(DATA_DIR):

        print(
            "\n❌ Data directory does not exist:"
        )

        print(DATA_DIR)

        return

    # --------------------------------------------------------
    # Database session
    # --------------------------------------------------------

    session = SessionLocal()

    results = []

    try:

        # ----------------------------------------------------
        # Import each stock
        # ----------------------------------------------------

        for stock_name, info in STOCK_INFO.items():

            result = import_stock(
                session=session,
                stock_name=stock_name,
                info=info,
            )

            results.append(result)

        # ----------------------------------------------------
        # Commit everything
        # ----------------------------------------------------

        session.commit()

        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------

        print("\n")
        print("=" * 70)
        print("                 IMPORT SUMMARY")
        print("=" * 70)

        successful = 0
        total_rows = 0

        for result in results:

            ticker = result["ticker"]
            status = result["status"]
            rows = result["rows"]

            if status == "success":

                print(
                    f"✓ {ticker:<15} "
                    f"{rows:>6} records"
                )

                successful += 1
                total_rows += rows

            else:

                print(
                    f"❌ {ticker:<15} "
                    f"FAILED"
                )

        print("-" * 70)

        print(
            f"Stocks processed: "
            f"{len(results)}"
        )

        print(
            f"Successful: "
            f"{successful}"
        )

        print(
            f"Total new records: "
            f"{total_rows}"
        )

        print("=" * 70)

        if successful == len(results):

            print(
                "\n✅ MARKET DATA IMPORT "
                "COMPLETED SUCCESSFULLY"
            )

        else:

            print(
                "\n⚠️ IMPORT COMPLETED "
                "WITH ERRORS"
            )

    except Exception as error:

        session.rollback()

        print("\n")
        print("=" * 70)
        print("❌ IMPORT FAILED")
        print("=" * 70)

        print(error)

    finally:

        session.close()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()