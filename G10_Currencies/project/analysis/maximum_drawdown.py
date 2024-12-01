import sys
import pandas as pd
from pathlib import Path

# Add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from loguru import logger
from config import PROCESSED_DATA_DIR


def calculate_maximum_drawdown():
    """
    Calculate the maximum drawdown (MDD) for each currency.
    """
    logger.info("Starting maximum drawdown (MDD) analysis...")

    # Ensure the processed data directory exists
    if not PROCESSED_DATA_DIR.exists():
        logger.error(f"Processed data directory does not exist: {PROCESSED_DATA_DIR}")
        return

    # List all processed CSV files
    csv_files = list(PROCESSED_DATA_DIR.glob("*.csv"))
    if not csv_files:
        logger.error("No processed datasets found.")
        return

    # Initialize a dictionary to store MDD results
    mdd_results = {}

    # Process each dataset
    for csv_file in csv_files:
        try:
            logger.info(f"Processing file: {csv_file}")
            # Load the dataset
            df = pd.read_csv(csv_file, parse_dates=["Date"])

            # Calculate the rolling maximum price up to each time point
            df["Rolling Max"] = df["Price"].cummax()

            # Calculate the drawdown as a percentage
            df["Drawdown"] = (df["Price"] - df["Rolling Max"]) / df["Rolling Max"] * 100

            # Identify the maximum drawdown
            max_drawdown = df["Drawdown"].min()
            mdd_results[csv_file.stem] = max_drawdown

            logger.info(f"{csv_file.stem}: Maximum Drawdown = {max_drawdown:.2f}%")
        except Exception as e:
            logger.error(f"Error processing file {csv_file}: {e}")

    # Display or save the results
    if mdd_results:
        print("\nMaximum Drawdown (MDD) Results:")
        for currency, mdd in mdd_results.items():
            print(f"{currency}: {mdd:.2f}%")
"""
        # Optionally save results to a CSV file
        results_df = pd.DataFrame(list(mdd_results.items()), columns=["Currency", "Maximum Drawdown (%)"])
        results_path = PROCESSED_DATA_DIR / "mdd_results.csv"
        results_df.to_csv(results_path, index=False)
        logger.success(f"MDD results saved to: {results_path}")
    else:
        logger.warning("No valid MDD data found.")
"""

if __name__ == "__main__":
    calculate_maximum_drawdown()
