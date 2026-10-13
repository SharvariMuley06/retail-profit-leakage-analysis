
from pathlib import Path
import csv

import pandas as pd

try:
    from .validation import validate_retail_data
    from .data_quality import check_numeric_columns
except ImportError:
    from validation import validate_retail_data
    from data_quality import check_numeric_columns


def load_csv(file_path: str | Path) -> pd.DataFrame:
    """Load a valid, non-empty CSV file safely."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    if not path.is_file():
        raise ValueError("The provided path is not a file.")

    if path.suffix.lower() != ".csv":
        raise ValueError("Only CSV files are supported.")

    if path.stat().st_size == 0:
        raise ValueError("The CSV file is empty.")

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            header = next(csv.reader(file), None)
    except (UnicodeDecodeError, csv.Error) as exc:
        raise ValueError(
            "The CSV file could not be read. Check its format and encoding."
        ) from exc

    if not header:
        raise ValueError("The CSV file contains no readable data.")

    if len(header) != len(set(header)):
        seen = set()
        duplicates = []

        for column in header:
            if column in seen and column not in duplicates:
                duplicates.append(column)
            seen.add(column)

        raise ValueError(f"Duplicate column names found: {duplicates}")

    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError("The CSV file contains no readable data.") from exc
    except (pd.errors.ParserError, UnicodeDecodeError) as exc:
        raise ValueError(
            "The CSV file could not be read. Check its format and encoding."
        ) from exc

    if df.empty:
        raise ValueError("The CSV file has headers but no data rows.")

    return df


def process_retail_data(df: pd.DataFrame) -> dict:
    """Validate retail data and generate a combined quality report."""
    validation = validate_retail_data(df)

    if not validation["valid"]:
        return {
            "success": False,
            "validation": validation,
            "quality_summary": None,
            "numeric_quality": None,
            "invalid_numeric_columns": [],
        }

    missing_by_column = (
        df.isna()
        .sum()
        .loc[lambda counts: counts > 0]
        .sort_values(ascending=False)
        .to_dict()
    )

    quality_summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": int(df.isna().sum().sum()),
        "missing_by_column": missing_by_column,
        "column_names": df.columns.tolist(),
    }

    numeric_quality = check_numeric_columns(df)

    invalid_numeric_columns = [
        column
        for column, details in numeric_quality.items()
        if details["exists"] and details["invalid_values"] > 0
    ]

    return {
        "success": len(invalid_numeric_columns) == 0,
        "validation": validation,
        "quality_summary": quality_summary,
        "numeric_quality": numeric_quality,
        "invalid_numeric_columns": invalid_numeric_columns,
    }


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    dataset_path = (
        project_root
        / "Data"
        / "Processed"
        / "final_retail_dataset.csv"
    )

    df = load_csv(dataset_path)
    result = process_retail_data(df)

    print("Processing successful:", result["success"])
    print("Validation:", result["validation"])
    print("Quality summary:", result["quality_summary"])
    print("Numeric quality:", result["numeric_quality"])
    print("Invalid numeric columns:", result["invalid_numeric_columns"])
