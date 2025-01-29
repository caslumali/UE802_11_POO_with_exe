# GeoJSON Parcel Processing Project

## Overview
This Python program is the final project for the UE802_11 Algorithmique et Programmation orientées objet course in the Master SIGMA at Université Toulouse Jean Jaurès/ENSAT. It processes and merges land parcel and owner data, combining CSV and GeoJSON files to generate an enhanced GeoJSON file. This file can be used in geographic information systems (GIS) like QGIS, offering a comprehensive view of property ownership. The program includes robust error handling and logging mechanisms for reliability and ease of debugging.

## Project Structure
```
GeoJSON_Parcel_Processing
|
├── build/
├── data/
├── docs/               # Screenshot of GUI interface 
├── config.ini          # Configuration file for paths and options
├── config_manager.py   # Handles configuration management
├── csv_handler.py      # Processes CSV data
├── geojson_handler.py  # Processes GeoJSON data
├── gui.py              # Graphical User Interface
├── main.py             # Entry point of the program
├── README.md        # Documentation
├── utils.py            # Utility functions
└── gui.spec            # Specification file for creating executables
```

## Graphical User Interface
The program features a GUI for ease of use. Below is a preview of the interface:

![GUI Screenshot](path/to/your/screenshot.png)

### Key Features of the GUI
- File and directory selection dialogs
- Input validation for CSV and GeoJSON files
- Real-time logging displayed within the GUI
- Simplified processing without command-line arguments

## Quick Start Guide

### Prerequisites
- Python 3.x installed ([Download Python](https://www.python.org/downloads/))

### Installation
1. **Download and Extract the Project**:
   Download the project files and extract them into a directory on your computer.

2. **Prepare Input Data**:
   Place the required CSV and GeoJSON files in an accessible location. Specify their paths in the `config.ini` file or via the GUI.

### Running the Program

#### Command Line
Run the following command from the project directory:
```bash
python main.py
```

#### GUI
To launch the GUI, use:
```bash
python gui.py
```

### Example Command-Line Execution
```bash
python main.py --input_csv "path/to/input.csv" --input_geojson "path/to/input.geojson" --output_geojson "path/to/output.geojson" --csv_separator ";"
```
Replace `"path/to/your/input.csv"`, `"path/to/your/input.geojson"`, and `"path/to/your/output.geojson"` with the actual paths to your files. Adjust the `--csv_separator ";"` as needed to match the delimiter used in your CSV file.


### Output Files
- Enhanced GeoJSON file: Contains combined parcel and owner data.
- Logs: Detailed logs of the processing.
- CSV with inconsistencies: Highlights any discrepancies between input files.

## Modules

### config_manager.py
Manages configurations from `config.ini` and command-line arguments. Ensures proper paths and options are set before processing begins.

### csv_handler.py
- Validates and processes the CSV file.
- Formats parcel IDs to match GeoJSON.
- Extracts and organizes owner data.

### geojson_handler.py
- Reads and updates the GeoJSON file.
- Merges owner data into parcels.
- Handles inconsistencies and exports detailed logs.

### utils.py
Provides utility functions for validating CSV separators and enhancing robustness.

### main.py
Coordinates the workflow:
1. Loads configuration.
2. Validates and processes input files.
3. Logs the execution flow.

### gui.py
A Tkinter-based graphical user interface for file selection and process initiation. Displays logs and handles errors interactively.

## Logging
Logs are stored in the `outputs` directory. Use them for debugging and auditing the process.

## Suggestions for Improvement
1. **Unit Testing**: Add automated tests for each module.
2. **Data Visualization**: Integrate with GIS platforms for direct visualization.
3. **Enhanced GUI**: Include more configuration options and better error messages.

## License
This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).

## Contact
For questions or collaborations:
- **Lucas Lima** - [caslumali@gmail.com](mailto:caslumali@gmail.com)
- **Robin Heckendorn** - [heckendornrobin@gmail.com](mailto:heckendornrobin@gmail.com)