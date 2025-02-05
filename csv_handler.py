"""
This module is designed to handle the processing of CSV files for a specific application,
focusing on manipulating and formatting parcel ID data and owner information. 
It provides functionalities for formatting a specific ID column to match a predefined format, 
processing a CSV to group owners by parcel ID, and exporting the processed data to a new CSV file.

Functions:
    - format_id_csv_column: Formats the ID field to match the specified ID format, 
    ensuring it aligns with the GeoJSON file requirements.
    - process_csv: Processes the input CSV file by grouping owners by their parcel ID, 
    handling invalid ID formats, and exporting the grouped data to a new CSV file.
    - read_csv: Reads a CSV file and returns a dictionary mapping parcel IDs to lists of owners,
    facilitating data manipulation and access.
    - export_to_csv : Exports the processed data, which maps parcel IDs to lists of owners, to a specified CSV file, ensuring data persistence and accessibility.

Dependencies:
    - csv: For reading from and writing to CSV files.
    - re: For regular expression matching, particularly in formatting ID columns.
    - logging: For logging messages, including errors and informational messages.
    - defaultdict from collections: For easily grouping data without initializing keys first.

"""

import csv
import logging
import re
from typing import Dict, List
from collections import defaultdict


def format_id_csv_column(id_csv_column):
    """
    Formats the 'Bg Emplacement' field to match the ID format in the GeoJSON file.

    The formatted ID will have 14 characters:
    - 5 digits for the 'code insee' of the commune
    - '0000' if the section has 1 letter, '000' if it has 2 letters
    - The section code (1 or 2 letters)
    - The parcel number, padded to 4 digits with leading zeros

    Parameters:
    bg_emplacement (str): The 'Bg Emplacement' field from the CSV file.

    Returns:
    str: The formatted parcel ID.
    """
    # Use a regular expression to extract the insee code, section code, and
    # parcel number from the 'Id column' field.
    match = re.match(r'(\d{5})\s*([A-Z]+)\s*(\d+)', id_csv_column)
    if match:
        insee_code, section_code, parcel_number = match.groups()
        # Pad the parcel number with leading zeros to ensure it's 4 digits
        parcel_number = parcel_number.zfill(4)
        # Determine the number of zeros based on the length of the section code
        zeros = '0000' if len(section_code) == 1 else '000'
        return f"{insee_code}{zeros}{section_code}{parcel_number}"
    else:
        # Log an error if the 'Id CSV column' doesn't match the expected
        # pattern
        logging.error(
            f"Id column value '{id_csv_column}' does not match the expected format.")
        raise ValueError(f"Invalid ID format: {id_csv_column}")


def process_csv(
        input_csv_path: str,
        csv_separator: str,
        id_csv_column: str,
        output_csv_path: str) -> None:
    """
    Processes the CSV file to group owners by parcel ID and exports the data.
    If an invalid ID format is detected, processing stops and logs an error.

    Parameters:
    input_csv_path (str): Path to the input CSV file.
    csv_separator (str): The separator used in the CSV file.
    id_csv_column (str): The name of the column containing the parcel ID.
    output_csv_path (str): Path to the output CSV file.
    """
    # Create a default dictionary to store owners by their formatted parcel ID.
    owners_by_parcel = defaultdict(list)

    # Log the paths of the CSV
    logging.info(f"Reading CSV from: {input_csv_path}")

    # Open the input CSV file and read it using a DictReader.
    with open(input_csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=csv_separator)
        for row in reader:
            # Attempt to format each 'Bg Emplacement' value to the required ID
            # format.
            try:
                formatted_id = format_id_csv_column(row[id_csv_column])
            except ValueError as e:
                # Log the error and stop processing if the ID is invalid.
                logging.error(f"Failed to process the CSV file: {e}")
                # Optionally, inform the user and exit or ask for a correct
                # column name.
                print(
                    "Invalid ID format found. Check the CSV file for errors or choose another column for the ID.")
                raise ValueError(
                    "Invalid ID format found. Check the CSV file for errors or choose another column for the ID.")

            # If the ID is valid, split the owner names and add them to the
            # dictionary.
            owners = row['Nom complet du proprietaire [BG]'].split(', ')
            owners_by_parcel[formatted_id].extend(owners)

        # After processing all rows without error, export the data to a CSV
        # file.
        export_to_csv(owners_by_parcel, output_csv_path, csv_separator)


def read_csv(input_csv_path: str, csv_separator: str) -> None:
    """
    Reads a CSV file and returns a dictionary of owners by parcel.

    Args:
    input_csv_path (str): Path to the input CSV file.
    csv_separator (str): The separator used in the CSV file.

    Returns:
    dict: A dictionary with the processed data from the CSV file.
    """
    # Initialize an empty dictionary to hold the data.
    owners_by_parcel = {}
    try:
        with open(input_csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv_separator)
            next(reader)  # Skip the header
            for row in reader:
                # Store each row's data in the dictionary.
                parcel_id, owners = row
                owners_by_parcel[parcel_id] = owners.split(', ')
    except Exception as e:
        # Log any exceptions that occur during reading.
        logging.error(f"Failed to read the CSV file: {e}")
        raise

    return owners_by_parcel


def export_to_csv(owners_by_parcel: Dict[str, List[str]], output_csv_path: str, csv_separator: str = ',') -> None:
    """Exports processed data to a CSV file.

    Args:
    owners_by_parcel (dict): Dictionary mapping parcel IDs to a list of owners.
    output_csv_path (str): Path to the output CSV file.
    csv_separator (str): Separator used in the CSV file.
    """
    try:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=csv_separator)
            writer.writerow(['Parcel ID', 'Owners'])
            for parcel_id, owners in owners_by_parcel.items():
                # Write each parcel ID and its corresponding owners.
                writer.writerow([parcel_id, ', '.join(owners)])
        logging.info(f"Data successfully exported to {output_csv_path}")
    except Exception as e:
        logging.error(f"Error exporting data to CSV: {e}")
