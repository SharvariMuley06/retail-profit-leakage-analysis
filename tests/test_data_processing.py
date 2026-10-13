
import pandas as pd
import pytest

from src.data_processing import load_csv


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_csv("file_that_does_not_exist.csv")


def test_wrong_file_extension(tmp_path):
    file_path = tmp_path / "dataset.txt"
    file_path.write_text("sample data", encoding="utf-8")

    with pytest.raises(ValueError, match="Only CSV files"):
        load_csv(file_path)


def test_empty_file(tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="empty"):
        load_csv(file_path)


def test_duplicate_column_names(tmp_path):
    file_path = tmp_path / "duplicate_columns.csv"
    file_path.write_text(
        "sales,profit,sales\n100,20,100\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate column names"):
        load_csv(file_path)
