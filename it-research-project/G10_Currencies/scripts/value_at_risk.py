import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from config import PROCESSED_DATA_DIR

def calculate_var(START, END, confidence_level=0.95):
    """
    Calculate the Value at Risk (VaR) for each currency using the historical method.

    Args:
        START (int): Start year for analysis.
        END (int): End year for analysis.
        confidence_level (float): The confidence level for VaR calculation (default is 0.95).
    Returns:
        dict: A dictionary with currencies as keys and their VaR as values.
    """
    # List all processed CSV files
    csv_files = list(PROCESSED_DATA_DIR.glob("*.csv"))
    if not csv_files:
        logger.error("No processed datasets found.")
        return

    var_results = {}

    # Process each dataset
    for csv_file in csv_files:
        try:
            # Load the dataset
            df = pd.read_csv(csv_file, parse_dates=["Date"])

            # Convert START and END years to datetime objects
            START_YEAR = datetime(START, 1, 1)
            END_YEAR = datetime(END, 12, 31)

            # Filter the dataset by date range
            df = df[(df["Date"] >= START_YEAR) & (df["Date"] <= END_YEAR)]

            # Calculate daily returns
            df["Return"] = df["Price"].pct_change()
            returns = df["Return"].dropna()

            # Calculate VaR
            var_percentile = (1 - confidence_level) * 100
            var = np.percentile(returns, var_percentile)
            var_results[csv_file.stem] = var * 100  # Convert to percentage

        except Exception as e:
            logger.error(f"Error processing file {csv_file}: {e}")

    # Display results
    if var_results:
        print("\nValue at Risk (VaR) Results:")
        for currency, var in var_results.items():
            print(f"{currency}: {var:.2f}%")
    return var_results

if __name__ == "__main__":
    calculate_var(2000, 2024)
