import sys
import pandas as pd
from pathlib import Path

# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from loguru import logger
from config import PROCESSED_DATA_DIR


def calculate_volatility():
    """
    Analyze the standard deviation of exchange rates (volatility) for each currency.
    """
    logger.info("Starting volatility analysis...")

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
            logger.info(f"Processing file: {csv_file}")
            # Load the dataset
            df = pd.read_csv(csv_file, parse_dates=["Date"])

            # Calculate the standard deviation of the Price column
            std_dev = df["Price"].std()
            volatility_results[csv_file.stem] = std_dev

            logger.info(f"{csv_file.stem}: Standard Deviation = {std_dev:.6f}")
        except Exception as e:
            logger.error(f"Error processing file {csv_file}: {e}")

    # Display or save the results
    if volatility_results:
        print("\nVolatility Results (Standard Deviation of Exchange Rates):")
        for currency, std_dev in volatility_results.items():
            print(f"{currency}: {std_dev:.6f}")
"""
        # Optionally save results to a CSV file
        results_df = pd.DataFrame(list(volatility_results.items()), columns=["Currency", "Standard Deviation"])
        results_path = PROCESSED_DATA_DIR / "volatility_results.csv"
        results_df.to_csv(results_path, index=False)
        logger.success(f"Volatility results saved to: {results_path}")
    else:
        logger.warning("No valid volatility data found.")
"""

if __name__ == "__main__":
    calculate_volatility()
