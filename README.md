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

The final analytical dataset contains:

- **51,290 records**
- **49 columns**

The dataset contains information related to:

- Sales
- Profit
- Discount
- Quantity
- Customers
- Products
- Categories
- Markets
- Countries
- Shipping
- Delivery
- Profit Margin
- Discount Bands
- Loss Status
- Economic indicators

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
