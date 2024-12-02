from pathlib import Path
import typer
from loguru import logger
from tqdm import tqdm
import pandas as pd 

from config import PROCESSED_DATA_DIR, RAW_DATA_DIR

"""
1. Find the dataset with the shortest time span, take this as a reference
2. Shorten all other datasets so that they are all the same length
3. Copy the datasets to processed folder
"""

def find_shortest_time_span():
    """
    Finds the dataset with the shortest time span in the RAW_DATA_DIR.
    
    Returns:
        str: The filename of the dataset with the shortest time span.
    """
    shortest_time_span = None
    reference_filename = None

    # Iterate over all CSV files in the raw data directory
    for csv_file in RAW_DATA_DIR.glob("*.csv"):
        logger.info(f"Processing file: {csv_file}")
        try:
            # Load the dataset
            df = pd.read_csv(csv_file, parse_dates=["Date"], dayfirst=True, quotechar='"')
            
            # Calculate the time span of the dataset
            start_date = df["Date"].min()
            end_date = df["Date"].max()
            time_span = (end_date - start_date).days
            
            logger.info(f"Dataset: {csv_file.name}, Start: {start_date}, End: {end_date}, Time Span: {time_span} days")
            
            # Update the reference dataset if this dataset has the shortest time span
            if shortest_time_span is None or time_span < shortest_time_span:
                shortest_time_span = time_span
                reference_filename = csv_file.name

        except Exception as e:
            logger.error(f"Error processing file {csv_file}: {e}")

    if reference_filename:
        logger.success(f"Reference dataset selected: {reference_filename} with a time span of {shortest_time_span} days")
    else:
        logger.error("No valid datasets found.")
    
    return reference_filename

def shorten_datasets_to_reference(reference_filename: str):
    """
    Shortens all datasets in RAW_DATA_DIR to match the time range of the reference dataset.
    The shortened datasets are saved to the PROCESSED_DATA_DIR.
    
    Args:
        reference_filename (str): The filename of the reference dataset.
    """
    logger.info(f"Using {reference_filename} as the reference dataset.")

    # Load the reference dataset to determine its time range
    reference_path = RAW_DATA_DIR / reference_filename
    try:
        reference_df = pd.read_csv(reference_path, parse_dates=["Date"], dayfirst=True, quotechar='"')
        reference_start_date = reference_df["Date"].min()
        reference_end_date = reference_df["Date"].max()
        logger.info(f"Reference dataset time range: {reference_start_date} to {reference_end_date}")
    except Exception as e:
        logger.error(f"Error loading reference dataset {reference_filename}: {e}")
        return

    # Ensure the processed data directory exists
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Iterate through all datasets
    for csv_file in RAW_DATA_DIR.glob("*.csv"):
        logger.info(f"Processing file: {csv_file}")
        try:
            # Load the dataset
            df = pd.read_csv(csv_file, parse_dates=["Date"], dayfirst=True, quotechar='"')
            
            # Filter the dataset to match the reference time range
            shortened_df = df[(df["Date"] >= reference_start_date) & (df["Date"] <= reference_end_date)]

            # Save the shortened dataset to the processed directory
            processed_path = PROCESSED_DATA_DIR / csv_file.name
            shortened_df.to_csv(processed_path, index=False)
            logger.success(f"Shortened dataset saved to: {processed_path}")
        except Exception as e:
            logger.error(f"Error processing file {csv_file}: {e}")

app = typer.Typer()


@app.command()
def main(
    output_path: Path = PROCESSED_DATA_DIR / "merged_dataset.csv",  # Output path for the merged file
):
    logger.info("Starting dataset check...")
    
    # Ensure the raw data directory exists
    if not RAW_DATA_DIR.exists():
        logger.error(f"Raw data directory does not exist: {RAW_DATA_DIR}")
        return

    # List all CSV files in the raw data directory
    csv_files = list(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        logger.error("No CSV files found in the raw data directory.")
        return

    logger.info(f"Found {len(csv_files)} files to check.")

    reference_filename = find_shortest_time_span()
    if reference_filename:
        shorten_datasets_to_reference(reference_filename)
    else:
        print("No valid reference dataset found.")

    


if __name__ == "__main__":
    app()
