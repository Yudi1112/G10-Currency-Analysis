import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from scripts.value_at_risk import calculate_var
from config import PROCESSED_DATA_DIR, FIGURES_DIR

def plot_var_bar_chart(START, END, confidence_level=0.95):
    """
    Calculate VaR and plot a bar chart of the results.

    Args:
        START (int): Start year for analysis.
        END (int): End year for analysis.
        confidence_level (float): The confidence level for VaR calculation (default is 0.95).
    """
    var_results = calculate_var(START, END, confidence_level)

    if not var_results:
        print("No VaR data available to plot.")
        return

    # Convert results to a DataFrame
    df = pd.DataFrame(list(var_results.items()), columns=["Currency", "VaR (%)"])

    # Extract currencies and VaR values
    currencies = df["Currency"]
    var_values = df["VaR (%)"]

    # Highlight the currency with the highest risk (most negative VaR)
    min_value = var_values.min()  # The most negative value indicates the highest risk
    colors = ["red" if val == min_value else "skyblue" for val in var_values]

    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(currencies, var_values, color=colors, edgecolor="black")

    # Add labels and title
    plt.title(f"Value at Risk (VaR) at {confidence_level*100:.0f}% Confidence", fontsize=16)
    plt.xlabel("Currency", fontsize=12)
    plt.ylabel("VaR (%)", fontsize=12)

    # Rotate x-axis labels for readability
    plt.xticks(rotation=45, ha="right")

    # Add grid for better readability
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_var_bar_chart(2000, 2024, confidence_level=0.95)
