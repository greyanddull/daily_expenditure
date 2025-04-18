# 📊 Daily Expenditure Estimator

This program estimates your daily expenditure based on your bank account transaction history.
It works best if you primarily use a small number of accounts for daily spending, bills, and taxes.

The program:
- Loads transaction history from one or more CSV spreadsheets
- Filters out income, large outflows, and internal transfers (based on a YAML filter file)
- Computes the cumulative balance over time
- Fits a linear trend to estimate average daily expenditure from the downward slope

---

## 🚀 Getting Started

> ⚠️ This program is designed for use with your own real financial data, so no pre-built examples are included.

### 📁 Prepare Account History

1. Download CSV transaction history from all relevant bank accounts
2. Format each CSV file to match the structure of the example in `example_accounts/`
3. Save all CSVs into a single folder (e.g., `my_accounts/`)

### 🧹 Define Filters

Filters help exclude transactions not relevant to daily expenditure.

1. Copy or edit a filter file in the `filters/` folder (YAML format)
2. You can filter:
   - a. Income (`amount > 0`)
   - b. Large outflows (`amount < -5000`)
   - c. Transfers between personal accounts  
      → These are matched by keywords in the `"Description"` column of your CSVs

---

## ▶️ Running the Program

Once your CSV files and filter config are ready, remain in the program's root directory and run:

```bash
python3 source/main_cashflow.py name_of_accounts_folder name_of_filter_yaml
```

Example:
```bash
python3 source/main_cashflow.py my_accounts conservative_filters.yaml
```

The program will generate a plot showing your cumulative balance without income and the estimated daily expenditure trend.


