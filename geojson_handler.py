"""
This module is designed for the processing of GeoJSON files,
focusing on updating property data, managing data inconsistencies,
and exporting these details efficiently. 
It incorporates functionalities for reading and writing GeoJSON files, 
exporting inconsistencies found during data processing to CSV files, 
and managing file overwriting with user confirmation.

Dependencies:
    - json: For handling JSON files, particularly for reading and writing GeoJSON data.
    - logging: For logging messages at various levels of severity (info, error, warning).
    - os: For interacting with the operating system, especially for file path manipulations and checking file existence.
    - csv: For operations related to CSV file handling, specifically for exporting inconsistencies.
    - time: For tracking the duration of the processing tasks.

Features and Functions:
    - read_geojson: Reads and returns the content of a GeoJSON file specified by the input path.
    - write_geojson: Writes the given data to a GeoJSON file at the specified output path.
    - export_inconsistencies: Exports a dictionary of inconsistencies to a CSV file
    - confirm_overwrite: Prompts the user for confirmation before overwriting an existing file
    - process_geojson: Processes an input GeoJSON file by updating it with owner information from a provided dictionary
"""

import json
import logging
import os
import csv
import time
from typing import Dict, List

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Sets the current working directory to the project root directory
# This confirms the good export of the files in the "outputs" folder
os.chdir(script_dir)

# Create the log directory if it does not exist
log_directory = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'outputs')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Logging to file
file_handler = logging.FileHandler(os.path.join(log_directory, 'project.log'))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))

# Logging to console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))

# Adding handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def read_geojson(input_geojson_path: str) -> dict:
    """Reads a GeoJSON file and returns its content."""

    # Log the paths of the CSV and JSON files
    logging.info(f"Reading JSON from: {input_geojson_path}")
    try:
        with open(input_geojson_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f'Error reading the GeoJSON file: {e}')
        raise


def write_geojson(data: dict, output_geojson_path: str) -> None:
    """Writes data to a GeoJSON file."""
    try:
        with open(output_geojson_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logging.info(
            f'GeoJSON file successfully written: {output_geojson_path}')
    except Exception as e:
        logging.error(f'Error writing the GeoJSON file: {e}')
        raise


def export_inconsistencies(
        inconsistencies: Dict[str, List[str]], output_path: str, csv_separator: str = ',') -> None:
    """
    Export inconsistencies to a specified CSV file.

    :param inconsistencies: A list of inconsistencies to be exported.
    :param output_path: The path where the inconsistencies CSV should be saved.
    :param csv_separator: The CSV separator to use.
    """
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=csv_separator)
            writer.writerow(['Parcel ID', 'Reason'])
            for parcel_id in inconsistencies:
                writer.writerow([parcel_id, 'No matching owner data'])
        logging.info(f"Inconsistencies exported to {output_path}")
    except Exception as e:
        logging.error(f"Error exporting inconsistencies to CSV: {e}")


def confirm_overwrite(file_path: str) -> bool:
    """Asks the user for confirmation to overwrite the GeoJson existing file."""
    if os.path.exists(file_path):
        response = input(
            f"The file '{file_path}' already exists. Do you want to overwrite it? (y/n): ")
        return response.lower() in ['yes', 'y']
    return True


