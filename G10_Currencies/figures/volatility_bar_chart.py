import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path
from datetime import datetime


# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from scripts.volatility import calculate_volatility
from config import PROCESSED_DATA_DIR, FIGURES_DIR



def plot_volatility_bar_chart(START, END):
    """
    Calculate volatility and plot a histogram of the results.
    """
    volatility_results = calculate_volatility(START, END)

    if not volatility_results:
        print("No depreciation data available to plot.")
        return

    # Convert results to a DataFrame
    df = pd.DataFrame(list(volatility_results.items()), columns=["Currency", "Standard Deviation"])

    # Extract currencies and depreciation values
    currencies = df["Currency"]
    std_dev_values = df["Standard Deviation"]

    # Find the most negative value
    max_value = std_dev_values.max()
    colors = ["red" if val == max_value else "skyblue" for val in std_dev_values]

 # Plot the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(currencies, std_dev_values, color=colors, edgecolor="black")

    # Add labels and title
    plt.title("Volatility of Exchange Rates", fontsize=16)
    plt.xlabel("Currency", fontsize=12)
    plt.ylabel("Standard Deviation", fontsize=12)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")

    # Add grid for easier reading
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_volatility_bar_chart(2000, 2024)
