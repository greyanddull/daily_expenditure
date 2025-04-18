from datetime import datetime
from collections import defaultdict

def calculate_cumulative_balance_by_date(data_dict):
    # Parse and collect (date, value)
    entries = []
    for entry in data_dict["entries"]:
        try:
            date_obj = datetime.strptime(entry["Date"].strip(), "%d %b %Y").date()
            value = float(entry["Value"].replace(',', '').replace('£', '').strip())
            entries.append((date_obj, value))
        except (ValueError, KeyError) as e:
            print(f"Skipping entry due to error: {e}")

    # Sort by date
    entries.sort(key=lambda x: x[0])

    # Sum transactions per date
    daily_net = defaultdict(float)
    for date, value in entries:
        daily_net[date] += value

    # Compute cumulative balance
    sorted_dates = sorted(daily_net)
    balances = []
    current_balance = 0
    for date in sorted_dates:
        current_balance += daily_net[date]
        balances.append(current_balance)

    return sorted_dates, balances
