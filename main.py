"""
This module is designed to automate the process of validating,
correcting, and integrating CSV and GeoJSON data for geographical information systems.
It leverages configuration settings, either specified via a configuration file or command-line arguments,
to guide the processing of CSV and GeoJSON files. 

Dependencies:
    - os: For interacting with the operating system, especially for file and directory operations.
    - config_manager: Manages application configuration, loading settings from files or command-line arguments.
    - csv_handler: Provides functionalities for processing CSV files, including validation and formatting.
    - geojson_handler: Handles the processing of GeoJSON files, integrating CSV data based on configuration.
    - logging: Used for logging information, warnings, and errors throughout the processing workflow.
    - sys: Enables interaction with the Python interpreter, particularly for exiting the program with status codes.
    - utils: Contains utility functions, such as validating the CSV file separator.

Workflow Overview:
    1. Configuration is loaded from a file or command-line arguments, establishing the parameters for processing.
    2. The existence of the output directory is verified, and it is created if it does not exist.
    3. The CSV file separator is validated against the expected format. 
    If a mismatch is detected, the user is prompted to provide the correct separator.
    4. The CSV file is processed to match the expected format, and results are outputted to specified paths.
    5. Processed CSV data is read and used to update a GeoJSON file according to the configurations specified.
    6. Errors and exceptions encountered during processing are logged,
    and the program exits with a non-zero status if critical issues occur.

Exception Handling:
The module employs exception handling to ensure that any errors encountered during the configuration loading,
CSV processing, or GeoJSON processing are logged. 
This approach facilitates troubleshooting by providing detailed
error messages and exits the program with an appropriate status code to indicate failure.
"""

import os
import config_manager
import csv_handler
import geojson_handler
import logging
import sys
import utils


def main():
    """
    Main function orchestrates the workflow for processing CSV and GeoJSON files based on configurations.

    Steps include:
    - Loading configuration from a file or command-line arguments.
    - Validating and possibly correcting the CSV file separator.
    - Processing the CSV file to match expected formats and outputting results.
    - Reading the processed CSV data.
    - Processing the GeoJSON file with CSV data and configurations.

    Exception handling is utilized to log errors and exit the program with a non-zero status on failure.
    """
    try:
        # Load configuration from file or CLI arguments
        cfg_manager = config_manager.ConfigManager()
        cfg_manager.get_config()

        # Ensure output directory exists
        outputs_dir = 'outputs'
        if not os.path.exists(outputs_dir):
            os.makedirs(outputs_dir)

        logging.info(
            f"Selected ID column in .csv: {cfg_manager.id_csv_column}")

        # Validate the CSV file separator, prompt for correction if invalid
        if not utils.is_valid_csv_separator(
                cfg_manager.input_csv_path,
                cfg_manager.csv_separator):
            logging.error("CSV separator does not match the expected format.")
            new_separator = input("Please enter the correct CSV separator: ")
            cfg_manager.csv_separator = new_separator

            if not utils.is_valid_csv_separator(
                    cfg_manager.input_csv_path,
                    cfg_manager.csv_separator):
                logging.error(
                    "CSV separator provided does not match the file format.")
                # Exit if the CSV separator still does not match after
                # correction
                sys.exit(1)

    except Exception as e:
        logging.error(f"Configuration error or invalid CSV separator: {e}")
        sys.exit(1)

    output_csv_path = os.path.join(outputs_dir, 'parcelles_edited.csv')
    inconsistencies_csv_path = os.path.join(
        outputs_dir, 'inconsistencies_csv.csv')
    inconsistencies_json_path = os.path.join(
        outputs_dir, 'inconsistencies_json.csv')

    # Process CSV file
    try:
        csv_handler.process_csv(
            cfg_manager.input_csv_path,
            cfg_manager.csv_separator,
            cfg_manager.id_csv_column,
            output_csv_path)
    except Exception as e:
        sys.exit(1)

    # Process GeoJSON file
    try:
        csv_data = csv_handler.read_csv(
            output_csv_path, cfg_manager.csv_separator)
        geojson_handler.process_geojson(
            cfg_manager.input_geojson_path,
            cfg_manager.output_geojson_path,
            csv_data,
            cfg_manager.prop_name,
            cfg_manager.individual_prop_name,
            inconsistencies_csv_path,
            inconsistencies_json_path)
    except Exception as e:
        logging.error(f"Error during GeoJSON processing: {e}")
        sys.exit(1)

    # Optionally, insert additional logging or operations here
if __name__ == '__main__':
    main()
