import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from loguru import logger
from config import PROCESSED_DATA_DIR


def calculate_historical_var(confidence_level=0.95):
    """
    Calculate the Value at Risk (VaR) for each currency using the historical method.
    
    Args:
        confidence_level (float): The confidence level for VaR calculation (default is 0.95).
    """
    logger.info("Starting Value at Risk (VaR) analysis...")

    # Ensure the processed data directory exists
    if not PROCESSED_DATA_DIR.exists():
        logger.error(f"Processed data directory does not exist: {PROCESSED_DATA_DIR}")
        return

    # List all processed CSV files
    csv_files = list(PROCESSED_DATA_DIR.glob("*.csv"))
    if not csv_files:
        logger.error("No processed datasets found.")
        return

    # Initialize a dictionary to store VaR results
    var_results = {}

    # Process each dataset
    for csv_file in csv_files:
        try:
            logger.info(f"Processing file: {csv_file}")
            # Load the dataset
            df = pd.read_csv(csv_file, parse_dates=["Date"])

            # Calculate daily percentage returns
            df["Return"] = df["Price"].pct_change()

            # Drop NaN values from returns
            returns = df["Return"].dropna()

            # Sort the returns and find the percentile corresponding to the confidence level
            var_percentile = (1 - confidence_level) * 100
            var = np.percentile(returns, var_percentile)

            # Convert VaR to percentage for readability
            var_percentage = var * 100
            var_results[csv_file.stem] = var_percentage

            logger.info(f"{csv_file.stem}: VaR at {confidence_level * 100}% confidence = {var_percentage:.2f}%")
        except Exception as e:
            logger.error(f"Error processing file {csv_file}: {e}")

    # Display or save the results
    if var_results:
        print("\nValue at Risk (VaR) Results:")
        for currency, var in var_results.items():
            print(f"{currency}: {var:.2f}%")
"""
        # Optionally save results to a CSV file
        results_df = pd.DataFrame(list(var_results.items()), columns=["Currency", "VaR (%)"])
        results_path = PROCESSED_DATA_DIR / "var_results.csv"
        results_df.to_csv(results_path, index=False)
        logger.success(f"VaR results saved to: {results_path}")
    else:
        logger.warning("No valid VaR data found.")
"""

if __name__ == "__main__":
    # Example confidence level: 95%
    calculate_historical_var(confidence_level=0.95)
