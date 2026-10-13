
import pandas as pd

from src.validation import validate_retail_data


def test_valid_retail_dataset():
    df = pd.DataFrame({
        "sales": [100, 200],
        "profit": [20, 40],
        "discount": [0.1, 0.2],
        "quantity": [2, 4],
    })

    result = validate_retail_data(df)

    assert result["valid"] is True
    assert result["rows"] == 2


def test_missing_required_column():
    df = pd.DataFrame({
        "sales": [100],
        "profit": [20],
        "discount": [0.1],
    })

    result = validate_retail_data(df)

    assert result["valid"] is False
    assert "quantity" in result["missing_columns"]


def test_empty_dataset():
    df = pd.DataFrame(
        columns=["sales", "profit", "discount", "quantity"]
    )

    result = validate_retail_data(df)

    assert result["valid"] is False
    assert result["rows"] == 0
