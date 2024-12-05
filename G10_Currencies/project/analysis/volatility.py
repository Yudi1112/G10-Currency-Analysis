import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np

# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from loguru import logger
from config import PROCESSED_DATA_DIR


def calculate_volatility(START, END):
    """
    Analyze the standard deviation of exchange rates (volatility) for each currency.
    """

    # List all processed CSV files
    csv_files = list(PROCESSED_DATA_DIR.glob("*.csv"))
    if not csv_files:
        logger.error("No processed datasets found.")
        return

    # Initialize a dictionary to store volatility results
    volatility_results = {}

    # Process each dataset
    for csv_file in csv_files:
        try:
            # Load the dataset
            df = pd.read_csv(csv_file, parse_dates=["Date"])

            # Convert START_YEAR and END_YEAR to datetime objects
            START_YEAR = datetime(START, 1, 1)
            END_YEAR = datetime(END, 12, 31)

            # Filter the dataset to start from the specified year
            df = df[(df["Date"] >= START_YEAR) & (df["Date"] <= END_YEAR)]

            # Calculate monthly log returns
            df["Log Return"] = np.log(df["Price"] / df["Price"].shift(1))

            # Calculate the standard deviation of log returns (volatility)
            monthly_std_dev = df["Log Return"].std()

            # Annualize the standard deviation
            annualized_std_dev = monthly_std_dev * np.sqrt(12)

            volatility_results[csv_file.stem] = annualized_std_dev

        except Exception as e:
            logger.error(f"Error processing file {csv_file}: {e}")

    # Display or save the results
    if volatility_results:
        print("\nVolatility Results (Standard Deviation of Exchange Rates):")
        for currency, std_dev in volatility_results.items():
            print(f"{currency}: {std_dev:.6f}")
    return volatility_results

if __name__ == "__main__":
    calculate_volatility(2000, 2024)
