import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from config import PROCESSED_DATA_DIR, FIGURES_DIR
from ipywidgets import interact, Dropdown

# Function to load and plot data for a selected currency
def plot_currency_chart(currency):
    """
    Plot the exchange rate chart for the selected currency.
    """
    # Path to the currency file
    csv_file_path = PROCESSED_DATA_DIR / f"{currency}.csv"

    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)  
        
        # Clean and parse the Date column
        df["Date"] = df["Date"].str.strip()  # Remove any extra spaces
        df["Date"] = pd.to_datetime(df["Date"], format="%Y-%d-%m")  # Parse dates explicitly

        # Sort by Date
        df = df.sort_values("Date")

        # Plot Exchange Rates
        plt.figure(figsize=(12, 6))
        plt.plot(df["Date"], df["Price"], label="Closing Price", marker="o", linestyle="-", color="blue")
        plt.xlabel("Date")
        plt.ylabel("Exchange Rate")
        plt.title(f"{currency}")
        plt.grid()
        plt.legend()
        plt.show()

    except FileNotFoundError:
        print(f"No data found for currency: {currency}")


if __name__ == "__main__":
    plot_currency_chart("CHF_AUD Historical Data")
