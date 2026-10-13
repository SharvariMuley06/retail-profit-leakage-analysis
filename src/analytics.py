
from pathlib import Path

import pandas as pd

try:
    from .data_processing import load_csv
except ImportError:
    from data_processing import load_csv


def calculate_overall_metrics(df: pd.DataFrame) -> dict:
    """Calculate the main retail business performance metrics."""
    required = {"sales", "profit", "quantity"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    sales = pd.to_numeric(df["sales"], errors="coerce")
    profit = pd.to_numeric(df["profit"], errors="coerce")
    quantity = pd.to_numeric(df["quantity"], errors="coerce")

    total_sales = float(sales.sum())
    total_profit = float(profit.sum())

    return {
        "total_sales": round(total_sales, 2),
        "total_profit": round(total_profit, 2),
        "total_quantity": round(float(quantity.sum()), 2),
        "profit_margin_pct": round(
            total_profit / total_sales * 100 if total_sales else 0.0, 2
        ),
        "total_records": int(len(df)),
    }


def performance_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize sales and profit by category."""
    required = {"category", "sales", "profit"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    result = (
        df.groupby("category", dropna=False)
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            order_records=(
                "order_id" if "order_id" in df.columns else "sales", "count"
            ),
        )
        .reset_index()
        .sort_values("total_sales", ascending=False)
    )

    return result.round(2)


def performance_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize sales and profit by region."""
    required = {"region", "sales", "profit"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    result = (
        df.groupby("region", dropna=False)
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
        )
        .reset_index()
        .sort_values("total_sales", ascending=False)
    )

    return result.round(2)


def monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly sales and profit from order_date."""
    required = {"order_date", "sales", "profit"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    working = df.copy()
    working["order_date"] = pd.to_datetime(
        working["order_date"], errors="coerce"
    )
    working = working.dropna(subset=["order_date"])
    working["month"] = working["order_date"].dt.to_period("M").astype(str)

    result = (
        working.groupby("month")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
        )
        .reset_index()
        .sort_values("month")
    )

    return result.round(2)


def loss_making_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Return records with negative profit."""
    if "profit" not in df.columns:
        raise ValueError("Missing required column: profit")

    profit = pd.to_numeric(df["profit"], errors="coerce")
    return df.loc[profit < 0].copy()


def discount_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze sales and profit by normalized discount level."""
    required = {"discount", "sales", "profit"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    working = df.copy()

    for column in ["discount", "sales", "profit"]:
        working[column] = pd.to_numeric(
            working[column], errors="coerce"
        )

    working = working.dropna(subset=["discount", "sales", "profit"])

    # Normalize floating-point values before grouping.
    working["discount"] = working["discount"].round(2)

    result = (
        working.groupby("discount", dropna=False)
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            record_count=("profit", "count"),
        )
        .reset_index()
        .sort_values("discount")
    )

    return result.round(2)


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    dataset_path = (
        project_root / "Data" / "Processed" / "final_retail_dataset.csv"
    )

    df = load_csv(dataset_path)

    print("\n=== OVERALL RETAIL METRICS ===")
    print(calculate_overall_metrics(df))

    print("\n=== PERFORMANCE BY CATEGORY ===")
    print(performance_by_category(df).to_string(index=False))

    print("\n=== PERFORMANCE BY REGION ===")
    print(performance_by_region(df).to_string(index=False))

    print("\n=== MONTHLY SALES TREND ===")
    print(monthly_sales_trend(df).head(12).to_string(index=False))

    print("\n=== LOSS-MAKING RECORDS ===")
    print("Count:", len(loss_making_orders(df)))

    print("\n=== DISCOUNT ANALYSIS ===")
    print(discount_analysis(df).to_string(index=False))
