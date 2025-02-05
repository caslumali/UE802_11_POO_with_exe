# GeoJSON Parcel Processing Project

This project was produced as the final result of the course *Algorithmique et Programmation Orientées Objet* conducted during the SIGMA master's program at Université Toulouse 2 - Jean Jaurès.


## Overview

This Python program is designed to process and merge land parcels from the French cadastre and owner data. The aim of this programa it's combining information from CSV and GeoJSON files to generate a final enhanced GeoJSON file. This enhanced file is ideal for use in geographic information systems (GIS) like QGIS, providing a comprehensive view of property ownership. The program is equipped with robust error handling and logging mechanisms to ensure reliability and ease of debugging.

## Table of Contents

- [Start Guide](#start-guide)
  - [Prerequisites](#prerequisites)
  - [Accessing the Program](#accessing-the-program)
- [Running the Program](#running-the-program)
  - [Via main.py](#running-the-program-via-mainpy)
  - [Through GUI via gui.py](#running-the-program-through-gui-via-guipy)
  - [Through a GUI executable](#running-the-program-through-a-gui-executable)
- [API QGIS](#api-qgis)
  - [Prerequisites](#prerequisites-1)
  - [API Execution](#api-execution)
- [Structure of the Program](#structure-of-the-program)
- [How the Program Works](#how-the-program-works)
  - [Startup](#startup)
  - [Processing Workflow](#processing-workflow)
  - [Outputs Generated and Dynamics](#outputs-generated-and-dynamics)
- [Command-Line Interface](#command-line-interface)
  - [Accessing Help](#accessing-help)
  - [Available Command-Line Arguments](#available-command-line-arguments)
- [Logging](#logging)
- [License](#license)
- [Contact Information](#contact-information)


## Start Guide

This guide will help you quickly set up and run the GeoJSON Parcel Processing Project on your system.

### Prerequisites
- Make sure Python 3.x is installed on your computer. If you need to install Python, visit [python.org](https://www.python.org/downloads/) for download instructions.

### Accessing the Program
1. **Download and extract the project**:
   Obtain the project files from your students :D or download them from GitHub.
   Extract the files to a directory on your computer.

2. **Content**:
   The zipped folder contains all the files necessary for the program to function. In the main folder are all the Python modules and two additional folders:

   - A folder named `data`, with the .CSV and the JSON that will be processed.
   - A folder named `bonus` that contains a) a QGIS project, b) a Python script to be executed in the QGIS API, and c) a standalone executable of the program that works independently on Windows PCs.
   
3. **Operation** The program is designed to be executed in three ways:
   - By running the [main.py](#running-the-program-via-mainpy) file.
   - Through a Graphical User Interface (GUI) by running the [gui.py](#running-the-program-via-guipy) file.
   - Using the GUI executable [Proj_GeoJSON.exe](#running-the-program-via-graphical-user-interface-gui-executable) in the **bonus** folder.

----

### Running the Program via main.py
To run the program via `main.py`, open a command prompt or terminal in the directory where the project files are located and execute the following command:

```
python main.py
```
You can customize the execution of the program using various command-line arguments to specify file paths and options directly (refer to the [Command-Line Interface](#command-line-interface) section for details).

### Example Execution
For example, to run the program with a custom CSV separator and specific file paths, you might use the following command:
```bash
python main.py --input_csv "path/to/your/input.csv" --input_geojson "path/to/your/input.geojson" --output_geojson "path/to/your/output.geojson" --csv_separator ";"
```
Replace `"path/to/your/input.csv"`, `"path/to/your/input.geojson"`, and `"path/to/your/output.geojson"` with the actual paths to your files. Adjust the `--csv_separator ";"` as needed to match the delimiter used in your CSV file.

---

### Running the Program through GUI via gui.py
To run the program via `gui.py`, open a command prompt or terminal in the directory where the project files are located and execute the following command:
```bash
python gui.py
```
The options for this execution are the same as those for execution through `main.py`, except for the option to differently name the column for owners and individual owners.

![GUI Screenshot](http://robinsigma.alwaysdata.net/image/ihm.png)

---

### Running the Program through a GUI executable
If you prefer, you can use the program directly through an executable GUI located in the `bonus` folder, named `Proj_GeoJSON.exe`. 

This executable is standalone and can be used on any computer with the Windows operating system. The options are the same as those available through execution via the `gui.py` file.


## API QGIS

As an additional feature, a Python script was created that can be executed directly in the QGIS software to visualize the final exported GeoJSON with a layer styling.

### Prerequisites
- Make sure QGIS 3.x is installed on your computer. If you need to install QGIS, visit [qgis.org](https://qgis.org/en/site/forusers/alldownloads.html) for download instructions.

- Run the program at least once and have the final exported GeoJSON in a folder named `outputs` in the root project folder. The Python script used in the QGIS API uses relative paths to load the file, so adhering to the folder hierarchy is crucial.

For the successful execution of the API, it is imperative that the QGIS project be run in the same folder as the Python file `pyQGIS.py`; therefore, we have left an empty QGIS project in the bonus folder named `QGIS_projGeoJSON.qgz` that we recommend using.

### API Execution
With QGIS open, go to `Plugins > Python Console`.
If you want, you can directly execute the file in the terminal using the command below:

```
exec(Path('pyQGIS.py').read_text())
```
If desired, you can open the file `pyQGIS.py` and run it through the editor within the Python Console.

If the prerequisites regarding the file and project hierarchy have been met, the program will automatically load the file `proprietaires.geojson` and open it as a layer named ***Propriétaires***. The layer styling will be applied automatically.


## Structure of the Program

The project is structured into several modules, each handling a specific aspect of the data processing:

1. **config_manager.py**: Manages configuration settings, including file paths and options, using both a `config.ini` file and command-line arguments. It ensures that the program runs with the correct parameters and allows for flexible configuration.

2. **csv_handler.py**: Responsible for processing the CSV file containing property owner information. It includes functionality to format and extract relevant data, ensuring compatibility with the GeoJSON format.

3. **geojson_handler.py**: Handles the GeoJSON file processing. This module merges the owner data from the CSV file into the GeoJSON file, enhancing it with additional property owner information.

4. **utils.py**: Provides utility functions such as CSV file validation to ensure proper handling of various CSV formats and enhance the program's robustness.

5. **main.py**: Serves as the entry point of the program. It orchestrates the overall workflow, utilizing the above modules to load data, process it, and generate the final GeoJSON file.

6. **gui.py** : Handles the creation and management of the Graphical User Interface.

## How the Program Works

### Startup
- Upon being launched via `main.py` or `gui.py`, the program begins by initializing settings using `config_manager.py`, which reads settings from the `config.ini` file and parses any command-line arguments provided.

### Processing Workflow

- `csv_handler.py` processes the .CSV file from city hall, formatting the ID column and extracting owner names to create a dictionary with these key values. It then outputs a .CSV file with this processed data named `parcelles_edited.csv`

- `geojson_handler.py` reads the input JSON from the French cadastre, merging the parcel IDs with the dictionary generated from the .CSV file. It outputs a GeoJSON file and two .CSV files listing inconsistencies found between the JSON and the original .CSV.

### Outputs Generated and Dynamics
The program generates the following outputs:
1. **parcelles_edited.csv**: This file is generated by modifying the original .CSV's ID column to incorporate owner data for each ID.

2. **proprietaires.geojson**: The primary output, containing teh Frence cadastre parcels annotated with owner names.

3. **inconsistencies_csv.csv**: Identifies parcels present in the municipality's .CSV but missing in the cadastre's JSON.

4. **inconsistencies_json.csv**: Highlights parcels found in the cadastre's JSON but absent in the municipality's .CSV.

5. **project.log**: Logs details of each program execution.

On the first run via `main.py` or `gui.py`, if the `outputs` folder is not defined, the program will create it in the project's root directory to store all outputs.

The program prompts for confirmation before overwriting the `proprietaires.geojson` file in subsequent runs. Other outputs are overwritten automatically.

The `proprietaires.geojson` file is compatible with GIS applications like QGIS for further analysis or visualization.

## Command-Line Interface

The program is equipped with a comprehensive command-line interface, offering users the flexibility to customize its operation according to their specific requirements. This functionality makes the program adaptable to a variety of data formats and user scenarios.

### Accessing Help
For a quick guide on how to use these options, you can invoke the help command:
```bash
python main.py --help
```

### Available Command-Line Arguments

- `--config CONFIG`: Specify the custom configuration file path. This allows you to use different settings without modifying the source code.

- `--input_csv INPUT_CSV`: Set the path to your input CSV file. This file should contain the property owner data you wish to process.

- `--input_geojson INPUT_GEOJSON`: Define the path to your input GeoJSON file. This file is expected to hold the parcel data for processing.

- `--output_geojson OUTPUT_GEOJSON`: Determine where to save the enhanced GeoJSON file after processing. This file will combine both parcel and owner information.

- `--inconsistencies_csv INCONSISTENCIES_CSV`: Provide a path to save a CSV file that records any inconsistencies or issues found during data processing. This is crucial for data validation and quality control.

- `--id_csv_column ID_CSV_COLUMN` : Indicate the name of the column within the CSV file that contains the ID value.

- `--prop_name PROP_NAME`: Specify the property field's name in the GeoJSON file, which will hold the list of owners. This parameter ensures the correct labeling of data in the output file.

- `--individual_prop_name INDIVIDUAL_PROP_NAME`: Set the base name for individual property owners in the GeoJSON file. This option allows for more detailed data representation.

- `--csv_separator CSV_SEPARATOR`: Choose the separator character used in the CSV file. This feature ensures compatibility with CSV files using different delimiter characters like commas (','), semicolons (';'), or tabs ('\t'). You must enclose the separator in quotes to ensure it is correctly processed

## Logging

- Comprehensive logging tracks critical events, processing steps, and errors, aiding in troubleshooting and insight into the program's operations.
- Logs are saved to `project.log` in the `outputs` directory, accessible for review post-execution and through the GUI.


## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License - see the [LICENSE](http://creativecommons.org/licenses/by-nc-sa/4.0/) page for details. Under this license, you are free to:

- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

The licensor cannot revoke these freedoms as long as you follow the license terms. Terms include:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **NonCommercial** — You may not use the material for commercial purposes.
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

## Contact Information

For questions, suggestions, or collaborations related to this project, please reach out to:

- **Lucas Lima** - Email: [caslumali@gmail.com](mailto:caslumali@gmail.com)
- **Robin Heckendorn** - Email: [heckendornrobin@gmail.com](mailto:heckendornrobin@gmail.com)

We appreciate your interest in our project and look forward to hearing from you!