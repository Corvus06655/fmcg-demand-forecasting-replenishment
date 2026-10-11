# FMCG Demand Forecasting & Inventory Replenishment

A notebook-based machine-learning workflow that uses historical FMCG sales to estimate each product's total demand over the next seven days and produce a **preliminary replenishment quantity**. It combines lagged and rolling time-series features, chronological validation, XGBoost/CatBoost routes, and a simple safety-stock heuristic.

![Python](https://img.shields.io/badge/Python-3-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/data-pandas-150458?logo=pandas&logoColor=white)
![Models](https://img.shields.io/badge/models-XGBoost%20%7C%20CatBoost-2563EB)
![Jupyter](https://img.shields.io/badge/notebooks-Jupyter-F37626?logo=jupyter&logoColor=white)
![Status](https://img.shields.io/badge/status-research%20prototype-0F766E)

**Start here:** [open the forecasting notebook](notebooks/demand_forecasting.ipynb) · [view the workflow](assets/forecasting-workflow.svg) · [read the methodology](docs/methodology.md)

> **Scope:** This is an analytical prototype, not a deployed application or an operational purchasing system. No raw sales dataset or reproducible evaluation results are included in this repository.

## Project overview

FMCG demand can be intermittent and vary across products. This project demonstrates a reproducible way to turn an approved historical sales extract into product-level seven-day demand estimates, compare time-aware model routes, and create a preliminary replenishment file for human review.

### Objectives and intended users

- Explore product-level sales patterns and data quality.
- Compare a simple demand baseline with global and category-level machine-learning routes on a chronological holdout.
- Generate a forecast and a transparent, provisional replenishment quantity.
- Support analysts, data-science learners, and inventory planners evaluating a prototype—not automate purchase orders.

### What the notebook implements

- Daily product-level demand preparation; unobserved product-date combinations are filled with zero.
- Lag, rolling, recency, recent-sales, calendar, price, promotion, and categorical features.
- A seven-day-ahead summed-sales target.
- A chronological train/validation/test approach with a seven-day separation around target windows.
- A global XGBoost model, category-level CatBoost and log-target CatBoost routes, plus baseline/constant fallbacks.
- MAE, RMSE, and R² evaluation against a 30-day-mean baseline.
- A preliminary replenishment calculation using the forecast and a trailing-sales-variability proxy.

## Workflow

![Verified project workflow from historical sales to preliminary replenishment](assets/forecasting-workflow.svg)

The diagram describes the code in the notebook. There is no production service or live dashboard behind the illustrative [dashboard concept](assets/replenishment-dashboard-mockup.svg); its chart is explicitly illustrative and contains no project results.

## Repository map

```text
fmcg-demand-forecasting-replenishment/
├── .github/workflows/validate-notebook.yml
├── assets/
│   ├── forecasting-workflow.svg
│   └── replenishment-dashboard-mockup.svg
├── docs/
│   └── methodology.md
├── notebooks/
│   └── demand_forecasting.ipynb
├── tests/
│   └── test_notebook_contract.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Data contract and feature definitions

The notebook expects a locally available `historical_data.csv` in the repository root. It is intentionally not distributed. Required columns, as read by the notebook:

| Column | Use |
|---|---|
| `product_id` | Product-level grouping and categorical model input |
| `category` | Category summaries and category-based routing |
| `hcode` | Additional categorical product/commodity-code feature |
| `date` | Observation date; converted to a datetime |
| `sold` | Units sold; aggregated to daily product demand |
| `price` | Price feature; last observed value is carried forward within product |
| `is_promotion` | Promotion indicator; missing values are filled with zero |

The notebook derives daily lags (1, 7, 14, 28, 56, 365 days), rolling means/medians/sums, recent variability and nonzero-sales counts, recency, last observed sale quantity, and calendar features. It also uses product, category, and `hcode` categoricals in the model routes.

**Data handling:** supply only data you are authorized to use. Do not commit raw or identifiable sales data, notebook outputs containing records, locally generated recommendation files, credentials, or private exports. `.gitignore` excludes CSVs and common local/generated artifacts; ignored files already committed to Git remain in history.

## Forecasting and model selection

1. **Daily panel and features:** sales are aggregated by product and date. Missing product-date combinations are represented as zero sales. Price is forward-filled within product; a missing promotion flag is set to zero.
2. **Target:** for each product and date *t*, `future_7` is the sum of daily sales on *t+1* through *t+7*. This is a seven-day total, not a daily forecast trajectory.
3. **Baseline:** the trailing 30-day mean daily sales multiplied by seven, clipped to a nonnegative value.
4. **Chronological holdout:** a date split is derived from the 80th percentile of the prepared rows. The model-training cutoff is shifted back seven days, and test origins are strictly after the split date. This is intended to keep seven-day label windows from crossing the train/test boundary; it is not a random split.
5. **Global route:** an XGBoost regressor with native categorical handling is fitted on training rows. Categories with less than 100 units sold in the training-period aggregate are routed to this global model.
6. **Category route:** other categories use CatBoost. In an earlier chronological validation window, the notebook compares a 30-day baseline, CatBoost on the original target, and CatBoost on `log1p` demand separately by product using RMSE. It refits required category models on the full training period. If the validation sample is insufficient, the baseline is used; a constant-target category uses a constant fallback.
7. **Predictions:** negative forecasts are clipped to zero. The notebook also scores category and product test slices; R² is undefined for a slice with no target variation and is left missing.

The time split and gap reduce target-window overlap, but they do not eliminate every possible source of bias. Review the notebook and data-specific assumptions before relying on reported metrics.

## Evaluation

The notebook calculates **MAE, RMSE, and R²** for held-out predictions and compares errors with the 30-day baseline. Results depend on the supplied dataset and are produced by running the notebook. Numeric results are not published here: the source data is intentionally excluded, and data-derived metrics may disclose business information. Do not infer model performance from the illustrative dashboard.

- **MAE:** average absolute error in seven-day unit totals.
- **RMSE:** square-root mean squared error, also in units, with larger errors weighted more heavily.
- **R²:** coefficient of determination; can be undefined when an evaluated target slice is constant.

## Preliminary replenishment logic

For the latest date and each product, the notebook computes:

```text
safety-stock proxy = 0.5 × trailing 7-day standard deviation of daily sales
preliminary quantity = ceil(max(7-day demand forecast + safety-stock proxy, 0))
```

This is a heuristic in **units**. It is not calibrated to a target service level and does not subtract on-hand inventory or incoming orders. The notebook variable/output label `recommended_reorder_quantity` should therefore be interpreted as a provisional demand-plus-buffer quantity—not a validated purchase order quantity.

The historical gap between sales events is a sales-pattern feature only. It is **not supplier lead time**. No supplier lead-time data is present in the notebook.

## Install and run

Use a recent Python 3 environment. From a terminal:

```bash
git clone https://github.com/Corvus06655/fmcg-demand-forecasting-replenishment.git
cd fmcg-demand-forecasting-replenishment
python -m venv .venv
```

Activate the virtual environment, then install dependencies and register a notebook kernel:

**macOS/Linux**
```bash
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install --user --name fmcg-demand-forecasting --display-name "Python (FMCG forecasting)"
jupyter lab
```

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install --user --name fmcg-demand-forecasting --display-name "Python (FMCG forecasting)"
jupyter lab
```

Put your authorized `historical_data.csv` in the repository root, open `notebooks/demand_forecasting.ipynb`, select the registered kernel, and run the cells in order. The current notebook reads that relative path directly. It writes `latest_reorder_recommendations.csv` and `product_model_scores.csv` locally; both are ignored by Git. Keep notebook outputs cleared before committing.

## Limitations and assumptions

- A missing product-date row is treated as zero sales; this may conflate no demand with stockouts, assortment changes, or incomplete data.
- The model uses historical price and promotion observations, not a known future price/promotion plan for the forecast horizon.
- The sales-gap feature is not supplier lead time. No current inventory, on-order quantity, supplier constraints, pack sizes, shelf life, or service-level target is modeled.
- The replenishment calculation is preliminary and should be reviewed by a planner.
- The 30-day baseline and model routes are prototype choices. No claims are made about cost savings, service levels, stockout reduction, or production deployment.
- The full model run cannot be reproduced from this repository alone; an authorized local source dataset is required.

## Future improvements

- Validate the feature and panel assumptions against an approved, representative sample.
- Add stockout/censored-demand handling and explicit future-known calendar/promotion inputs.
- Incorporate on-hand and inbound stock, validated supplier lead times, service-level policy, pack sizes, minimum order quantities, and shelf-life constraints.
- Add rolling-origin backtesting, uncertainty intervals, segment-level error analysis, and model monitoring.
- Extract stable notebook logic into tested Python modules if a reusable library or application becomes a project goal.

## Conclusion

This repository is a transparent, data-dependent demonstration of seven-day FMCG demand forecasting and preliminary replenishment logic. Its intended value is as an explainable prototype and starting point for evaluation—not as a claim of validated business impact or a production-ready inventory optimizer.
