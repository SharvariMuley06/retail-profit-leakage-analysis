
from pathlib import Path
import re

import pandas as pd
import requests


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
API_BASE_URL = "http://127.0.0.1:8000"
DATA_PATH = PROJECT_ROOT / "Data" / "Processed" / "final_retail_dataset.csv"
REPORTS_DIR = PROJECT_ROOT / "Reports"


# --------------------------------------------------
# API and data helpers
# --------------------------------------------------

def api_get(endpoint, params=None):
    """Fetch data from the FastAPI backend."""
    try:
        response = requests.get(
            f"{API_BASE_URL}{endpoint}",
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        return {"error": f"API request failed: {exc}"}


def load_retail_data():
    """Load the processed retail dataset."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Retail dataset not found at: {DATA_PATH}"
        )

    return pd.read_csv(DATA_PATH, low_memory=False)


def load_report(filename):
    """Load a CSV report from the Reports directory."""
    path = REPORTS_DIR / filename

    if not path.exists():
        return None

    return pd.read_csv(path, low_memory=False)


def format_number(value, decimals=2):
    """Format numeric values for readable answers."""
    try:
        number = float(value)
        return f"{number:,.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)


def format_dataframe(df, max_rows=15):
    """Convert a DataFrame into a readable Markdown table."""
    if df is None or df.empty:
        return "_No records found._"

    display_df = df.head(max_rows).copy()

    for column in display_df.columns:
        if pd.api.types.is_float_dtype(display_df[column]):
            display_df[column] = display_df[column].map(
                lambda x: f"{x:,.2f}" if pd.notna(x) else ""
            )

    try:
        table = display_df.to_markdown(index=False)
    except ImportError:
        table = "```text\n" + display_df.to_string(index=False) + "\n```"

    if len(df) > max_rows:
        table += f"\n\n_Showing {max_rows} of {len(df):,} records._"

    return table


def find_column(df, *possible_names):
    """Find a column without depending on capitalization or spacing."""
    normalized = {
        str(column).strip().lower().replace("_", " "): column
        for column in df.columns
    }

    for name in possible_names:
        key = name.strip().lower().replace("_", " ")
        if key in normalized:
            return normalized[key]

    return None


# --------------------------------------------------
# Order investigation
# --------------------------------------------------

def investigate_order(order_id):
    """Investigate all dataset rows belonging to one order."""
    df = load_retail_data()

    order_column = find_column(
        df, "Order ID", "Order_ID", "OrderID"
    )

    if order_column is None:
        return "❌ The dataset does not contain an Order ID column."

    order_id = str(order_id).strip()
    matching = df[
        df[order_column].astype(str).str.strip().str.casefold()
        == order_id.casefold()
    ].copy()

    if matching.empty:
        return (
            f"## Order Investigation\n\n"
            f"No records were found for order **{order_id}**.\n\n"
            "Check that the Order ID is correct."
        )

    sales_col = find_column(matching, "Sales")
    profit_col = find_column(matching, "Profit")
    shipping_col = find_column(
        matching, "Shipping Cost", "Shipping_Cost"
    )
    discount_col = find_column(matching, "Discount")

    def total(column):
        if column is None:
            return None
        return pd.to_numeric(
            matching[column], errors="coerce"
        ).fillna(0).sum()

    sales = total(sales_col)
    profit = total(profit_col)
    shipping = total(shipping_col)
    discount = total(discount_col)

    if profit is None:
        status = "Unknown — profit column unavailable"
    elif profit < 0:
        status = "Loss-making"
    elif profit > 0:
        status = "Profitable"
    else:
        status = "Break-even"

    summary_rows = [
        ("Matching product rows", f"{len(matching):,}"),
        ("Total sales", format_number(sales) if sales is not None else "N/A"),
        ("Total profit", format_number(profit) if profit is not None else "N/A"),
        (
            "Total shipping cost",
            format_number(shipping) if shipping is not None else "N/A",
        ),
        (
            "Sum of row-level discounts",
            format_number(discount) if discount is not None else "N/A",
        ),
        ("Order status", status),
    ]

    output = [
        "## Order Investigation",
        f"**Order ID:** `{order_id}`",
        "",
        "### Order Summary",
        "| Metric | Value |",
        "|---|---:|",
    ]

    for label, value in summary_rows:
        output.append(f"| {label} | {value} |")

    # Check anomaly reports for this order, when available.
    flagged = load_report("flagged_anomalies.csv")
    anomaly_messages = []

    if flagged is not None:
        report_order_col = find_column(
            flagged, "Order ID", "Order_ID", "OrderID"
        )

        if report_order_col is not None:
            order_flags = flagged[
                flagged[report_order_col].astype(str).str.strip().str.casefold()
                == order_id.casefold()
            ]

            if not order_flags.empty:
                flag_columns = [
                    col for col in order_flags.columns
                    if "flag" in col.lower()
                ]

                for column in flag_columns:
                    values = order_flags[column].astype(str).str.lower()
                    if values.isin(["true", "1", "yes"]).any():
                        anomaly_messages.append(
                            column.replace("_", " ").title()
                        )

    output.extend(["", "### Anomaly Status"])

    if anomaly_messages:
        output.append(
            "**Review recommended:** " + ", ".join(sorted(set(anomaly_messages)))
        )
    else:
        output.append(
            "No matching flagged anomaly was found in the available anomaly report."
        )

    # Show useful product-level details.
    output.extend(["", "### Product Details"])

    preferred_names = [
        "Product Name", "Product", "Category", "Sub-Category",
        "Region", "Sales", "Profit", "Discount", "Shipping Cost",
    ]

    selected_columns = []
    for name in preferred_names:
        column = find_column(matching, name)
        if column is not None and column not in selected_columns:
            selected_columns.append(column)

    if selected_columns:
        details = matching[selected_columns].copy()
        output.append(format_dataframe(details, max_rows=20))
    else:
        output.append(format_dataframe(matching, max_rows=20))

    return "\n".join(output)


def extract_order_id(question):
    """Recognize an order ID even when the word 'order' is omitted."""
    match = re.search(
        r"\b[A-Z]{2}-\d{4}-\d{6}\b",
        question,
        flags=re.IGNORECASE,
    )
    return match.group(0) if match else None


# --------------------------------------------------
# Assistant response logic
# --------------------------------------------------

def answer_question(question):
    """Answer supported retail analytics questions."""
    question = str(question).strip()

    if not question:
        return "Please enter a question about your retail data."

    q = question.lower()

    # IMPORTANT: Check for an order ID BEFORE generic question routing.
    # This supports both "order CA-2011-118962" and the ID alone.
    order_id = extract_order_id(question)
    if order_id:
        try:
            return investigate_order(order_id)
        except (FileNotFoundError, pd.errors.ParserError, OSError) as exc:
            return f"❌ Could not investigate this order: {exc}"

    # API status
    if any(term in q for term in ["api status", "health check", "is api running"]):
        result = api_get("/health")

        if "error" in result:
            return f"## API Status\n\n❌ {result['error']}"

        return (
            "## API Status\n\n"
            f"```json\n{pd.Series(result).to_json(indent=2)}\n```"
        )

    # Overall metrics
    if any(
        term in q for term in [
            "overall metrics", "total sales", "total profit",
            "profit margin", "total quantity", "total records",
            "overall performance", "business overview",
        ]
    ):
        result = api_get("/analytics/overview")

        if "error" in result:
            return f"❌ {result['error']}"

        output = ["## Retail Business Overview", "", "| Metric | Value |", "|---|---:|"]

        for key, value in result.items():
            label = key.replace("_", " ").title()
            if isinstance(value, (int, float)):
                if "pct" in key.lower():
                    formatted = f"{value:,.2f}%"
                else:
                    formatted = format_number(value)
            else:
                formatted = str(value)
            output.append(f"| {label} | {formatted} |")

        return "\n".join(output)

    # Category ranking
    if "categor" in q:
        result = api_get("/analytics/category")

        if "error" in result:
            return f"❌ {result['error']}"

        df = pd.DataFrame(result)
        if df.empty:
            return "No category analytics were returned by the API."

        profit_col = find_column(df, "total_profit", "Total Profit", "profit")
        category_col = find_column(df, "category", "Category")

        if profit_col and category_col:
            df[profit_col] = pd.to_numeric(df[profit_col], errors="coerce")
            if "lowest" in q or "least" in q:
                df = df.sort_values(profit_col, ascending=True).head(1)
                title = "Category with the Lowest Profit"
            elif "highest" in q or "most" in q or "best" in q:
                df = df.sort_values(profit_col, ascending=False).head(1)
                title = "Category with the Highest Profit"
            else:
                df = df.sort_values(profit_col, ascending=False)
                title = "Profit by Category"
        else:
            title = "Category Analytics"

        return f"## {title}\n\n{format_dataframe(df)}"

    # Region ranking
    if "region" in q:
        result = api_get("/analytics/region")

        if "error" in result:
            return f"❌ {result['error']}"

        df = pd.DataFrame(result)
        if df.empty:
            return "No regional analytics were returned by the API."

        profit_col = find_column(df, "total_profit", "Total Profit", "profit")

        if profit_col:
            df[profit_col] = pd.to_numeric(df[profit_col], errors="coerce")

            if "lowest" in q or "least" in q:
                df = df.sort_values(profit_col).head(1)
                title = "Region with the Lowest Profit"
            elif "highest" in q or "most" in q or "best" in q:
                df = df.sort_values(profit_col, ascending=False).head(1)
                title = "Region with the Highest Profit"
            else:
                df = df.sort_values(profit_col, ascending=False)
                title = "Profit by Region"
        else:
            title = "Regional Analytics"

        return f"## {title}\n\n{format_dataframe(df)}"

    # Monthly sales trend
    if any(term in q for term in ["monthly", "month trend", "sales trend", "sales over time"]):
        result = api_get("/analytics/monthly-trend")

        if "error" in result:
            return f"❌ {result['error']}"

        df = pd.DataFrame(result)
        return f"## Monthly Sales Trend\n\n{format_dataframe(df, max_rows=24)}"

    # Loss-making records
    if any(term in q for term in ["loss-making", "loss making", "negative profit", "unprofitable"]):
        result = api_get("/analytics/loss-making", params={"limit": 100, "offset": 0})

        if "error" in result:
            return f"❌ {result['error']}"

        if isinstance(result, dict):
            records = result.get("data", result.get("records", []))
            total = result.get("total", result.get("total_records"))
            df = pd.DataFrame(records)
        else:
            df = pd.DataFrame(result)
            total = None

        heading = "## Loss-Making Transactions\n\n"
        if total is not None:
            heading += f"**Total loss-making records:** {total:,}\n\n"

        return heading + format_dataframe(df, max_rows=20)

    # Discount analysis
    if "discount" in q:
        result = api_get("/analytics/discount")

        if "error" in result:
            return f"❌ {result['error']}"

        df = pd.DataFrame(result)
        return f"## Discount Analysis\n\n{format_dataframe(df)}"

    # Profit leakage investigation summary
    if any(term in q for term in ["leakage summary", "investigation summary", "profit leakage summary"]):
        df = load_report("profit_leakage_investigation_summary.csv")

        if df is None:
            return "❌ The profit leakage investigation summary report was not found."

        return (
            "## Profit Leakage Investigation Summary\n\n"
            f"{format_dataframe(df, max_rows=20)}"
        )

    # Anomaly count
    if any(term in q for term in ["anomal", "flagged transactions", "flagged records"]):
        df = load_report("flagged_anomalies.csv")

        if df is None:
            return "❌ The flagged anomalies report was not found."

        return (
            "## Anomaly Detection Summary\n\n"
            f"**Flagged anomaly records:** {len(df):,}\n\n"
            "These are records flagged by the anomaly detection pipeline; "
            "a flag does not by itself prove fraud or an actual loss."
        )

    # High-discount / high-shipping investigation
    if "high discount" in q or "discount flag" in q:
        df = load_report("flagged_anomalies.csv")
        if df is None:
            return "❌ The flagged anomalies report was not found."

        flag_col = find_column(df, "high_discount_flag")
        if flag_col is None:
            return "The report does not contain a high-discount flag column."

        flags = df[flag_col].astype(str).str.lower().isin(["true", "1", "yes"])
        return f"## High-Discount Flags\n\n**Flagged records:** {int(flags.sum()):,}"

    if "high shipping" in q or "shipping flag" in q:
        df = load_report("flagged_anomalies.csv")
        if df is None:
            return "❌ The flagged anomalies report was not found."

        flag_col = find_column(df, "high_shipping_flag")
        if flag_col is None:
            return "The report does not contain a high-shipping flag column."

        flags = df[flag_col].astype(str).str.lower().isin(["true", "1", "yes"])
        return f"## High-Shipping-Cost Flags\n\n**Flagged records:** {int(flags.sum()):,}"

    # Help
    return (
        "## Retail AI Assistant\n\n"
        "I can answer questions about:\n\n"
        "- **Overall metrics:** total sales, profit, quantity, and profit margin\n"
        "- **Categories and regions:** highest or lowest profit\n"
        "- **Monthly trends:** sales over time\n"
        "- **Loss-making transactions**\n"
        "- **Discount analysis**\n"
        "- **Anomaly counts and investigation flags**\n"
        "- **Profit leakage investigation summary**\n"
        "- **Individual orders:** enter an ID such as `CA-2011-118962`\n\n"
        "Try asking: **Which region has the lowest profit?**"
    )


# --------------------------------------------------
# Terminal testing
# --------------------------------------------------

if __name__ == "__main__":
    print("Retail AI Assistant")
    print("Type 'exit' to stop.\n")

    while True:
        user_question = input("You: ").strip()

        if user_question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        print("\nAssistant:\n")
        print(answer_question(user_question))
        print("\n" + "-" * 60 + "\n")
