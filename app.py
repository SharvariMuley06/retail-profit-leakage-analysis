from pathlib import Path

import pandas as pd
import streamlit as st

# Project files
ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "Data" / "Processed" / "final_retail_dataset.csv"
REPORTS_DIR = ROOT / "Reports"
ANOMALY_PATH = REPORTS_DIR / "anomaly_detection_results.csv"
FLAGGED_PATH = REPORTS_DIR / "flagged_anomalies.csv"
SUMMARY_PATH = REPORTS_DIR / "profit_leakage_investigation_summary.csv"

st.set_page_config(
    page_title="Retail Intelligence AI",
    page_icon="📊",
    layout="wide",
)

# Safe light styling: only custom dashboard elements are styled.
st.markdown(
    """
    <style>
    .ri-hero {
        background: linear-gradient(120deg, #eaf3ff, #f5fbff 60%, #e8faf6);
        border: 1px solid #d5e4f4;
        border-radius: 18px;
        padding: 26px 28px;
        margin-bottom: 22px;
    }
    .ri-eyebrow {
        color: #087e8b;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .ri-title {
        color: #122943;
        font-size: 34px;
        font-weight: 800;
        margin: 8px 0;
    }
    .ri-subtitle {
        color: #4d627b;
        font-size: 16px;
    }
    .ri-card {
        background: #ffffff;
        border: 1px solid #dce6f2;
        border-radius: 14px;
        padding: 17px;
        min-height: 112px;
        box-shadow: 0 4px 14px rgba(24, 59, 99, 0.05);
    }
    .ri-label {
        color: #62748a;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }
    .ri-value {
        color: #10243d;
        font-size: 25px;
        font-weight: 800;
        overflow-wrap: anywhere;
    }
    .ri-line {
        height: 3px;
        width: 36px;
        border-radius: 5px;
        background: #3478f6;
        margin-top: 12px;
    }
    .ri-teal { background: #0baa9d; }
    .ri-purple { background: #8265d9; }
    .ri-orange { background: #e59a32; }
    .ri-insight {
        background: #ffffff;
        border: 1px solid #dce6f2;
        border-left: 4px solid #0baa9d;
        border-radius: 10px;
        padding: 12px 15px;
        margin-bottom: 10px;
        color: #253b55;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


