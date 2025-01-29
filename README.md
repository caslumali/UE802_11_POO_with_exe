
---

# GeoJSON Parcel Processing Project

![Python Version](https://img.shields.io/badge/python-3.x-blue)
![License](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-green)

## Overview
This Python program is the final project for the UE802_11 Algorithmique et Programmation orientées objet course in the Master SIGMA at Université Toulouse Jean Jaurès/ENSAT. It processes and merges land parcel and owner data, combining CSV and GeoJSON files to generate an enhanced GeoJSON file. This file can be used in geographic information systems (GIS) like QGIS, offering a comprehensive view of property ownership. The program includes robust error handling and logging mechanisms for reliability and ease of debugging.

---

## Key Benefits
- **Efficient Data Integration**: Combines parcel and owner data seamlessly.
- **GIS Ready**: Outputs enhanced GeoJSON files directly usable in QGIS or other GIS platforms.
- **Error Detection**: Identifies and logs inconsistencies between input datasets.
- **User-Friendly Interface**: Simplifies processing with an intuitive GUI.

---

## Project Structure
```
GeoJSON_Parcel_Processing
|
├── build/
├── data/
├── docs/               # Screenshot of GUI interface
├── outputs/            # Logs and processed files
├── config.ini          # Configuration file for paths and options
├── config_manager.py   # Handles configuration management
├── csv_handler.py      # Processes CSV data
├── geojson_handler.py  # Processes GeoJSON data
├── gui.py              # Graphical User Interface
├── gui.exe             # Compiled GUI executable
├── main.py             # Entry point of the program
├── README.md           # Documentation
├── utils.py            # Utility functions
└── gui.spec            # Specification file for creating executables
```

---

## Graphical User Interface
The program features a GUI for ease of use. Below is a preview of the interface:

![GUI Screenshot](https://github.com/caslumali/UE802_11_POO_with_exe/blob/main/docs/print_gui.png)

### Key Features of the GUI
- File and directory selection dialogs.
- Input validation for CSV and GeoJSON files.
- Real-time logging displayed within the GUI.
- Simplified processing without command-line arguments.

---

## Workflow
Here’s an overview of the program’s workflow:

1. **Input Data**: The user provides a GeoJSON file and a CSV file containing parcel and owner information.
2. **Processing**:
   - The program validates and formats the data.
   - CSV owner data is merged into the GeoJSON file.
   - Inconsistencies are identified and logged.
3. **Output**:
   - Enhanced GeoJSON file.
   - CSV log of inconsistencies (if any).
   - Real-time logs for debugging.

---

## Quick Start Guide

### Prerequisites
- Python 3.x installed ([Download Python](https://www.python.org/downloads/)).

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

### Output Files
- **Enhanced GeoJSON File**: Contains combined parcel and owner data.
- **Logs**: Detailed logs of the processing.
- **CSV with Inconsistencies**: Highlights any discrepancies between input files.

---

## Configuration Guide

### Configuring `config.ini`
The `config.ini` file contains paths and options for the program. Example:
```ini
[Paths]
InputCSV = path/to/input.csv
InputGeoJSON = path/to/input.geojson
OutputGeoJSON = path/to/output.geojson

[Options]
IdCSVColumn = id_column_name
PropName = Propriétaires
IndividualPropName = Propriétaire
CSVSeparator = ;
```

---

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

---

## Logging
Logs are stored in the `outputs` directory. Use them for debugging and auditing the process.

---

## Suggestions for Improvement
1. **Unit Testing**: Add automated tests for each module.
2. **Data Visualization**: Integrate with GIS platforms for direct visualization.
3. **Enhanced GUI**: Include more configuration options and better error messages.

---

## How to Contribute
1. Fork this repository.
2. Create a branch for your feature: `git checkout -b feature/your-feature-name`.
3. Commit your changes: `git commit -m "Add your feature"`.
4. Push to your branch: `git push origin feature/your-feature-name`.
5. Open a pull request.

---

## License
This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).

---

## Contact
For questions or collaborations:
- **Lucas Lima** - [caslumali@gmail.com](mailto:caslumali@gmail.com)
- **Robin Heckendorn** - [heckendornrobin@gmail.com](mailto:heckendornrobin@gmail.com)

---
