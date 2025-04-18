import argparse
from import_utils import *
from plotting_utils import *
from calc_utils import *
import yaml
import os

def main():
    parser = argparse.ArgumentParser(description="Import all CSV bank transaction files from a folder into a dictionary.")
    parser.add_argument("folder", help="Path to the folder containing CSV files")
    parser.add_argument("filter", help="Name of the *.yaml containing the account filters")
    args = parser.parse_args()

    # Import data
    data = import_transactions_from_folder(args.folder)

    # Import the filter file
    with open(f"filters/{args.filter}.yaml") as f:
        filters = yaml.safe_load(f)

    for rule in filters.get("remove_if_amount", []):
        for op, val in rule.items():
            data = filter_transactions(data, val, op, mode="remove")

    for desc in filters.get("remove_if_description", []):
        data = filter_transactions_by_description(data, desc, mode="remove")
    
    # Remove large expenses
    data = filter_transactions_by_description(data, "Flynn", mode="remove")
    data = filter_transactions_by_description(data, "Virgin", mode="remove")

    # For demonstration: print how many rows were imported
    dates, balances = calculate_cumulative_balance_by_date(data)
    plot_cumulative_balance_with_trendline(dates, balances)


if __name__ == "__main__":
    main()