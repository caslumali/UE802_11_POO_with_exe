"""
This module creates a graphical user interface (GUI) application
for processing and managing parcel data from CSV and GeoJSON files. 
It integrates functionalities for file selection, CSV validation, and GeoJSON processing.

Dependencies:
    - tkinter: Used for creating the GUI components.
    - ttk, filedialog, simpledialog, messagebox: Tkinter modules for themed widgets,
    file selection dialogs, simple input dialogs, and message boxes, respectively.
    - config_manager: Manages application configuration settings.
    - csv_handler: Handles CSV file processing.
    - geojson_handler: Manages GeoJSON file processing.
    - os, csv: Standard Python modules for operating system interactions and CSV file operations.
    - logging: Provides logging functionalities.

Main Components:
    - TextHandler: A custom logging handler that directs logging output to a Tkinter Text widget
    - configure_logging: Configures the application's logging to output to the specified Tkinter Text widget.
    - browse_file, browse_folder: Functions to open file and folder dialog windows, 
    allowing the user to select files or directories and display their paths in the GUI.
    - validate_csv_separator, confirm_column_name: Validate the CSV file's structure, 
    including the separator and column names, ensuring compatibility with processing expectations.
    - submit(): The main function that handles the submission from the GUI,
    validating inputs and initiating the processing of selected files.

Usage:
The module is designed to be run as a standalone application. 
Upon execution, it presents a user-friendly interface that guides the user through the process of selecting input CSV and GeoJSON files
specifying processing options, and choosing an output directory for the processed files. 
The GUI also provides real-time feedback through a dedicated logging area.

Features:
    - Interactive file and directory selection.
    - Real-time logging within the GUI.
    - Input validation and error handling.
    - Configuration management through external modules.
    - Processing of CSV and GeoJSON files with customizable options.
"""
import config_manager
import csv
import csv_handler
import geojson_handler
import logging
import os
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox


class TextHandler(logging.Handler):
    """
    A custom logging handler that directs logging output to a Tkinter Text widget.

    Attributes:
        text_widget (tk.Text): The Tkinter Text widget to which log messages are directed.
    """

    def __init__(self, text_widget: tk.Text):
        """
        Initialize the handler with the Tkinter Text widget.

        Args:
            text_widget (tk.Text): A Tkinter Text widget instance.
        """
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record: logging.LogRecord):
        """
        Override the emit function to log a record to the text widget.

        Args:
            record (logging.LogRecord): Log record, which is a LogRecord object.
        """
        msg = self.format(record)  # Format the log message
        # Safely make changes to the text widget
        self.text_widget.configure(state='normal')
        # Append the message to the widget
        self.text_widget.insert(tk.END, msg + '\n')
        # Disable editing of the widget
        self.text_widget.configure(state='disabled')
        self.text_widget.yview(tk.END)  # Auto-scroll to the end of the widget


def configure_logging(log_text: tk.Text):
    """
    Configures logging to direct messages to a Tkinter Text widget.

    Args:
        log_text (tk.Text): A Tkinter Text widget where logs will be displayed.
    """
    # Create a text handler which directs logs to the text widget
    text_handler = TextHandler(log_text)
    # Set a formatter for the handler
    text_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'))
    # Set the logging level and add the handler to the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(text_handler)


def browse_file(entry: str, file_type: str) -> str:
    """Opens a dialog for the user to select a file and inserts the path into the associated entry field."""
    filetype_options = {
        "json": (("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")),
        "csv": (("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")),
    }
    filename = filedialog.askopenfilename(
        filetypes=filetype_options[file_type])
    if filename:  # Check if a file was selected
        entry.delete(0, tk.END)
        entry.insert(0, filename)


def browse_folder(entry: str) -> str:
    """Opens a dialog for the user to select a directory and inserts the path into the associated entry field."""
    foldername = filedialog.askdirectory()
    if foldername:  # Check if a directory was selected
        entry.delete(0, tk.END)
        entry.insert(0, foldername)


def validate_csv_separator(csv_file: str, separator: str, expected_column: int) -> bool:
    """
    Attempts to read the CSV file with the provided separator and checks for the expected column.
    Returns:
    - True if the column is found with the exact name.
    - 'wrong_case' if the column is found with a different case.
    - 'wrong_separator' if the separator is incorrect.
    - 'wrong_column' if the column name is incorrect.
    - False if an error occurs.
    """
    try:
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            # Vamos tentar ler o cabeçalho do arquivo para verificar o separador e a coluna
            header = csvfile.readline()
            if separator not in header:
                return 'wrong_separator'
            else:
                # Retorna ao início do arquivo para a leitura do csv
                csvfile.seek(0)
                reader = csv.DictReader(csvfile, delimiter=separator)
                fieldnames = reader.fieldnames
                if expected_column in fieldnames:
                    return True
                elif any(expected_column.lower() == col.lower() for col in fieldnames):
                    return 'wrong_case'
                else:
                    return 'wrong_column'
    except Exception as e:
        messagebox.showerror(
            "Erreur de validation CSV",
            f"Une erreur est survenue lors de la validation du séparateur CSV : {e}"
        )
        return False


