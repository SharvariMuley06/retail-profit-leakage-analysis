# Retail Profit Leakage & Performance Analysis

## Project Overview

Retail businesses can generate strong sales while still losing profitability through excessive discounting, high-cost transactions, and underperforming products.

This project analyzes retail sales and profitability data to identify **profit leakage patterns, quantify their statistical significance, and translate the findings into actionable business recommendations**.

A retail analytics project that combines business performance analysis, machine learning-based anomaly detection, and interactive dashboards to identify potential profit leakage.

## Features

- **Retail Analytics:** Analyze sales, profit, discounts, categories, regions, and monthly trends.
- **Anomaly Detection:** Use Isolation Forest to identify unusual retail transactions.
- **Profit Leakage Investigation:** Flag negative-profit transactions, high discounts, and high shipping costs.
- **Interactive Dashboard:** Explore KPIs, charts, and flagged transactions using Streamlit.
- **FastAPI Backend:** Provide analytics through REST API endpoints.
- **Retail Analytics Assistant:** Ask supported questions about business metrics, regional performance, anomalies, and individual orders.

---

## Business Objective

The primary objective is to answer:

> **Where is profit leaking, what factors are associated with lower profitability, and what actions can help reduce profit leakage?**

Key business questions include:

- How are sales and profit changing over time?
- Which categories and markets generate the most sales and profit?
- Which products and customers contribute to profitability?
- Where are loss-making transactions concentrated?
- How does discounting affect profit margin?
- Are differences in profitability across discount levels statistically significant?
- Which discount levels require greater business attention?
---

## Dataset

This project uses the **Global Retail dataset** as the primary retail transaction dataset and two external World Bank datasets for economic enrichment.

### 1. Global Retail Dataset

The **Global Retail dataset** is the primary dataset used for the project.

It contains retail transaction-level information covering:

- Orders
- Customers
- Products
- Categories
- Sub-Categories
- Sales
- Profit
- Discount
- Quantity
- Markets
- Countries
- Regions
- Shipping
- Order Priority
- Order Dates
- Delivery Information

  The final analytical dataset contains:

- **51,290 records**
- **49 columns**

The Global Retail dataset forms the foundation of the analysis and is used for sales, profitability, customer, product, market, discount, and operational analysis.

### 2. World Bank GDP Growth Dataset

GDP growth data was used as an external economic enrichment dataset.

It provides additional economic context for the countries and time periods represented in the Global Retail data.

The integrated feature is:

- `gdp_growth`

### 3. World Bank Inflation Dataset

Inflation data was used as a second external economic enrichment dataset.

It provides additional economic context for the retail transactions by incorporating inflation conditions across relevant countries and time periods.

The integrated feature is:

- `inflation_rate`

### Data Enrichment & Integration

The three datasets were cleaned, transformed, and integrated using relevant **geographic and time dimensions**.

```text
Global Retail Dataset
        +
World Bank GDP Growth
        +
World Bank Inflation
        ↓
Enriched Global Retail Analytical Dataset
```
The enrichment adds external economic context to the original Global Retail transaction data, allowing the project to move beyond basic sales reporting toward broader business, profitability, and economic performance analysis.

### Additional Analytical Features

Additional analytical features were created during the project, including:

- `profit_margin`
- `discount_band`
- `loss_order`
- `high_discount`
- `sales_bucket`
- `profit_bucket`
- `shipping_cost_bucket`
- `average_order_value`
- `shipping_cost_pct`
- `discount_amount`
- `net_sales`
- `profit_status`
- `delivery_status`
- `profit_per_unit`
- `gdp_growth`
- `inflation_rate`

---

## Project Workflow

```text
├── Data/
│   ├── Processed/
│   └── External/
├── Reports/
│   ├── anomaly_detection_results.csv
│   ├── flagged_anomalies.csv
│   └── profit_leakage_investigation_summary.csv
├── Python/
├── SQL/
├── PowerBI/
├── Screenshots/
├── src/
│   ├── data_processing.py
│   └── analytics.py
├── ml/
│   └── anomaly_detection.py
├── api/
│   └── main.py
├── ai_assistant/
│   └── assistant.py
├── app.py
├── README.md
```
## Tools & Technologies

| Technology | Purpose |
|---|---|
| Python | Data processing and analysis |
| Pandas and NumPy | Data manipulation and numerical analysis |
| SciPy and Statsmodels | Statistical testing |
| Scikit-learn | Isolation Forest anomaly detection |
| SQL | Business queries and aggregations |
| Power BI | Interactive business intelligence dashboards |
| Streamlit and Plotly | Interactive analytics application |
| FastAPI and Uvicorn | Analytics API |
| Git and GitHub | Version control and project presentation |


## Key Statistical Results
### Analysis	                    Result
Pearson Correlation                	-0.8464
Pearson P-value	                    < 0.001
Welch's ANOVA Statistic            	11,077.2888
Welch's ANOVA P-value	            < 0.001
Eta Squared	                        0.7517
Loss-Making Transactions	        12,544
Loss-Making Rate	                24.46%
High-Discount Loss Transactions	    9,579
Share of Loss-Making Transactions	76.36%

These results indicate a strong negative association between discount and profit margin and statistically significant differences in profitability across discount bands.

### Main Dashboard
<img width="1136" height="650" alt="image" src="https://github.com/user-attachments/assets/fb0f7dbd-33e5-442a-8e7a-e298b52a69fe" />

The Power BI solution converts the analytical results into interactive business dashboards.

