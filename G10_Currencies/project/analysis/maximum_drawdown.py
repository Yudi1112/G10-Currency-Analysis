import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from loguru import logger
logger.remove()
logger.add(sys.stdout, level="WARNING")  # Zeigt nur WARNINGS und ERRORs an

from config import PROCESSED_DATA_DIR

def calculate_maximum_drawdown(START, END):
    """
    Calculate the maximum drawdown for each currency within a specified time period,
    using the reciprocal (1 / Price) of the original prices.

    Args:
        START (int): Start year for filtering the data.
        END (int): End year for filtering the data.

    Returns:
        dict: Dictionary of currencies and their respective maximum drawdown percentages.
    """

    # List all processed CSV files
    csv_files = list(PROCESSED_DATA_DIR.glob("*.csv"))
    if not csv_files:
        logger.error("No processed datasets found.")
        return

    # Initialize a dictionary to store maximum drawdown results
    mdd_results = {}

    # Process each dataset
    for csv_file in csv_files:
        try:
            logger.info(f"Processing file: {csv_file}")

            # Load the dataset
            df = pd.read_csv(csv_file, parse_dates=["Date"])

            # Convert START_YEAR and END_YEAR to datetime objects
            START_YEAR = datetime(START, 1, 1)
            END_YEAR = datetime(END, 12, 31)

            # Filter the dataset to include only rows within the specified date range
            df = df[(df["Date"] >= START_YEAR) & (df["Date"] <= END_YEAR)]

            # Ensure the dataset is sorted by date
            df = df.sort_values(by="Date")

            # Calculate the reciprocal (1 / Price) of the original prices
            df["Reciprocal Price"] = 1 / df["Price"]

            # Calculate the rolling maximum of reciprocal prices
            df["Rolling Max"] = df["Reciprocal Price"].cummax()

            # Calculate the drawdown as a percentage
            df["Drawdown"] = (df["Reciprocal Price"] - df["Rolling Max"]) / df["Rolling Max"] * 100

            # Find the maximum drawdown value
            max_drawdown = df["Drawdown"].min()

            # Store the maximum drawdown in the results dictionary
            mdd_results[csv_file.stem] = max_drawdown

        except Exception as e:
            logger.error(f"Error processing file {csv_file}: {e}")

    # Display or save the results
    if mdd_results:
        print("\nMaximum Drawdown (MDD) Results:")
        for currency, mdd in mdd_results.items():
            print(f"{currency}: {mdd:.2f}%")
    return mdd_results

if __name__ == "__main__":
    calculate_maximum_drawdown(2000, 2024)
