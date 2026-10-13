
import pandas as pd


REQUIRED_RETAIL_COLUMNS = {
    "sales",
    "profit",
    "discount",
    "quantity",
}


def validate_retail_data(df: pd.DataFrame) -> dict:
    """Check whether a dataset supports the core retail analysis."""

    missing_columns = REQUIRED_RETAIL_COLUMNS - set(df.columns)

    if missing_columns:
        return {
            "valid": False,
            "message": "Required retail columns are missing.",
            "missing_columns": sorted(missing_columns),
            "rows": len(df),
            "columns": len(df.columns),
        }

    if df.empty:
        return {
            "valid": False,
            "message": "The uploaded dataset is empty.",
            "missing_columns": [],
            "rows": 0,
            "columns": len(df.columns),
        }

    return {
        "valid": True,
        "message": "Dataset contains the required retail columns.",
        "missing_columns": [],
        "rows": len(df),
        "columns": len(df.columns),
    }
if __name__ == "__main__":
    from pathlib import Path

    project_root = Path(__file__).resolve().parent.parent
    dataset_path = (
        project_root / "Data" / "Processed" / "final_retail_dataset.csv"
    )

    df = pd.read_csv(dataset_path)
    result = validate_retail_data(df)

    print(result)