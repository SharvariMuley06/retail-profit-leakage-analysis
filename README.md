# Retail Profit Leakage & Performance Analysis

## Project Overview

Retail businesses can generate strong sales while still losing profitability through excessive discounting, high-cost transactions, and underperforming products.

This project analyzes retail sales and profitability data to identify **profit leakage patterns, quantify their statistical significance, and translate the findings into actionable business recommendations**.

The project combines:

- Python for data analysis and statistical validation
- SQL for business-oriented data analysis
- Power BI for interactive dashboards and decision support
- Statistical hypothesis testing to validate relationships and differences in profitability

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

## What Makes This Project Different

This project is not limited to creating a Power BI dashboard.

It combines four analytical layers:

### Layer 1 — Data

Cleaning, integration, and feature engineering.

### Layer 2 — Business Analytics

SQL-based analysis of customers, products, markets, and profitability.

### Layer 3 — Statistical Validation

Correlation, hypothesis testing, ANOVA, Welch's ANOVA, Tukey HSD, Kruskal-Wallis, and effect-size analysis.

### Layer 4 — Decision Support

Power BI dashboards and business recommendations.

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
Raw Data
    ↓
Data Cleaning & Validation
    ↓
Feature Engineering
    ↓
SQL Business Analysis
    ↓
Exploratory Data Analysis
    ↓
Power BI Dashboard
    ↓
Statistical Analysis
    ↓
Hypothesis Testing
    ↓
Business Findings
    ↓
Business Recommendations
```
## Tools & Technologies
Tool	        Purpose
Python	        Data cleaning, EDA, and statistical analysis
Pandas	        Data manipulation
NumPy	        Numerical analysis
SciPy	        Statistical testing
Statsmodels 	ANOVA and post-hoc analysis
Matplotlib	    Statistical visualizations
Seaborn	        Exploratory visualizations
SQL	            Business queries and aggregations
Power BI	    Interactive dashboards and reporting
GitHub	        Version control and project presentation

## Statistical Methods Used
### Method	                  Purpose
Descriptive Statistics	   Understand distributions and central tendency
IQR Outlier Detection	   Identify unusual observations
Pearson Correlation	       Measure linear association
Spearman Correlation	   Measure monotonic association
One-Way ANOVA	           Test differences across discount groups
Welch's ANOVA	           Robust test when equal variance is questionable
Tukey HSD	               Identify specific group differences
Kruskal-Wallis	           Non-parametric validation
Eta Squared	               Measure effect size

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

## Power BI Dashboard

### Main Dashboard
<img width="1136" height="650" alt="image" src="https://github.com/user-attachments/assets/fb0f7dbd-33e5-442a-8e7a-e298b52a69fe" />

The Power BI solution converts the analytical results into interactive business dashboards.

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

## Project Structure

```text
retail-profit-leakage-analysis/
│
├── Data/
│   ├── Processed/
│   └── External/
│
├── Python/
│   ├── 01_Data_Cleaning.py
│   ├── 02_EDA.py
│   ├── 03_Feature_Engineering.py
│   ├── 04_Final_Data_Integration.py
│   └── 05_Statistical_Analysis.ipynb
│
├── SQL/
│   └── SQL_Analysis.sql
│
├── PowerBI/
│   └── Retail_Profit_Leakage_Dashboard.pbix
│
├── Dashboard_Screenshots/
│
├── README.md
└── LICENSE
```
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

## Conclusion

This project demonstrates how retail transaction data can be transformed into actionable profitability intelligence.

The analysis identifies a strong negative association between discounting and profit margin, statistically significant differences in profitability across discount bands, and a substantial concentration of loss-making transactions among high-discount orders.

The final solution combines:

**Python + SQL + Statistics + Power BI**

to move from:

**Raw Data → Analysis → Statistical Validation → Visualization → Business Decision**

---

## Author

**Sharvari Muley**

Data Analytics | Business Intelligence | Python | SQL | Power BI | Statistics

---

## Copyright & Usage

© 2026 Sharvari Muley. All rights reserved.

This project is published for portfolio, educational, and evaluation purposes.

No permission is granted to copy, reproduce, modify, redistribute, or present this project or substantial portions of its code, analysis, documentation, or visualizations as another person's work without prior written permission.