### AI_assistant
<img width="1916" height="713" alt="ai_assistant" src="https://github.com/user-attachments/assets/bbc8a924-9078-4768-83c8-69451a6954e0" />

Ask questions about sales, profitability, regional performance, anomalies, and individual orders using the interactive analytics assistant.

### Geographic Analysis

- Profit by Country
- Sales by Country
- Profit Leakage Countries

### Customer Analysis

- Top 10 Customers by Sales

### Product Analysis

- Top 10 Products by Sales
- Highest Profit Leakage Products

### Market Analysis

- Profit by Market
- Sales by Market

### Discount Analysis

- Profit Margin by Discount Band

### Operations

- Shipping Mode Distribution
- Orders by Priority

---

## Dashboard Purpose

The dashboard is designed to help business users answer:

- Where are we making money?
- Where are we losing money?
- Which products are causing leakage?
- Which customers generate high sales?
- Which markets perform best?
- Are discounts associated with lower profitability?
- Where should management investigate?

The Python statistical analysis provides analytical validation, while Power BI provides interactive decision support.

---

## Key Business Findings

### 1. Discount & Profitability

A strong negative relationship exists between discount and profit margin.

**Pearson correlation = -0.8464**

The relationship is statistically significant at **p < 0.001**.

---

### 2. Profitability Across Discount Bands

Welch's ANOVA confirms statistically significant differences in profit margins across discount bands.

**p < 0.001**

---

### 3. Large Effect Size

The effect size is:

**η² = 0.7517**

This indicates a very large association between discount-band grouping and observed profit-margin differences.

---

### 4. Loss-Making Transactions

- **12,544 loss-making transactions**
- **24.46% of total transactions**

---

### 5. High-Discount Losses

- **9,579 high-discount loss transactions**
- **76.36% of all loss-making transactions**

---

### 6. Extreme Discounting

The **Above 50% discount band** has the lowest observed average profit margin:

**-115.0090**

---

## Business Recommendations

### 1. Review High Discounting

Review high-discount transactions before approving similar promotions, as higher discounts are strongly associated with lower profit margins.

### 2. Control Extreme Discounts

Transactions with discounts above 50% should receive additional review because this discount band has the lowest average profit margin.

### 3. Investigate Loss-Making Transactions

Investigate loss-making transactions to identify recurring product, customer, market, or discount-related patterns.

### 4. Prioritize High-Discount Losses

Prioritize loss-making transactions with discounts above 30% for profit-leakage investigation.

### 5. Evaluate Promotions Using Profitability

Promotional performance should be evaluated using profit and profit margin rather than relying only on sales or revenue growth.

### 6. Establish Discount Controls

Statistical evidence can support discount thresholds, approval rules, and ongoing monitoring of promotion profitability.

---

## Important Statistical Interpretation

The analysis identifies **statistical associations and significant differences**.

It does not establish that discounting alone causes every observed change in profit margin.

Other business factors can also affect profitability, including:

- Product characteristics
- Cost structure
- Shipping cost
- Market
- Customer
- Quantity
- Pricing
- Operational factors

Therefore, the results should be used to identify areas for investigation and decision support rather than interpreted as a standalone causal model.

---

## Future Improvements

Potential future development includes:

- Predictive profit-risk scoring
- Automated profit-leakage alerts
- Customer profitability segmentation
- Product-level risk scoring
- Promotion effectiveness analysis
- Time-series forecasting
- Machine-learning-based loss prediction
- Automated reporting
- Scenario analysis for discount decisions

These extensions could turn the analytical framework into a more automated profitability monitoring system.

---
## Tech Stack

Python, Pandas, Scikit-learn, Streamlit, Plotly, FastAPI, Uvicorn, SQL, Power BI.

## Dataset

- **Records:** 51,290
- **Columns:** 49
- **File:** `Data/Processed/final_retail_dataset.csv`

The dataset contains order, customer, product, sales, profit, discount, shipping, and regional information.

## Machine Learning

The project uses **Isolation Forest**, an unsupervised machine learning algorithm, to identify unusual transaction patterns.

Features used:
- Sales
- Profit
- Discount
- Quantity
- Shipping cost

Configuration: 200 estimators, contamination of 0.03, random state 42.

## Results

| Metric | Result |
|---|---:|
| Transactions analyzed | 51,290 |
| Anomaly records flagged | 1,539 |
| Negative-profit anomaly flags | 544 |
| High-discount flags | 420 |
| High-shipping-cost flags | 312 |

Flag categories can overlap. An anomaly indicates a transaction requiring investigation, not necessarily fraud or a confirmed loss.

## Run the Project

Install the required packages:

```bash
python -m pip install pandas numpy scikit-learn streamlit plotly fastapi uvicorn requests tabulate
```

Start the API from the project root:

```bash
python -m uvicorn api.main:app --reload
```

Start the dashboard in a second terminal:

```bash
python -m streamlit run app.py
```

API documentation: `http://127.0.0.1:8000/docs`



## Author

**Sharvari Muley**

 Python | Pandas | NumPy | SQL | Scikit-learn | Machine Learning | Streamlit | FastAPI | Plotly | Power BI | Git & GitHub


## Copyright & Usage

© 2026 Sharvari Muley. All rights reserved.

This project is published for portfolio, educational, and evaluation purposes.

No permission is granted to copy, reproduce, modify, redistribute, or present this project or substantial portions of its code, analysis, documentation, or visualizations as another person's work without prior written permission.
