import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path
from datetime import datetime

# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from analysis.maximum_drawdown import calculate_maximum_drawdown
from config import PROCESSED_DATA_DIR, FIGURES_DIR

def plot_maximum_drawdown_bar_chart(START, END):
    """
    Calculate maximum drawdown and plot a bar chart of the results.

    Args:
        START (int): Start year for filtering the data.
        END (int): End year for filtering the data.
    """
    # Calculate maximum drawdown results
    mdd_results = calculate_maximum_drawdown(START, END)

    if not mdd_results:
        print("No maximum drawdown data available to plot.")
        return

    # Convert results to a DataFrame
    df = pd.DataFrame(list(mdd_results.items()), columns=["Currency", "Maximum Drawdown (%)"])

    # Extract currencies and drawdown values
    currencies = df["Currency"]
    mdd_values = df["Maximum Drawdown (%)"]

    # Find the most extreme drawdown
    min_value = mdd_values.min()
    colors = ["red" if val == min_value else "skyblue" for val in mdd_values]

    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(currencies, mdd_values, color=colors, edgecolor="black")

    # Add labels and title
    plt.title("Maximum Drawdown of Exchange Rates", fontsize=16)
    plt.xlabel("Currency", fontsize=12)
    plt.ylabel("Maximum Drawdown (%)", fontsize=12)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")

    # Add grid for easier reading
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Example: Plot the maximum drawdown bar chart for the years 2000 to 2024
    plot_maximum_drawdown_bar_chart(2000, 2024)
