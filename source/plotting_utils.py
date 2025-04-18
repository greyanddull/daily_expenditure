import matplotlib.pyplot as plt
import numpy as np

def plot_cumulative_balance_with_trendline(dates, balances):
    # Convert dates to numerical format for regression (days since first date)
    days_since_start = np.array([(date - dates[0]).days for date in dates])
    balance_array = np.array(balances)

    # Linear regression
    slope, intercept = np.polyfit(days_since_start, balance_array, 1)
    trendline = slope * days_since_start + intercept

    # Print slope
    print(f"Linear regression slope: £{slope:.2f} per day")

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(dates, balances, marker='o', label='Cumulative Balance')
    plt.plot(dates, trendline, linestyle='--', label=f'Trend Line of £{slope:.2f} per day')
    plt.title("Reconstructed Cumulative Balance with Trend")
    plt.xlabel("Date")
    plt.ylabel("Balance")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def print_account_preview(data_dict, account_number, n=5):
    print(f"\nPreviewing first {n} transactions for account: {account_number}")
    print("-" * 80)
    print(f"{'Description':50} {'Value':>10} {'Balance':>10}")
    print("-" * 80)

    count = 0
    for entry in data_dict["entries"]:
        if entry.get("Account Number") == account_number:
            desc = entry.get("Description", "")[:50]
            value = entry.get("Value", "")
            balance = entry.get("Balance", "")
            print(f"{desc:50} {value:>10} {balance:>10}")
            count += 1
            if count >= n:
                break

    if count == 0:
        print(f"No entries found for account: {account_number}")
    print("-" * 80)
