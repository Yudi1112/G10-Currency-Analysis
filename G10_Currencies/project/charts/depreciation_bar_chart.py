import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path
from datetime import datetime


# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from analysis.depreciation import calculate_depreciation  
from config import PROCESSED_DATA_DIR, FIGURES_DIR



def plot_depreciation_bar_chart(START, END):
    """
    Calculate depreciation and plot a histogram of the results.
    """
    # Calculate depreciation
    depreciation_results = calculate_depreciation(START, END)

    if not depreciation_results:
        print("No depreciation data available to plot.")
        return

    # Convert results to a DataFrame
    df = pd.DataFrame(list(depreciation_results.items()), columns=["Currency", "Depreciation (%)"])

    # Extract currencies and depreciation values
    currencies = df["Currency"]
    depreciation_values = df["Depreciation (%)"]

    # Find the most negative value
    min_value = depreciation_values.min()
    colors = ["red" if val == min_value else "skyblue" for val in depreciation_values]

    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(currencies, depreciation_values, color=colors, edgecolor="black")

    # Add labels and title
    plt.title("Depreciation of Currencies vs CHF", fontsize=16)
    plt.xlabel("Currency", fontsize=12)
    plt.ylabel("Depreciation (%)", fontsize=12)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")

    # Add grid for easier reading
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_depreciation_bar_chart(2000, 2024)
