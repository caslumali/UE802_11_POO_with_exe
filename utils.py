# Import the logging module for logging error messages.
import logging


def is_valid_csv_separator(file_path: str, expected_separator: str) -> bool:
    """
    Checks if the given CSV file uses the expected separator.

    Args:
    file_path (str): Path to the CSV file.
    expected_separator (str): The expected separator character, e.g., ',', ';', or '\t'.

    Returns:
    bool: True if the expected separator is used, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the first line of the file
            first_line = file.readline()

            # Check if the expected separator is in the first line
            if expected_separator in first_line:
                # If the separator is found, return True indicating a valid
                # separator.
                return True
            else:
                return False
    except IOError as e:
        # Log an error message if the file can't be opened
        logging.error(f"Error opening file {file_path}: {e}")
        return False
    except Exception as e:
        # Log any other unexpected errors
        logging.error(f"Unexpected error: {e}")
        return False
