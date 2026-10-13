
import pandas as pd


NUMERIC_COLUMNS = [
    "sales",
    "profit",
    "discount",
    "quantity",
    "shipping_cost",
]


def check_numeric_columns(df: pd.DataFrame) -> dict:
    """Check numeric columns for missing and invalid values."""
    results = {}

    for column in NUMERIC_COLUMNS:
        if column not in df.columns:
            results[column] = {
                "exists": False,
                "invalid_values": None,
                "missing_values": None,
            }
            continue

        converted = pd.to_numeric(df[column], errors="coerce")
        invalid_mask = df[column].notna() & converted.isna()

        results[column] = {
            "exists": True,
            "invalid_values": int(invalid_mask.sum()),
            "missing_values": int(df[column].isna().sum()),
        }

    return results
