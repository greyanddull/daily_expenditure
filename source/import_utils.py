import csv
import os

def import_transactions_from_folder(folder_path):
    combined_data = {"entries": []}

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            is_credit_card = filename.upper().startswith("CC")

            try:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    sample = f.read(1024)
                    f.seek(0)
                    delimiter = '\t' if '\t' in sample else ','
                    reader = csv.DictReader(f, delimiter=delimiter)

                    for row in reader:
                        if "Value" in row and row["Value"].strip():
                            try:
                                value = float(row["Value"].replace(',', '').replace('£', '').strip())
                                if is_credit_card:
                                    value *= -1
                                row["Value"] = str(value)
                            except ValueError:
                                print(f"Warning: could not convert Value in file {filename}: {row['Value']}")

                        combined_data["entries"].append(row)

            except Exception as e:
                print(f"Failed to process {filename}: {e}")

    return combined_data

def filter_transactions(data_dict, value1, operator, value2=None, mode="keep", verbose=False):
    filtered = {"entries": []}

    # Supported ops
    ops = {
        "==": lambda v: v == value1,
        "lt": lambda v: v < value1,
        "gt": lambda v: v > value1,
        "between": lambda v: value1 <= v <= value2 if value2 is not None else False
    }

    if operator not in ops:
        raise ValueError(f"Unsupported operator: {operator}. Use '==', 'lt', 'gt', or 'between'.")

    invert = (mode == "remove")

    for entry in data_dict["entries"]:
        try:
            value = float(entry["Value"].replace(',', '').replace('£', '').strip())
            match = ops[operator](value)

            should_include = (match and not invert) or (not match and invert)

            if should_include:
                filtered["entries"].append(entry)
                if verbose and mode == "keep":
                    print(f"[KEPT] {entry['Date']} | {entry['Description']} | Value: {entry['Value']}")
                elif verbose and mode == "remove":
                    print(f"[REMOVED] {entry['Date']} | {entry['Description']} | Value: {entry['Value']}")
            elif verbose and mode == "remove":
                print(f"[REMOVED] {entry['Date']} | {entry['Description']} | Value: {entry['Value']}")
            elif verbose and mode == "keep":
                print(f"[KEPT] {entry['Date']} | {entry['Description']} | Value: {entry['Value']}")

        except (ValueError, KeyError) as e:
            print(f"Skipping entry: {entry} (error: {e})")

    return filtered


def filter_transactions_by_description(data_dict, keyword, mode="keep"):
    filtered = {"entries": []}
    keyword_lower = keyword.lower()
    invert = (mode == "remove")

    for entry in data_dict["entries"]:
        try:
            description = entry["Description"].lower()
            match = keyword_lower in description

            if (match and not invert) or (not match and invert):
                filtered["entries"].append(entry)

        except KeyError as e:
            print(f"Skipping entry due to missing 'Description': {entry}")

    return filtered

from datetime import datetime

def filter_transactions_by_date(data_dict, date1, date2=None, mode="keep"):
    filtered = {"entries": []}
    invert = (mode == "remove")

    # Ensure date1 and date2 are datetime.date objects
    try:
        date1_obj = datetime.strptime(date1, "%d %b %Y").date()
        date2_obj = datetime.strptime(date2, "%d %b %Y").date() if date2 else date1_obj
    except ValueError as e:
        raise ValueError(f"Date format should be 'DD Mon YYYY' (e.g., '01 Jan 2025') - {e}")

    for entry in data_dict["entries"]:
        try:
            entry_date = datetime.strptime(entry["Date"].strip(), "%d %b %Y").date()
            in_range = date1_obj <= entry_date <= date2_obj

            if (in_range and not invert) or (not in_range and invert):
                filtered["entries"].append(entry)
        except (ValueError, KeyError) as e:
            print(f"Skipping entry due to date parsing error: {e} | Entry: {entry}")

    return filtered