def process_geojson(
        input_geojson_path: str,
        output_geojson_path: str,
        owners_by_parcel,
        prop_name: str,
        individual_prop_base_name: str,
        inconsistencies_csv_path: str,
        inconsistencies_json_path: str,
        overwrite_mode: str = 'ask') -> None:
    """
    Processes a GeoJSON file to update property data and manage data inconsistencies.
    This function takes the path to an input GeoJSON file and updates it with owner information
    based on a provided mapping. It also checks for and reports inconsistencies between the GeoJSON
    and a corresponding CSV dataset.

    Args:
        input_geojson_path (str): Path to the input GeoJSON file to be processed.
        output_geojson_path (str): Path where the updated GeoJSON file will be saved.
        owners_by_parcel (dict): A dictionary mapping parcel IDs to a list of owner names.
        prop_name (str): The property name under which owners will be listed in the GeoJSON file.
        individual_prop_base_name (str): A base name for properties in the GeoJSON file to list
                                         individual owners separately.
        inconsistencies_csv_path (str): Path to export any inconsistencies found in the CSV dataset.
        inconsistencies_json_path (str): Path to export any inconsistencies found in the GeoJSON dataset.
        overwrite_mode (str): Determines the mode of confirmation for file overwriting. It can be 'ask'
                              for terminal-based confirmation or 'gui' for GUI-based confirmation.

    Processing Steps:
        - Reads the input GeoJSON file.
        - Iterates over each feature, updating owner information from the `owners_by_parcel` mapping.
        - Checks for parcels present in the GeoJSON but not in the CSV (and vice versa) and reports them.
        - Handles file overwriting based on the provided `overwrite_mode`.
        - If overwrite is confirmed or not needed, writes the updated GeoJSON to the specified output path.

    Returns:
        bool: False if the operation was cancelled by the user during overwrite confirmation, True otherwise.
    """
    # Log the commencement of the processing with the specified property names
    logging.info(f"Processing GeoJSON with prop_name: {prop_name}")
    logging.info(
        f"Processing GeoJSON with individual_prop_name: {individual_prop_base_name}")

    # Record the start time for performance measurement
    start_time = time.time()

    # Read the existing GeoJSON data from the provided file path
    geojson_data = read_geojson(input_geojson_path)

    # Initialize counters for processed parcels and lists for inconsistencies
    processed_count = 0
    json_inconsistencies = []
    csv_inconsistencies = []

    # Iterate through each feature (parcel) in the GeoJSON data
    for feature in geojson_data['features']:
        parcel_id = feature['properties'].get('id', None)
        if parcel_id in owners_by_parcel:
            # Update feature properties with owners
            feature['properties'][prop_name] = ', '.join(
                owners_by_parcel[parcel_id])
            # Add individual owner properties if a base name is provided
            if individual_prop_base_name:
                for i, owner in enumerate(
                        owners_by_parcel[parcel_id], start=1):
                    feature['properties'][f'{individual_prop_base_name} {i}'] = owner
            processed_count += 1
        else:
            json_inconsistencies.append(parcel_id)

    # Check for parcels that are in the CSV but not in the GeoJSON
    for parcel_id in owners_by_parcel:
        if parcel_id not in [feature['properties'].get(
                'id') for feature in geojson_data['features']]:
            csv_inconsistencies.append(parcel_id)

    # Log processing time and counts
    elapsed_time = time.time() - start_time
    logging.info(f"GeoJSON processed in {elapsed_time:.2f} seconds")
    logging.info(f"Total of {processed_count} parcels processed")

    # Export any found inconsistencies to specified paths
    if json_inconsistencies:
        logging.warning(
            f"{len(json_inconsistencies)} parcels found in JSON but not in CSV")
        export_inconsistencies(json_inconsistencies, inconsistencies_json_path)

    if csv_inconsistencies:
        logging.warning(
            f"{len(csv_inconsistencies)} parcels found in CSV but not in JSON")
        export_inconsistencies(csv_inconsistencies, inconsistencies_csv_path)

    # Handle file overwriting confirmation based on mode
    if overwrite_mode == 'gui':
        # GUI mode: proceed without asking in terminal
        write_geojson(geojson_data, output_geojson_path)
    else:
        # Terminal mode: ask for confirmation in terminal
        if confirm_overwrite(output_geojson_path):
            write_geojson(geojson_data, output_geojson_path)
        else:
            logging.info("Operation cancelled by the user.")
            return False  # Indicate cancellation

 # The output GeoJSON file has been written if we reached this point
    logging.info(
        "GeoJSON file has been successfully updated and written to the output path.")
    return True  # Indicate success
