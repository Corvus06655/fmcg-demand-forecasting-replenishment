# Inventory Demand Forecasting & Reorder Optimization

A Python time-series forecasting project that compares demand-prediction approaches and explores how short-term forecasts can inform preliminary inventory replenishment decisions.

## Project Overview

The notebook analyzes daily product sales, prepares time-based features, compares a moving-average baseline with machine-learning models, and calculates an initial reorder estimate from predicted 7-day demand and safety stock.

**Important:** This is an analytical prototype, not a production-ready inventory planning system.

## Repository Structure

```text
inventory-demand-forecasting/
├── notebooks/
│   └── demand_forecasting.ipynb
├── .gitignore
├── requirements.txt
└── README.md
```

## Workflow

1. Load and validate the source sales data.
2. Clean fields and prepare date-based features.
3. Explore sales distributions and product/category patterns.
4. Build a moving-average baseline.
5. Train and compare Linear Regression, Random Forest, and XGBoost.
6. Evaluate model predictions with MAE, RMSE, and R².
7. Generate a preliminary reorder-quantity estimate.

## Recorded Model Results

The following metrics are recorded in the project notebook:

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Moving-average baseline | 18.297 | 152.535 | 0.230 |
| Linear Regression | 17.141 | 134.033 | 0.405 |
| Random Forest | 17.401 | 141.534 | 0.337 |
| XGBoost | 17.572 | 138.490 | 0.365 |

Among these global comparisons, Linear Regression has the lowest MAE and RMSE and the highest R². Performance varies across categories; the same accuracy should not be assumed for every product. Re-run the notebook on the authorized dataset to reproduce the results.

## Dataset

The notebook expects a source file named `historical_data.csv` in the repository root. **That file is intentionally not included** because the source data may be private or subject to company restrictions. Only add or publish it if you have explicit permission.

Expected columns:

| Column | Description |
|---|---|
| `product_id` | Product identifier |
| `category` | Product category |
| `hcode` | Product/commodity code |
| `sold` | Units sold |
| `date` | Sales date |
| `is_promotion` | Promotion indicator |
| `price` | Product price |

## Setup and Run

Requires Python 3.10+ recommended.

1. Clone the repository:

   ```bash
   git clone https://github.com/Corvus06655/inventory-demand-forecasting.git
   cd inventory-demand-forecasting
   ```

2. Create and activate a virtual environment (optional but recommended):

   **Windows**
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Place your authorized `historical_data.csv` file in the repository root.
5. Start Jupyter:

   ```bash
   jupyter lab
   ```

6. Open `notebooks/demand_forecasting.ipynb` and run the cells from top to bottom.

The notebook saves its preliminary output as `recommended_reorder_quantity.csv` in the working directory. Generated CSV files and raw data are excluded by `.gitignore`.

## Preliminary Reorder Logic and Limitations

The notebook explores a simple estimate based on predicted 7-day demand plus safety stock, rounded up and clipped at zero. This should be treated as a starting point only.

The current approach does not fully account for:

- Current on-hand stock or inventory already on order
- Supplier lead times and lead-time demand
- A statistically defined service level and safety-stock policy
- Supplier pack sizes, minimum order quantities, or shelf-life constraints
- Stockouts that may cause recorded sales to understate true demand

Category-level model performance is mixed. No business savings, stockout reduction, or operational impact is claimed without measured evidence.

## Tech Stack

- Python, Jupyter Notebook
- Pandas, NumPy
- Matplotlib
- scikit-learn
- XGBoost, CatBoost

## Potential Next Steps

- Add time-aware backtesting and compare forecasts against seasonal-naive baselines.
- Report metrics by product and category.
- Tune models using a strictly time-based validation strategy.
- Incorporate inventory position, lead time, and service-level assumptions into replenishment logic.
- Add reproducible configuration and a concise evaluation report.
