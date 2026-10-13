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


# --- Minimal dashboard renderer (smallest safe fix) ---
# Use package imports from src/ (src is a package in this repo)
from src.data_processing import load_csv
from src.analytics import (
    calculate_overall_metrics,
    performance_by_category,
    performance_by_region,
    monthly_sales_trend,
    loss_making_orders,
    discount_analysis,
)


def _format_kpi(value, is_pct: bool = False) -> str:
    """Format KPI values safely for display.

    - Returns an em dash for missing/None values.
    - Formats numeric values with commas; percentages with 2 decimals + %.
    - Falls back to str(value) if formatting fails.
    """
    if value is None:
        return "—"
    try:
        v = float(value)
    except Exception:
        # If it's a string or non-numeric, return as-is (but safe)
        return str(value)

    if is_pct:
        return f"{v:.2f}%"

    # Formatting for large numbers; show no decimals for whole numbers
    if abs(v - round(v)) < 1e-9:
        return f"{int(round(v)):,}"

    return f"{v:,.2f}"


def _render_dashboard() -> None:
    """Render the minimal dashboard UI using existing analytics functions."""
    try:
        df = load_csv(DATA_PATH)
    except Exception as e:
        st.error(f"Failed to load dataset at {DATA_PATH}: {e}")
        return

    # Header / hero
    st.markdown(
        f"""
        <div class="ri-hero">
            <div class="ri-eyebrow">Retail Intelligence</div>
            <div class="ri-title">Retail Profit Leakage Analysis</div>
            <div class="ri-subtitle">Interactive dashboard — KPIs, category & region analysis, trends and anomalies.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Overall KPIs
    try:
        metrics = calculate_overall_metrics(df)
    except Exception as e:
        st.error(f"Failed calculating overall metrics: {e}")
        metrics = {}

    total_sales = _format_kpi(metrics.get("total_sales"))
    total_profit = _format_kpi(metrics.get("total_profit"))
    total_quantity = _format_kpi(metrics.get("total_quantity"))
    profit_margin = _format_kpi(metrics.get("profit_margin_pct"), is_pct=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"<div class='ri-card'><div class='ri-label'>Total sales</div><div class='ri-value'>{total_sales}</div></div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"<div class='ri-card'><div class='ri-label'>Total profit</div><div class='ri-value'>{total_profit}</div></div>",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"<div class='ri-card'><div class='ri-label'>Total quantity</div><div class='ri-value'>{total_quantity}</div></div>",
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"<div class='ri-card'><div class='ri-label'>Profit margin %</div><div class='ri-value'>{profit_margin}</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("## Performance by Category")
    try:
        cat_df = performance_by_category(df)
        st.dataframe(cat_df.head(15), use_container_width=True)
    except Exception as e:
        st.error(f"Category performance failed: {e}")

    st.markdown("## Performance by Region")
    try:
        reg_df = performance_by_region(df)
        if not reg_df.empty and "region" in reg_df.columns and "total_sales" in reg_df.columns:
            st.bar_chart(reg_df.set_index("region")["total_sales"])
        else:
            st.info("No region sales data to chart.")
    except Exception as e:
        st.error(f"Region performance failed: {e}")

    st.markdown("## Monthly sales & profit trend")
    try:
        monthly = monthly_sales_trend(df)
        if not monthly.empty:
            monthly_plot = monthly.set_index("month")[ ["total_sales", "total_profit"] ].sort_index()
            st.line_chart(monthly_plot)
        else:
            st.info("No monthly trend data available after parsing order_date.")
    except Exception as e:
        st.error(f"Monthly trend failed: {e}")

    st.markdown("## Loss-making orders (example)")
    try:
        losses = loss_making_orders(df)
        st.dataframe(losses.head(10), use_container_width=True)
    except Exception as e:
        st.error(f"Loss-making orders failed: {e}")

    st.markdown("## Discount analysis (sample)")
    try:
        disc = discount_analysis(df)
        st.dataframe(disc.head(10), use_container_width=True)
    except Exception as e:
        st.error(f"Discount analysis failed: {e}")


# Execute render when Streamlit runs this module.
_render_dashboard()