def submit():
    """
    Handles the submission from the GUI form, validating inputs, and processing files accordingly.
    Checks for file existence, directory validity, and CSV separator before processing.
    Prompts the user for overwrite confirmation if the output GeoJSON file already exists.
    """
    # Retrieve input values from the GUI
    json_file = entries[0].get()
    csv_file = entries[1].get()
    csv_separator = entries[2].get()
    csv_id_column = entries[3].get()
    output_dir = entries[4].get()

    # Construct full paths for output files based on the output directory
    output_csv_path = os.path.join(output_dir, 'parcelles_edited.csv')
    inconsistencies_csv_path = os.path.join(
        output_dir, 'inconsistencies_csv.csv')
    inconsistencies_json_path = os.path.join(
        output_dir, 'inconsistencies_json.csv')
    output_geojson_path = os.path.join(output_dir, 'proprietaires.geojson')

    cfg_manager = config_manager.ConfigManager()

    # Atualiza as configurações diretamente
    cfg_manager.config['Paths']['InputCSV'] = csv_file
    cfg_manager.config['Paths']['InputGeoJSON'] = json_file
    cfg_manager.config['Paths']['OutputGeoJSON'] = output_geojson_path
    cfg_manager.config['Paths']['InconsistenciesCSV'] = inconsistencies_csv_path
    cfg_manager.config['Options']['IdCSVColumn'] = csv_id_column
    # Exemplo fixo, ajuste conforme necessário
    cfg_manager.config['Options']['PropName'] = 'Propriétaires'
    # Exemplo fixo, ajuste conforme necessário
    cfg_manager.config['Options']['IndividualPropName'] = 'Propriétaire'
    cfg_manager.config['Options']['CSVSeparator'] = csv_separator

    # Check if JSON and CSV files are selected
    if not os.path.exists(json_file) or not os.path.exists(csv_file):
        messagebox.showwarning(
            "Fichier introuvable", "Assurez-vous que les fichiers JSON et CSV sont sélectionnés.")
        return

    # Check if a valid output directory is selected
    if not os.path.isdir(output_dir):
        messagebox.showwarning("Répertoire de sortie invalide",
                               "Veuillez sélectionner un répertoire de sortie valide.")
        return

    # Validate the CSV separator with the user until a valid one is provided or the user cancels
    separator_valid = False
    column_name_correct = False
    while not separator_valid or not column_name_correct:
        result = validate_csv_separator(csv_file, csv_separator, csv_id_column)
        if result == True:
            separator_valid = True
            column_name_correct = True
        elif result == 'wrong_case':
            messagebox.showerror(
                "Erreur de validation CSV",
                "La colonne attendue a été trouvée avec une casse différente. Vérifiez la casse et réessayez."
            )
            return
        elif result == 'wrong_separator':
            new_separator = simpledialog.askstring(
                "Séparateur CSV incorrect",
                "Le séparateur spécifié n'est pas correct. Veuillez entrer le séparateur correct:",
                parent=root
            )
            if new_separator is not None and new_separator.strip() != '':
                csv_separator = new_separator.strip()
            else:
                messagebox.showinfo(
                    "Traitement annulé", "Le traitement a été annulé par l'utilisateur."
                )
                return
        elif result == 'wrong_column':
            messagebox.showerror(
                "Erreur de validation CSV",
                "Le nom de la colonne spécifié n'a pas été trouvé. Vérifiez le nom de la colonne et réessayez."
            )
            return
        else:
            messagebox.showerror(
                "Erreur de validation CSV",
                "Une erreur inattendue est survenue. Veuillez vérifier le fichier CSV et réessayer."
            )
            return

    # Only proceed if both the separator and the column name are correct
    if separator_valid and column_name_correct:
        # Check if the output GeoJSON file already exists and ask for overwrite confirmation
        if os.path.exists(output_geojson_path):
            overwrite = messagebox.askyesno("Fichier Existant",
                                            "Le fichier GeoJSON existe déjà. Voulez-vous le remplacer?")
            if not overwrite:  # Stop processing if the user does not confirm overwriting
                messagebox.showinfo("Processus Annulé",
                                    "Le processus a été annulé par l'utilisateur.")
                return

        # Process the files with the provided paths
        try:
            csv_handler.process_csv(
                csv_file, csv_separator, csv_id_column, output_csv_path)
            csv_data = csv_handler.read_csv(output_csv_path, csv_separator)
            geojson_handler.process_geojson(json_file, output_geojson_path, csv_data, 'Propriétaires',
                                            'Propriétaire', inconsistencies_csv_path, inconsistencies_json_path, overwrite_mode='gui')
            messagebox.showinfo(
                "Succès", "Les fichiers ont été traités avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur de traitement",
                                 f"Erreur lors du traitement des fichiers : {e}")
    else:
        messagebox.showerror(
            "Erreur de validation CSV",
            "Le séparateur CSV ou le nom de la colonne est incorrect. Veuillez les vérifier et réessayer."
        )


