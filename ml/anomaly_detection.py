
from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest


FEATURE_COLUMNS = [
    "sales",
    "profit",
    "discount",
    "quantity",
    "shipping_cost",
]


def detect_anomalies(
    df: pd.DataFrame,
    contamination: float = 0.03,
    random_state: int = 42,
) -> pd.DataFrame:
    """Flag unusual retail records using Isolation Forest."""

    if not 0 < contamination < 0.5:
        raise ValueError(
            "contamination must be greater than 0 and less than 0.5."
        )

    missing = set(FEATURE_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    results = df.copy()

    features = results[FEATURE_COLUMNS].apply(
        pd.to_numeric, errors="coerce"
    )
    features = features.replace(
        [float("inf"), float("-inf")], float("nan")
    )

    valid_mask = features.notna().all(axis=1)
    results["anomaly_score"] = float("nan")
    results["is_anomaly"] = False

    if valid_mask.sum() < 2:
        raise ValueError(
            "At least two records with valid numeric features are required."
        )

    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1,
    )

    valid_features = features.loc[valid_mask]
    model.fit(valid_features)

    results.loc[valid_mask, "anomaly_score"] = (
        model.decision_function(valid_features)
    )
    results.loc[valid_mask, "is_anomaly"] = (
        model.predict(valid_features) == -1
    )

    return results


def build_investigation_report(
    results: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create independent investigation flags and summary metrics."""

    flagged = results.loc[results["is_anomaly"]].copy()

    # Convert values safely for consistent business calculations.
    for column in ["sales", "profit", "discount", "shipping_cost"]:
        flagged[column] = pd.to_numeric(
            flagged[column], errors="coerce"
        )

    # These thresholds are initial business rules, not ML predictions.
    flagged["negative_profit_flag"] = flagged["profit"] < 0
    flagged["high_discount_flag"] = flagged["discount"] >= 0.40
    flagged["high_shipping_flag"] = (
        flagged["shipping_cost"] > flagged["sales"].abs() * 0.20
    )

    flagged["negative_profit_and_high_discount"] = (
        flagged["negative_profit_flag"]
        & flagged["high_discount_flag"]
    )

    flagged["negative_profit_and_high_shipping"] = (
        flagged["negative_profit_flag"]
        & flagged["high_shipping_flag"]
    )

    flagged["negative_profit_high_discount_high_shipping"] = (
        flagged["negative_profit_flag"]
        & flagged["high_discount_flag"]
        & flagged["high_shipping_flag"]
    )

    # Positive amount representing the magnitude of negative profit.
    flagged["negative_profit_amount"] = (
    (-flagged["profit"].clip(upper=0)).clip(lower=0)
)
    categories = [
        ("Negative profit", "negative_profit_flag"),
        ("High discount", "high_discount_flag"),
        ("High shipping cost", "high_shipping_flag"),
        (
            "Negative profit and high discount",
            "negative_profit_and_high_discount",
        ),
        (
            "Negative profit and high shipping cost",
            "negative_profit_and_high_shipping",
        ),
        (
            "Negative profit, high discount and high shipping cost",
            "negative_profit_high_discount_high_shipping",
        ),
    ]

    summary_rows = []

    for category, flag_column in categories:
        group = flagged.loc[flagged[flag_column]]

        summary_rows.append(
            {
                "investigation_category": category,
                "flagged_records": int(len(group)),
                "total_negative_profit": round(
                    float(group["negative_profit_amount"].sum()), 2
                ),
                "total_sales": round(
                    float(group["sales"].sum()), 2
                ),
                "total_profit": round(
                    float(group["profit"].sum()), 2
                ),
            }
        )

    summary = pd.DataFrame(summary_rows)

    return flagged, summary


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent

    dataset_path = (
        project_root
        / "Data"
        / "Processed"
        / "final_retail_dataset.csv"
    )

    reports_dir = project_root / "Reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(dataset_path)

    results = detect_anomalies(df)
    flagged, summary = build_investigation_report(results)

    all_results_path = reports_dir / "anomaly_detection_results.csv"
    flagged_path = reports_dir / "flagged_anomalies.csv"
    summary_path = (
        reports_dir / "profit_leakage_investigation_summary.csv"
    )

    results.to_csv(all_results_path, index=False)
    flagged.to_csv(flagged_path, index=False)
    summary.to_csv(summary_path, index=False)

    print("\n=== ANOMALY DETECTION SUMMARY ===")
    print("Total records:", len(results))
    print("Flagged records:", len(flagged))
    print(
        "Percentage flagged:",
        round(len(flagged) / len(results) * 100, 2),
        "%",
    )

    print("\n=== INDEPENDENT INVESTIGATION SUMMARY ===")
    print(summary.to_string(index=False))

    print("\n=== FLAGGED RECORDS WITH NEGATIVE PROFIT ===")
    negative = flagged.loc[flagged["negative_profit_flag"]]
    print("Count:", len(negative))
    print(
        "Combined negative profit:",
        round(float(negative["negative_profit_amount"].sum()), 2),
    )

    print("\n=== REPORTS SAVED ===")
    print(all_results_path)
    print(flagged_path)
    print(summary_path)
