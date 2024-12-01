import sys
import pandas as pd
from pathlib import Path

# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from loguru import logger
from config import PROCESSED_DATA_DIR
from variables import START_DATE 

def calculate_depreciation():
    """
    Analyze which currency depreciated the most vs. CHF over the time period.
    """
    logger.info("Starting depreciation analysis...")

    # Ensure the processed data directory exists
    if not PROCESSED_DATA_DIR.exists():
        logger.error(f"Processed data directory does not exist: {PROCESSED_DATA_DIR}")
        return

    # List all processed CSV files
    csv_files = list(PROCESSED_DATA_DIR.glob("*.csv"))
    if not csv_files:
        logger.error("No processed datasets found.")
        return

    # Initialize a dictionary to store depreciation values
    depreciation_results = {}

    # Process each dataset
    for csv_file in csv_files:
        try:
            logger.info(f"Processing file: {csv_file}")
            # Load the dataset
            df = pd.read_csv(csv_file, parse_dates=["Date"])

            # Filter the dataset to start from the specified START_DATE
            df = df[df["Date"] >= START_DATE]

            if df.empty:
                logger.warning(f"No data available after START_DATE for {csv_file.stem}. Skipping.")
                continue

            # Extract start and end exchange rates
            start_rate = df.iloc[-1]["Price"]
            end_rate = df.iloc[0]["Price"]

            # Calculate percentage depreciation
            depreciation = ((start_rate - end_rate) / start_rate) * 100
            depreciation_results[csv_file.stem] = depreciation

            logger.info(f"{csv_file.stem}: Start Rate = {start_rate}, End Rate = {end_rate}, Depreciation = {depreciation:.2f}%")

        except Exception as e:
            logger.error(f"Error processing file {csv_file}: {e}")

    # Identify the currency with the highest depreciation
    if depreciation_results:
        max_depreciation_currency = min(depreciation_results, key=depreciation_results.get)
        logger.success(f"Currency with the highest depreciation: {max_depreciation_currency} ({depreciation_results[max_depreciation_currency]:.2f}%)")

        # Print all depreciation results
        print("\nDepreciation Results:")
        for currency, dep in depreciation_results.items():
            print(f"{currency}: {dep:.2f}%")
    else:
        logger.warning("No valid depreciation data found.")


if __name__ == "__main__":
    calculate_depreciation()