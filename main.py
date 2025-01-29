'''
Import necessary modules for file operations, command-line arguments,
configuration management, CSV and GeoJSON processing, logging,
system-specific operations, and utility functions.
'''
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
