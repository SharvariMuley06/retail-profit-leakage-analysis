
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, Query

from src.analytics import (
    calculate_overall_metrics,
    performance_by_category,
    performance_by_region,
    monthly_sales_trend,
    loss_making_orders,
    discount_analysis,
)
from src.data_processing import load_csv

app = FastAPI(
    title="Retail Intelligence API",
    description="API for retail performance analytics and profit leakage investigation.",
    version="1.0.0",
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = (
    PROJECT_ROOT / "Data" / "Processed" / "final_retail_dataset.csv"
)


def get_dataframe() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail="Processed retail dataset was not found.",
        )
    try:
        return load_csv(DATASET_PATH)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not load retail dataset: {exc}",
        ) from exc


@app.get("/")
def home():
    return {
        "message": "Retail Intelligence API is running",
        "status": "healthy",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "retail-intelligence-api",
    }


@app.get("/analytics/overview")
def analytics_overview():
    return calculate_overall_metrics(get_dataframe())


@app.get("/analytics/category")
def category_performance():
    return performance_by_category(get_dataframe()).to_dict(
        orient="records"
    )


@app.get("/analytics/region")
def region_performance():
    return performance_by_region(get_dataframe()).to_dict(
        orient="records"
    )


@app.get("/analytics/monthly-trend")
def monthly_trend():
    return monthly_sales_trend(get_dataframe()).to_dict(
        orient="records"
    )



@app.get("/analytics/loss-making")
def loss_making(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    """Return a paginated list of negative-profit records."""
    result = loss_making_orders(get_dataframe())
    total_count = len(result)

    page = result.iloc[offset : offset + limit].copy()
    page = page.astype(object).where(pd.notna(page), None)

    return {
        "count": total_count,
        "limit": limit,
        "offset": offset,
        "returned_records": len(page),
        "records": page.to_dict(orient="records"),
    }



@app.get("/analytics/discount")
def discount_summary():
    return discount_analysis(get_dataframe()).to_dict(
        orient="records"
    )
