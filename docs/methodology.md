# Methodology and implementation notes

This note documents `notebooks/demand_forecasting.ipynb` as it is implemented. It is not a claim that the workflow has been independently validated on the underlying business data.

## Input and panel construction

The notebook reads `historical_data.csv` from the repository root. It uses `product_id`, `category`, `hcode`, `date`, `sold`, `price`, and `is_promotion`. Sales are grouped by product and date; the product-date Cartesian panel is filled with zero for missing sales observations. Product category is attached from the observed product-category mapping. Price and `hcode` are forward-filled within product; missing promotion values become zero.

This panel construction assumes an absent product-date observation means zero sales. It does not distinguish true zero demand from stockouts, delisting, or incomplete reporting.

## Features and target

Features are calculated within each product after sorting by date:

- Sales lags at 1, 7, 14, 28, 56, and 365 days.
- Trailing means at 7, 14, 30, and 60 days; medians at 7, 30, and 60 days; sums at 7, 14, 30, and 60 days.
- Seven-day sales standard deviation and maximum; nonzero-sales counts over 7 and 30 days.
- Recency, previous nonzero sale quantity, and a historical median inter-sale gap feature stored as `lead_time`.
- Price, promotion, month, and day of week.
- Product/category/code categoricals in the global model; product/code categoricals in the category route.

Rolling features are based on a one-row-shifted sales series, so the current day's sales are not included in those trailing statistics. The `future_7` target sums the next seven daily observations, *t+1* through *t+7*. The field named `lead_time` is computed from historical gaps between sales events. It is not a supplier delivery lead-time observation.

## Chronological split and evaluation

The split date is the 80th percentile of prepared row dates. Training origins stop seven calendar days before that date, and test origins are later than the split date. This leaves a temporal gap intended to prevent overlapping seven-day target windows at the boundary. The category-model selection stage uses an earlier chronological validation window, separated from its validation origins by the same seven-day adjustment.

The simple baseline is trailing 30-day mean daily sales multiplied by seven. Evaluation includes MAE, RMSE, and R² at category, product, and overall test levels; comparisons with the baseline use the same held-out rows. R² is not defined for constant-target slices. Metric values are data-dependent and are not included in this repository.

## Model routing

- **Global model:** XGBoost regressor with histogram tree method and native categorical features; configured with 100 estimators, depth 4, learning rate 0.05, subsampling 0.8, and column sampling 0.8.
- **Sparse category fallback:** categories below 100 units of total training-period sales use the global model.
- **Category route:** other categories use CatBoost. In validation, product-level RMSE selects among the 30-day baseline, raw-target CatBoost, and `log1p`-target CatBoost. The selected learned model is refit on the category's full training data. Insufficient validation data falls back to baseline; constant training targets use a constant prediction.
- Predictions are clipped to nonnegative values. Model settings and routing thresholds are prototype choices, not a tuned or universally optimal policy.

## Preliminary replenishment

The latest date's seven-day forecast is combined with half of the standard deviation of the preceding seven daily sales values. The result is clipped at zero and rounded upward. The calculation does not subtract stock on hand or inbound orders, and it is not linked to supplier lead time, service level, pack size, minimum order quantity, or shelf life. Treat it as a preliminary, unit-based decision-support quantity only.

## Reproducibility and data boundaries

Install the packages in `requirements.txt`, place an authorized input file at the documented relative path, select the notebook kernel, and execute cells in order. The notebook writes recommendation and product-score CSV files locally; repository ignore rules cover CSV outputs. The repository does not include the source sales dataset, so the full training/evaluation run and numerical metrics cannot be reproduced from this checkout alone.
