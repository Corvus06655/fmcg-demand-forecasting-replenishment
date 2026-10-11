# Inventory Demand Forecasting & Reorder Optimization

A time-series forecasting project that explores daily product demand and estimates short-term sales to support preliminary inventory replenishment decisions.

## Project Overview

This project compares baseline and machine-learning approaches for predicting product sales. It includes data preparation, feature engineering, model evaluation, and an initial reorder-quantity calculation.

> **Data note:** The source dataset is not included in this repository. Add it only if you have permission to share it publicly.

## Workflow

1. Prepare daily product-level sales data.
2. Create time-based and product-related features.
3. Establish a moving-average baseline.
4. Train and compare Linear Regression, Random Forest, and XGBoost models.
5. Evaluate predictions with MAE, RMSE, and R².
6. Explore a preliminary reorder estimate based on predicted demand and safety stock.

## Recorded Model Results

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Moving-average baseline | 18.297 | 152.535 | 0.230 |
| Linear Regression | 17.141 | 134.033 | 0.405 |
| Random Forest | 17.401 | 141.534 | 0.337 |
| XGBoost | 17.572 | 138.490 | 0.365 |

In this global comparison, Linear Regression had the lowest MAE and RMSE and the highest R² among the listed models. Results varied across categories, so performance should not be assumed to be equally strong for every product or category.

## Preliminary Reorder Logic

The notebook explores a simple estimate based on predicted 7-day demand plus safety stock, rounded up and clipped at zero.

This is **not a production-ready replenishment policy**. The current logic does not fully account for current on-hand inventory, purchase orders already in transit, supplier lead times, target service levels, pack-size constraints, or stockout-related demand censoring.

## Data Fields

The working dataset uses fields such as:

- `product_id`
- `category`
- `hcode`
- `sold`
- `date`
- `is_promotion`
- `price`

## Tech Stack

- Python
- Pandas and NumPy
- Matplotlib
- scikit-learn
- XGBoost
- Jupyter Notebook

## Running the Project

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies listed in `requirements.txt`.
4. Place the authorized source dataset at the location expected by the notebook.
5. Open and run the notebook from top to bottom.

The notebook path and dataset path may need to be adjusted to match the files included in your local checkout.

## Limitations

- Reported metrics are from the notebook's recorded evaluation; reproduce them on the authorized dataset before relying on them.
- Category-level performance is mixed.
- The reorder calculation is a starting point for analysis, not a validated inventory optimization system.
- No business savings, stockout reduction, or operational impact is claimed without measured evidence.

## Future Improvements

- Use time-aware validation and backtesting.
- Compare performance by product and category.
- Incorporate lead time and inventory-position data into replenishment calculations.
- Tune safety stock using explicit service-level assumptions.
- Add reproducible configuration and evaluation reports.
