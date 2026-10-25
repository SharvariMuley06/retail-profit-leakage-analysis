
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

from src.data_processing import load_csv
from src.analytics import (
    calculate_overall_metrics,
    performance_by_category,
    performance_by_region,
    monthly_sales_trend,
    loss_making_orders,
    discount_analysis,
)
from ai_assistant.assistant import answer_question

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "Data" / "Processed" / "final_retail_dataset.csv"
FLAGGED_ANOMALIES_PATH = ROOT / "Reports" / "flagged_anomalies.csv"
INVESTIGATION_SUMMARY_PATH = (
    ROOT / "Reports" / "profit_leakage_investigation_summary.csv"
)

st.set_page_config(
    page_title="Retail Intelligence AI",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
    .ri-hero {
        background: linear-gradient(120deg,#eaf3ff,#f5fbff 60%,#e8faf6);
        border: 1px solid #d5e4f4;
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 22px;
    }
    .ri-eyebrow {
        color: #087e8b;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
    }
    .ri-title {
        color: #122943;
        font-size: 32px;
        font-weight: 800;
        margin: 8px 0;
    }
    .ri-subtitle {
        color: #4d627b;
    }
    .ri-card {
        background: white;
        border: 1px solid #dce6f2;
        border-radius: 14px;
        padding: 17px;
        min-height: 105px;
    }
    .ri-label {
        color: #62748a;
        font-size: 12px;
        font-weight: 800;
        margin-bottom: 12px;
    }
    .ri-value {
        color: #10243d;
        font-size: 25px;
        font-weight: 800;
    }

    /* Improve readability of assistant responses and tables. */
    .stChatMessage {
        border-radius: 14px;
    }
    [data-testid="stChatMessage"] {
        width: 100%;
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        width: 100%;
        overflow-wrap: anywhere;
    }
    [data-testid="stChatMessage"] table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
    }
    [data-testid="stChatMessage"] th,
    [data-testid="stChatMessage"] td {
        text-align: left;
        padding: 9px 12px;
        border-bottom: 1px solid #dce6f2;
        vertical-align: top;
    }
    [data-testid="stChatMessage"] th {
        font-weight: 700;
    }
    [data-testid="stChatMessage"] pre {
        white-space: pre-wrap;
        overflow-wrap: anywhere;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_data(path):
    return load_csv(path)


@st.cache_data
def get_investigation_reports(flagged_path, summary_path):
    return pd.read_csv(flagged_path), pd.read_csv(summary_path)


def flag_mask(series):
    values = series.astype("string").str.strip().str.lower()
    return values.isin({"true", "1", "1.0", "yes", "y", "t"})


def money(value):
    try:
        if pd.isna(value):
            return "—"
        return f"{float(value):,.2f}"
    except (TypeError, ValueError):
        return str(value)


def number(value):
    try:
        if pd.isna(value):
            return "—"
        return f"{float(value):,.0f}"
    except (TypeError, ValueError):
        return str(value)


def read_selection(event, field="x"):
    """Extract the clicked x value from a Plotly selection event."""
    try:
        points = event.selection.points
        if points:
            value = points[0].get(field)
            if value is not None:
                return str(value)
    except (AttributeError, TypeError, KeyError):
        pass
    return None


def chart_key(name):
    return f"{name}_{st.session_state.chart_version}"


def render_chart(fig, key):
    """Render a Plotly chart with point-click selection."""
    return st.plotly_chart(
        fig,
        key=key,
        use_container_width=True,
        on_select="rerun",
        selection_mode="points",
        config={"displaylogo": False, "scrollZoom": True},
    )


def render_ai_assistant():
    """Display the AI assistant in the dashboard with readable responses."""
    st.divider()
    st.subheader("🤖 Retail AI Assistant")
    st.caption(
        "Ask questions about sales, profit, categories, regions, monthly "
        "trends, anomalies, discounts, or individual orders."
    )

    if "ai_chat_history" not in st.session_state:
        st.session_state.ai_chat_history = []

    top_left, top_right = st.columns([5, 1])
    with top_right:
        if st.button("Clear chat", key="clear_ai_chat", use_container_width=True):
            st.session_state.ai_chat_history = []
            st.rerun()

    # Display the conversation history.
    for message in st.session_state.ai_chat_history:
        with st.chat_message(message["role"]):
            # Markdown rendering supports headings, tables, and lists.
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask about your retail data...",
        key="retail_ai_chat_input",
    )

    if question:
        st.session_state.ai_chat_history.append(
            {"role": "user", "content": question}
        )

        try:
            with st.spinner("Analyzing your retail data..."):
                answer = answer_question(question)
        except Exception as exc:
            answer = (
                "### Unable to answer this question\n\n"
                "Please check that the FastAPI server is running and the "
                "required dataset and reports are available.\n\n"
                f"**Details:** {exc}"
            )

        st.session_state.ai_chat_history.append(
            {"role": "assistant", "content": answer}
        )
        st.rerun()


def render_anomaly_investigation():
    st.subheader("Anomaly Investigation")

    missing_paths = [
        path for path in [
            FLAGGED_ANOMALIES_PATH,
            INVESTIGATION_SUMMARY_PATH,
        ]
        if not path.is_file()
    ]
    if missing_paths:
        for path in missing_paths:
            st.error(f"Required anomaly report not found: {path}")
        return

    try:
        flagged, summary = get_investigation_reports(
            str(FLAGGED_ANOMALIES_PATH),
            str(INVESTIGATION_SUMMARY_PATH),
        )
    except Exception as exc:
        st.error(f"Could not load the anomaly investigation reports: {exc}")
        return

    flag_columns = {
        "negative_profit_flag": "Negative-profit flagged records",
        "high_discount_flag": "High-discount flagged records",
        "high_shipping_flag": "High-shipping-cost flagged records",
    }

    kpi_columns = st.columns(4)
    kpi_columns[0].metric("Total flagged anomalies", f"{len(flagged):,}")

    for index, (column, label) in enumerate(flag_columns.items(), start=1):
        count = int(flag_mask(flagged[column]).sum()) if column in flagged else 0
        kpi_columns[index].metric(label, f"{count:,}")

    st.markdown("#### Investigation Summary")
    st.dataframe(summary, use_container_width=True, hide_index=True)

    report = flagged.copy()
    for column in flag_columns:
        if column in report.columns:
            report[column] = flag_mask(report[column])

    filter_columns = st.columns(4)

    category_options = (
        sorted(report["category"].dropna().astype(str).unique().tolist())
        if "category" in report.columns else []
    )
    region_options = (
        sorted(report["region"].dropna().astype(str).unique().tolist())
        if "region" in report.columns else []
    )

    selected_category = filter_columns[0].selectbox(
        "Category", ["All"] + category_options, key="anomaly_category"
    )
    selected_region = filter_columns[1].selectbox(
        "Region", ["All"] + region_options, key="anomaly_region"
    )
    anomaly_type = filter_columns[2].selectbox(
        "Anomaly type",
        ["All", "Negative profit", "High discount", "High shipping cost"],
        key="anomaly_type",
    )
    profit_status = filter_columns[3].selectbox(
        "Profit status",
        ["All", "Negative profit", "Zero/positive profit"],
        key="anomaly_profit_status",
    )

    filtered = report.copy()

    if selected_category != "All" and "category" in filtered.columns:
        filtered = filtered[
            filtered["category"].astype("string") == selected_category
        ]

    if selected_region != "All" and "region" in filtered.columns:
        filtered = filtered[
            filtered["region"].astype("string") == selected_region
        ]

    anomaly_flags = {
        "Negative profit": "negative_profit_flag",
        "High discount": "high_discount_flag",
        "High shipping cost": "high_shipping_flag",
    }

    if anomaly_type != "All":
        flag_column = anomaly_flags[anomaly_type]
        if flag_column in filtered.columns:
            filtered = filtered[filtered[flag_column]]
        else:
            filtered = filtered.iloc[0:0]

    if profit_status != "All":
        if "profit" in filtered.columns:
            profits = pd.to_numeric(filtered["profit"], errors="coerce")
            if profit_status == "Negative profit":
                filtered = filtered[profits < 0]
            else:
                filtered = filtered[profits >= 0]
        else:
            filtered = filtered.iloc[0:0]

    display_columns = [
        "order_id", "order_date", "product_name", "category", "region",
        "sales", "profit", "discount", "shipping_cost", "anomaly_score",
        "negative_profit_flag", "high_discount_flag", "high_shipping_flag",
    ]
    available_columns = [
        column for column in display_columns if column in filtered.columns
    ]

    st.markdown("#### Filtered Anomaly Records")

    if filtered.empty:
        st.info("No anomaly records match the selected filters.")
    elif available_columns:
        st.dataframe(
            filtered[available_columns],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No displayable transaction columns are available.")

    st.download_button(
        "Download filtered anomaly records",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_anomalies.csv",
        mime="text/csv",
        key="download_filtered_anomalies",
    )

    st.markdown("#### Transaction Details")

    if "order_id" not in filtered.columns:
        st.info("Transaction details are unavailable because order_id is missing.")
        return

    order_ids = filtered["order_id"].dropna().astype(str).unique().tolist()

    if not order_ids:
        st.info("No transactions are available for the selected filters.")
        return

    selected_order_id = st.selectbox(
        "Select order_id",
        order_ids,
        key="anomaly_order_id",
    )
    details = filtered[
        filtered["order_id"].astype("string") == selected_order_id
    ]
    st.dataframe(details, use_container_width=True, hide_index=True)


def main():
    try:
        df = get_data(DATA_PATH)
    except Exception as exc:
        st.error(f"Could not load the dataset: {exc}")
        st.info(f"Expected dataset: {DATA_PATH}")
        return

    required = {"sales", "profit", "quantity"}
    missing = required - set(df.columns)

    if missing:
        st.error(f"Dataset is missing required columns: {sorted(missing)}")
        return

    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(
            df["order_date"], errors="coerce", dayfirst=True
        )

    for col in ["sales", "profit", "quantity", "discount", "shipping_cost"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "chart_version" not in st.session_state:
        st.session_state.chart_version = 0

    st.markdown(
        """
        <div class="ri-hero">
            <div class="ri-eyebrow">RETAIL INTELLIGENCE</div>
            <div class="ri-title">Retail Profit Leakage Analysis</div>
            <div class="ri-subtitle">
                Select a category, region or month in a chart to cross-filter
                the other charts and transaction details.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    version = st.session_state.chart_version
    selected_category = read_selection(
        st.session_state.get(f"category_chart_{version}")
    )
    selected_region = read_selection(
        st.session_state.get(f"region_chart_{version}")
    )
    selected_month = read_selection(
        st.session_state.get(f"month_chart_{version}")
    )

    if st.button("↻ Clear all chart selections"):
        st.session_state.chart_version += 1
        st.rerun()

    filtered = df.copy()

    if selected_category and "category" in filtered.columns:
        filtered = filtered[
            filtered["category"].astype(str) == selected_category
        ]

    if selected_region and "region" in filtered.columns:
        filtered = filtered[
            filtered["region"].astype(str) == selected_region
        ]

    if selected_month and "order_date" in filtered.columns:
        month_values = filtered["order_date"].dt.strftime("%Y-%m")
        filtered = filtered[month_values == selected_month]

    active = []
    if selected_category:
        active.append(f"Category: {selected_category}")
    if selected_region:
        active.append(f"Region: {selected_region}")
    if selected_month:
        active.append(f"Month: {selected_month}")

    if active:
        st.info("Active chart filters: " + " | ".join(active))
    else:
        st.caption("No chart selection active — showing all records.")

    if filtered.empty:
        st.warning("No records match the current chart selections.")
        render_ai_assistant()
        return

    try:
        metrics = calculate_overall_metrics(filtered)
    except Exception as exc:
        st.error(f"Could not calculate KPIs: {exc}")
        render_ai_assistant()
        return

    cols = st.columns(4)
    kpis = [
        ("Total sales", money(metrics.get("total_sales"))),
        ("Total profit", money(metrics.get("total_profit"))),
        ("Total quantity", number(metrics.get("total_quantity"))),
        (
            "Profit margin",
            (
                f"{float(metrics['profit_margin_pct']):.2f}%"
                if metrics.get("profit_margin_pct") is not None
                else "—"
            ),
        ),
    ]

    for col, (label, value) in zip(cols, kpis):
        col.markdown(
            f"""
            <div class="ri-card">
                <div class="ri-label">{label}</div>
                <div class="ri-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption(f"Showing {len(filtered):,} of {len(df):,} records.")

    if "category" in filtered.columns:
        st.subheader("Performance by Category")
        try:
            categories = performance_by_category(filtered)

            if not categories.empty:
                fig = px.bar(
                    categories,
                    x="category",
                    y="total_sales",
                    color="total_profit",
                    hover_data=[
                        c for c in ["total_profit", "order_records"]
                        if c in categories.columns
                    ],
                    title="Sales by Category — click a bar to filter",
                    color_continuous_scale="Teal",
                )
                fig.update_layout(
                    clickmode="event+select",
                    xaxis_title="Category",
                    yaxis_title="Sales",
                )
                render_chart(fig, chart_key("category_chart"))
            else:
                st.info("No category data available.")
        except Exception as exc:
            st.error(f"Category chart failed: {exc}")

    if "region" in filtered.columns:
        st.subheader("Performance by Region")
        try:
            regions = performance_by_region(filtered)

            if not regions.empty:
                regions = regions.sort_values("total_sales", ascending=True)
                fig = px.bar(
                    regions,
                    x="region",
                    y="total_sales",
                    color="total_profit",
                    hover_data=[
                        c for c in ["total_profit"] if c in regions.columns
                    ],
                    title="Sales by Region — click a bar to filter",
                    color_continuous_scale="Blues",
                )
                fig.update_layout(
                    clickmode="event+select",
                    xaxis_title="Region",
                    yaxis_title="Sales",
                )
                render_chart(fig, chart_key("region_chart"))
            else:
                st.info("No regional data available.")
        except Exception as exc:
            st.error(f"Region chart failed: {exc}")

    if "order_date" in filtered.columns:
        st.subheader("Monthly Sales & Profit Trend")
        try:
            monthly = monthly_sales_trend(filtered)

            if not monthly.empty:
                monthly["month"] = monthly["month"].astype(str)
                monthly = monthly.sort_values("month")

                fig = px.line(
                    monthly,
                    x="month",
                    y=["total_sales", "total_profit"],
                    markers=True,
                    title="Monthly trend — click a point to filter",
                )
                fig.update_layout(
                    clickmode="event+select",
                    xaxis_title="Month",
                    yaxis_title="Amount",
                    legend_title="Metric",
                )
                render_chart(fig, chart_key("month_chart"))
            else:
                st.info("No monthly trend data available.")
        except Exception as exc:
            st.error(f"Monthly trend failed: {exc}")

    st.subheader("Loss-Making Transactions")
    try:
        losses = loss_making_orders(filtered)

        if not losses.empty:
            display_cols = [
                c for c in [
                    "order_id", "order_date", "product_name", "category",
                    "region", "discount", "sales", "profit", "shipping_cost",
                    "customer_name",
                ]
                if c in losses.columns
            ]
            st.caption(f"{len(losses):,} loss-making records in this selection.")
            st.dataframe(
                losses[display_cols].head(100),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.success("No loss-making records in this selection.")
    except Exception as exc:
        st.error(f"Loss-making transaction analysis failed: {exc}")

    st.subheader("Discount Analysis")
    try:
        discount = discount_analysis(filtered)

        if not discount.empty:
            st.dataframe(
                discount.head(20),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No discount analysis data available.")
    except Exception as exc:
        st.error(f"Discount analysis failed: {exc}")

    render_anomaly_investigation()
    render_ai_assistant()


if __name__ == "__main__":
    main()