def confirm_column_name(csv_file: str, separator: str, expected_column: str) -> bool:
    """
    Check if the column name is the issue rather than the separator.
    :param csv_file: Path to the CSV file.
    :param separator: Separator character.
    :param expected_column: The exact name of the expected column.
    :return: True if the issue is with the column name, False if it's the separator.
    """
    try:
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=separator)
            # If the expected column is not found, but a case-insensitive match is found, return True
            return expected_column not in reader.fieldnames and \
                any(expected_column.lower() == col.lower()
                    for col in reader.fieldnames)
    except Exception as e:
        messagebox.showerror(
            "Erreur de validation CSV",
            f"Une erreur est survenue lors de la vérification du nom de la colonne : {e}"
        )
        return False


# Initialize the main application window
root = tk.Tk()
root.title("Configuration des fichiers : traitement des parcelles du cadastre ")

# Configure the application's style
style = ttk.Style()
style.theme_use('alt')

# Configure the style of buttons
color = "#6F3122"
style.configure('TButton', font=('Arial', 10), background=color,
                foreground='#D9C6A4', borderwidth=1, focusthickness=3, focuscolor='none',
                relief='raised', padding=2)
style.configure('TLabel', font=('Arial', 10),
                background='#D9C6A4', foreground='black')  # Style for the label text
style.configure('TEntry', font=('Arial', 10, 'bold'), padding=5,
                borderwidth=2)
style.map('TButton',
          background=[('active', color), ('pressed', '#5C4033')],
          foreground=[('active', 'white'), ('pressed', '#D9C6A4')],
          relief=[('pressed', 'sunken'), ('!pressed', 'raised')])  # Style for buttons when hovered

# Create a main frame to contain the GUI elements
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Define the input fields and set them up with labels
fields = ["Fichier JSON", "Fichier CSV", "Séparateur CSV",
          "Colonne ID CSV", "Répertoire de sortie"]
entries = []  # List to keep track of the entry widgets for retrieving their contents later

# Loop over the field names and create corresponding labels and entry widgets
for i, field in enumerate(fields):
    # Create a label with text aligned to the east (right)
    label = ttk.Label(main_frame, text=field + " :", anchor="e")
    label.grid(row=i, column=0, sticky="e", padx=5, pady=5)

    # Set a fixed width for all entry fields
    entry_width = 100

    # Create the entry with the specified width
    entry = ttk.Entry(main_frame, width=entry_width)
    # Align to west to prevent stretching
    entry.grid(row=i, column=1, sticky="w", padx=5, pady=5)
    entries.append(entry)


# Add buttons for browsing files and directories
browse_buttons = [
    ("Parcourir...", lambda: browse_file(entries[0], "json")),
    ("Parcourir...", lambda: browse_file(entries[1], "csv")),
    ("Parcourir...", lambda: browse_folder(entries[4]))
]

# Set up the browse buttons next to their corresponding entry widgets
for i, (text, command) in enumerate(browse_buttons, start=0):
    button = ttk.Button(main_frame, text=text, command=command)
    # Align buttons to the east-west
    button.grid(row=i, column=2, padx=5, pady=5, sticky="ew")

# Adding output path buttonslign buttons to the east-west
button.grid(row=4, column=2, padx=5, pady=5, sticky="ew")

# Create and place the submit button
submit_button = ttk.Button(
    main_frame, text="Soumettre", command=lambda: submit())
# Center the submit button
submit_button.grid(row=6, column=1, pady=10, sticky="ew")

# Configure the main frame to expand with the window
main_frame.columnconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


def clear_logs(log_text: tk.Text):
    """
    Clears the content of the logging area in the Tkinter Text widget.

    Args:
        log_text (tk.Text): A Tkinter Text widget from which logs will be cleared.
    """
    log_text.configure(
        state='normal')  # Temporarily make the text widget editable
    # Clear all the contents of the text widget
    log_text.delete('1.0', tk.END)
    log_text.configure(state='disabled')  # Disable editing of the widget again


#  Layout from the log widget
log_frame = ttk.LabelFrame(main_frame, text="Logs", padding="10 10 10 10")
log_frame.grid(column=0, row=7, columnspan=3, sticky=(
    tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

# Create a Text widget for displaying logs
log_text = tk.Text(log_frame, state='disabled', wrap='word', height=10)
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a Scrollbar for the Text widget
log_scrollbar = ttk.Scrollbar(
    log_frame, orient=tk.VERTICAL, command=log_text.yview)
log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the Text widget to use the Scrollbar
log_text.configure(yscrollcommand=log_scrollbar.set)
# Configure logging to direct logs to the log_text widget
configure_logging(log_text)
# Run the application's main event loop
root.mainloop()
