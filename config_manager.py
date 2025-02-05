"""
This module serves as the program configuration manager. 
It primarily focuses on parsing parameterized information from a config.ini file, 
interpreting command-line arguments with argparse, 
and setting up logging parameters to be utilized across various modules.

Imported Libraries:
    - configparser: Used for parsing configuration files.
    - argparse: Facilitates parsing of command-line arguments.
    - os: Provides a way of using operating system dependent functionality.
    - logging: Supports logging of messages with varying levels of severity.

Features:
    - Sets the current working directory to the project's root directory.
    - Creates a dedicated log directory if it doesn't exist.
    - Initializes logging to record messages at the INFO level and above.

Class ConfigManager:
    - Initializes by reading the configuration from the config.ini file and parsing command-line arguments.
    - read_config_file`: Reads and validates the presence of the config.ini file,
    logging an error and exiting if not found.
    - parse_command_line_args: Parses command line arguments to override default settings in the config.ini file.
    - get_config: Accessor method that sets configuration data as instance attributes for easy access.
    - update_config: Allows for the programmatic update of configuration
    settings post-initialization, reflecting changes both in the configuration file and the class instance attributes.
"""
import configparser
import argparse
import os
import logging

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Sets the current working directory to the project root directory
os.chdir(script_dir)


# Create the log directory if it does not exist
log_directory = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'outputs')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Initialize logging to record messages with the level of INFO and above
logging.basicConfig(filename='outputs/project.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class ConfigManager:
    def __init__(self):
        # Initialize the parser and the configuration
        self.config = configparser.ConfigParser()
        self.read_config_file()
        self.parse_command_line_args()

    def read_config_file(self):
        """Reads the configuration from the config.ini file."""
        config_path = 'config.ini'
        if not os.path.exists(config_path):
            # Log an error and raise a FileNotFoundError if the config file is
            # missing
            logging.error('Config file not found. Exiting.')
            raise FileNotFoundError('Config file not found. Exiting.')

        # Read the config file and log the success
        self.config.read(config_path, encoding='utf-8')
        logging.info('Config file read successfully.')

    def parse_command_line_args(self):
        """Parses command line arguments and updates the configuration."""
        # Define the command line arguments that the program accepts
        parser = argparse.ArgumentParser(
            description='Process CSV and GeoJSON files for property data.')
        # Initialize the argument parser with a description.
        parser.add_argument(
            '--config', help='Path to the config file', default='config.ini')
        parser.add_argument('--input_csv', help='Path to the input CSV file')
        parser.add_argument('--input_geojson',
                            help='Path to the input GeoJSON file')
        parser.add_argument('--output_geojson',
                            help='Path to the output GeoJSON file')
        parser.add_argument('--inconsistencies_csv',
                            help='Path to the inconsistencies CSV file')
        parser.add_argument(
            '--id_csv_column',
            help='Column with the parcel ID in the .csv',
            default=self.config.get(
                'Options',
                'IdCSVColumn'))
        parser.add_argument(
            '--prop_name',
            help='Name of the property for the list of owners',
            default=self.config.get(
                'Options',
                'PropName'))
        parser.add_argument(
            '--individual_prop_name',
            help='Base name for individual property owners',
            default=self.config.get(
                'Options',
                'IndividualPropName'))
        parser.add_argument('--csv_separator', help='CSV separator',
                            default=self.config.get('Options', 'CSVSeparator'))

        # Parse the command line arguments
        args = parser.parse_args()

        # Update the configuration with command line arguments if provided
        if args.config:
            self.config.read(args.config)
        if args.input_csv:
            self.config.set('Paths', 'InputCSV', args.input_csv)
        if args.input_geojson:
            self.config.set('Paths', 'InputGeoJSON', args.input_geojson)
        if args.output_geojson:
            self.config.set('Paths', 'OutputGeoJSON', args.output_geojson)
        if args.inconsistencies_csv:
            self.config.set('Paths', 'InconsistenciesCSV',
                            args.inconsistencies_csv)
        if args.id_csv_column:
            self.config.set('Options', 'IdCSVColumn',
                            args.id_csv_column)
        if args.prop_name:
            self.config.set('Options', 'PropName', args.prop_name)
        if args.individual_prop_name:
            self.config.set('Options', 'IndividualPropName',
                            args.individual_prop_name)
        if args.csv_separator:
            self.config.set('Options', 'CSVSeparator', args.csv_separator)
            logging.info(f"CSV separator set to: {args.csv_separator}")

        # Log that the command line arguments have been processed
        logging.info('Command line arguments processed.')

    def get_config(self):
        """Sets the configuration as instance attributes."""
        self.input_csv_path = self.config.get('Paths', 'InputCSV')
        self.input_geojson_path = self.config.get('Paths', 'InputGeoJSON')
        self.output_geojson_path = self.config.get('Paths', 'OutputGeoJSON')
        self.inconsistencies_csv_path = self.config.get(
            'Paths', 'InconsistenciesCSV')
        self.id_csv_column = self.config.get('Options', 'IdCSVColumn')
        self.prop_name = self.config.get('Options', 'PropName')
        self.individual_prop_name = self.config.get(
            'Options', 'IndividualPropName')
        self.csv_separator = self.config.get('Options', 'CSVSeparator')

    def update_config(
            self,
            input_csv: str,
            input_geojson: str,
            output_geojson: str,
            inconsistencies_csv: str,
            id_csv_column: str,
            prop_name: str,
            individual_prop_name: str,
            csv_separator: str) -> None:
        self.config.set('Paths', 'InputCSV', input_csv)
        self.config.set('Paths', 'InputGeoJSON', input_geojson)
        self.config.set('Paths', 'OutputGeoJSON', output_geojson)
        self.config.set('Paths', 'InconsistenciesCSV', inconsistencies_csv)
        self.config.set('Options', 'IdCSVColumn', id_csv_column)
        self.config.set('Options', 'PropName', prop_name)
        self.config.set('Options', 'IndividualPropName', individual_prop_name)
        self.config.set('Options', 'CSVSeparator', csv_separator)
        logging.info('Configuration updated via GUI.')

        # Now update the instance attributes
        self.input_csv_path = input_csv
        self.input_geojson_path = input_geojson
        self.output_geojson_path = output_geojson
        self.inconsistencies_csv_path = inconsistencies_csv
        self.id_csv_column = id_csv_column
        self.prop_name = prop_name
        self.individual_prop_name = individual_prop_name
        self.csv_separator = csv_separator

        logging.info('Configuration and attributes updated via GUI.')


if __name__ == '__main__':
    # Main execution block of the script.
    try:
        # Create a ConfigManager instance and retrieve the configuration
        config_manager = ConfigManager()
        config = config_manager.get_config()
        # Log the successful loading of configuration
        logging.info('Configuration loaded successfully.')
        # Here you can add more logic or call other modules as needed.
    except Exception as e:
        # Log any exceptions that occur and print an error message
        logging.error(f'An error occurred: {e}')
        print(f'An error occurred: {e}')
