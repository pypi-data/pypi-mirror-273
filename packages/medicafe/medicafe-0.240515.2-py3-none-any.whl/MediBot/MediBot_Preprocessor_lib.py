from collections import OrderedDict, defaultdict
from datetime import datetime
import os
import csv
import sys

# Add parent directory of the project to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_dir)

try:
    import MediLink_ConfigLoader
    import MediLink_DataMgmt
except ImportError:
    from MediLink import MediLink_ConfigLoader
    from MediLink import MediLink_DataMgmt
    
try:
    from MediBot_UI import app_control
except ImportError:
    from MediBot import MediBot_UI
    app_control = MediBot_UI.app_control

"""
Draft Docstring to move over from Preprocessor.

Data Integrity and Validation
 Implement a mechanism to confirm the accuracy of entered data, potentially through a verification step or summary report.
 Enhance CSV integrity checks to identify and report potential issues with data format, especially concerning insurance policy numbers and special character handling.

Development Roadmap for crosswalk_update()
 Automation required for updating the crosswalk.json when new Medisoft insurance is discovered.
For open_csv_for_editing

Known Issues and Bugs
 Address the handling of '.' and other special characters that may disrupt parsing, especially under Windows XP.

For load_csv_data

Preprocessing Enhancements
 Optimize script startup and CSV loading to reduce initial latency.

Data Integrity and Validation
 Conduct a thorough CSV integrity check before processing to flag potential issues upfront.

Future Work
 Consolidate data from multiple sources (Provider_Notes.csv, Surgery_Schedule.csv, and Carols_CSV.csv) into a single table with Patient ID as the key, ensuring all data elements are aligned and duplicate entries are minimized.
 Implement logic to verify and match Patient IDs across different files to ensure data integrity before consolidation. (Catching errors between source data)
 Optimize the preprocessing of surgery dates and diagnosis codes for use in patient billing and scheduling systems.
"""
class InitializationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def initialize(config):
    global AHK_EXECUTABLE, CSV_FILE_PATH, field_mapping, page_end_markers
    
    try:
        AHK_EXECUTABLE = config.get('AHK_EXECUTABLE', "")
    except AttributeError:
        raise InitializationError("Error: 'AHK_EXECUTABLE' not found in config.")
    
    try:
        CSV_FILE_PATH = config.get('CSV_FILE_PATH', "")
    except AttributeError:
        raise InitializationError("Error: 'CSV_FILE_PATH' not found in config.")
    
    try:
        field_mapping = OrderedDict(config.get('field_mapping', {}))
    except AttributeError:
        raise InitializationError("Error: 'field_mapping' not found in config.")
    
    try:
        page_end_markers = config.get('page_end_markers', [])
    except AttributeError:
        raise InitializationError("Error: 'page_end_markers' not found in config.")


def open_csv_for_editing(csv_file_path):
    try:
        # Open the CSV file with its associated application
        os.system('start "" "{}"'.format(csv_file_path))
        print("After saving the revised CSV, please re-run MediBot.")
    except Exception as e:
        print("Failed to open CSV file:", e)
        
# Function to load and process CSV data
def load_csv_data(csv_file_path):
    try:
        # Check if the file exists
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError("***Error: CSV file '{}' not found.".format(csv_file_path))
        
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]  # Return a list of dictionaries
    except FileNotFoundError as e:
        print(e)  # Print the informative error message
        print("Hint: Check if CSV file is located in the expected directory or specify a different path in config file.")
        print("Please correct the issue and re-run MediBot.")
        sys.exit(1)  # Halt the script
    except IOError as e:
        print("Error reading CSV file: {}. Please check the file path and permissions.".format(e))
        sys.exit(1)  # Halt the script in case of other IO errors

# CSV Pre-processor Helper functions
def add_insurance_id_column(csv_data):
    for row in csv_data:
        row['Ins1 Insurance ID'] = ''  # Initialize the column with empty values

def filter_rows(csv_data):
    csv_data[:] = [row for row in csv_data if row.get('Patient ID', '').strip()]
    csv_data[:] = [row for row in csv_data if row.get('Primary Insurance', '').strip() not in ['AETNA', 'AETNA MEDICARE', 'HUMANA MED HMO']]

def convert_surgery_date(csv_data):
    for row in csv_data:
        try:
            row['Surgery Date'] = datetime.strptime(row.get('Surgery Date', ''), '%m/%d/%Y')
        except ValueError:
            row['Surgery Date'] = datetime.min  # Assign a minimum datetime value for sorting purposes

def sort_and_deduplicate(csv_data):
    csv_data.sort(key=lambda x: (x['Surgery Date'], x.get('Patient Last', '').strip()))
    unique_patients = {}
    for row in csv_data:
        patient_id = row.get('Patient ID')
        if patient_id not in unique_patients or row['Surgery Date'] < unique_patients[patient_id]['Surgery Date']:
            unique_patients[patient_id] = row
    csv_data[:] = list(unique_patients.values())
    csv_data.sort(key=lambda x: (x['Surgery Date'], x.get('Patient Last', '').strip()))

def combine_fields(csv_data):
    for row in csv_data:
        row['Surgery Date'] = row['Surgery Date'].strftime('%m/%d/%Y')
        first_name = row.get('Patient First', '').strip()
        middle_name = row.get('Patient Middle', '').strip()
        if len(middle_name) > 1:
            middle_name = middle_name[0]  # Take only the first character
        last_name = row.get('Patient Last', '').strip()
        row['Patient Name'] = "{}, {} {}".format(last_name, first_name, middle_name).strip()
        address1 = row.get('Patient Address1', '').strip()
        address2 = row.get('Patient Address2', '').strip()
        row['Patient Street'] = "{} {}".format(address1, address2).strip()

def apply_replacements(csv_data, crosswalk):
    replacements = crosswalk.get('csv_replacements', {})
    for row in csv_data:
        for old_value, new_value in replacements.items():
            if row.get('Patient SSN', '') == old_value:
                row['Patient SSN'] = new_value
            elif row.get('Primary Insurance', '') == old_value:
                row['Primary Insurance'] = new_value
            elif row.get('Ins1 Payer ID') == old_value:
                row['Ins1 Payer ID'] = new_value

def update_insurance_ids(csv_data, crosswalk):
    for row in csv_data:
        ins1_payer_id = row.get('Ins1 Payer ID', '').strip()
        MediLink_ConfigLoader.log("Ins1 Payer ID '{}' associated with Patient ID {}.".format(ins1_payer_id, row.get('Patient ID', "None")))
        if ins1_payer_id:
            if ins1_payer_id in crosswalk.get('payer_id', {}):
                medisoft_ids = crosswalk['payer_id'][ins1_payer_id].get('medisoft_id', [])
                if medisoft_ids:
                    medisoft_ids = [int(id) for id in medisoft_ids]
                    # TODO Try to match OpenPM's Insurance Name to get a better match
                    row['Ins1 Insurance ID'] = medisoft_ids[0] 
                    MediLink_ConfigLoader.log("Ins1 Insurance ID '{}' used for Payer ID {} in crosswalk.".format(row.get('Ins1 Insurance ID', ''), ins1_payer_id))
            else:
                MediLink_ConfigLoader.log("Ins1 Payer ID '{}' not found in the crosswalk.".format(ins1_payer_id))
                # Create a placeholder entry in the crosswalk, need to consider the medisoft_medicare_id handling later.
                if 'payer_id' not in crosswalk:
                    crosswalk['payer_id'] = {}
                crosswalk['payer_id'][ins1_payer_id] = {
                    'medisoft_id': [],
                    'medisoft_medicare_id': [],
                    'endpoint': 'OPTUMEDI' # Default probably should be a flag for the crosswalk update function to deal with. BUG HARDCODE THERE ARE 3 of these defaults
                } 

def load_data_sources(config, crosswalk):
    """Loads historical mappings from MAPAT and Carol's CSVs."""
    patient_id_to_insurance_id = load_insurance_data_from_mapat(config, crosswalk)
    if not patient_id_to_insurance_id:
        raise ValueError("Failed to load historical Patient ID to Insurance ID mappings from MAPAT.")

    payer_id_to_patient_ids = load_historical_payer_to_patient_mappings(config)
    if not payer_id_to_patient_ids:
        raise ValueError("Failed to load historical Carol's CSVs.")

    return patient_id_to_insurance_id, payer_id_to_patient_ids

def map_payer_ids_to_insurance_ids(patient_id_to_insurance_id, payer_id_to_patient_ids):
    """Maps Payer IDs to Insurance IDs based on the historical mappings."""
    payer_id_to_details = {}
    for payer_id, patient_ids in payer_id_to_patient_ids.items():
        medisoft_ids = set()
        for patient_id in patient_ids:
            if patient_id in patient_id_to_insurance_id:
                medisoft_id = patient_id_to_insurance_id[patient_id]
                medisoft_ids.add(medisoft_id)
                MediLink_ConfigLoader.log("Added Medisoft ID {} for Patient ID {} and Payer ID {}".format(medisoft_id, patient_id, payer_id))
            else:
                MediLink_ConfigLoader.log("No matching Insurance ID found for Patient ID {}".format(patient_id))
        if medisoft_ids:
            payer_id_to_details[payer_id] = {
                "endpoint": "OPTUMEDI",  # TODO Default, to be refined via API poll. There are 2 of these defaults!
                "medisoft_id": list(medisoft_ids),
                "medisoft_medicare_id": []  # Placeholder for future implementation
            }
    return payer_id_to_details

def load_insurance_data_from_mains(config):
    """
    Loads insurance data from MAINS and creates a mapping from insurance names to their respective IDs.
    This mapping is critical for the crosswalk update process to correctly associate payer IDs with insurance IDs.

    Args:
        config (dict): Configuration object containing necessary paths and parameters.

    Returns:
        dict: A dictionary mapping insurance names to insurance IDs.
    """
    # Reset config pull to make sure its not using the MediLink config key subset
    config, crosswalk = MediLink_ConfigLoader.load_configuration()
    
    # Retrieve MAINS path and slicing information from the configuration   
    # TODO (Low) For secondary insurance, this needs to be pulling from the correct MAINS (there are 2)
    # TODO (Low) Performance: There probably needs to be a dictionary proxy for MAINS that gets updated.
    mains_path = config['MAINS_MED_PATH']
    mains_slices = crosswalk['mains_mapping']['slices']
    
    # Initialize the dictionary to hold the insurance to insurance ID mappings
    insurance_to_id = {}
    
    # Read data from MAINS using a provided function to handle fixed-width data
    for record, line_number in MediLink_DataMgmt.read_general_fixed_width_data(mains_path, mains_slices):
        insurance_name = record['MAINSNAME']
        # Assuming line_number gives the correct insurance ID without needing adjustment
        insurance_to_id[insurance_name] = line_number
    
    return insurance_to_id

def load_insurance_data_from_mapat(config, crosswalk):
    """
    Loads insurance data from MAPAT and creates a mapping from patient ID to insurance ID.
    
    Args:
        config (dict): Configuration object containing necessary paths and parameters.
        crosswalk ... ADD HERE.

    Returns:
        dict: A dictionary mapping patient IDs to insurance IDs.
    """
    # Retrieve MAPAT path and slicing information from the configuration
    mapat_path = app_control.get_mapat_med_path()
    mapat_slices = crosswalk['mapat_mapping']['slices']
    
    # Initialize the dictionary to hold the patient ID to insurance ID mappings
    patient_id_to_insurance_id = {}
    
    # Read data from MAPAT using a provided function to handle fixed-width data
    for record, _ in MediLink_DataMgmt.read_general_fixed_width_data(mapat_path, mapat_slices):
        patient_id = record['MAPATPXID']
        insurance_id = record['MAPATINID']
        patient_id_to_insurance_id[patient_id] = insurance_id
        
    return patient_id_to_insurance_id

def parse_z_dat(z_dat_path, config):
    """
    Parses the Z.dat file to map Patient IDs to Insurance Names using the provided fixed-width file format.
    
    Args:
        z_dat_path (str): Path to the Z.dat file.
        config (dict): Configuration object containing slicing information and other parameters.
    
    Returns:
        dict: A dictionary mapping Patient IDs to Insurance Names.
    """
    patient_id_to_insurance_name = {}
    
    try:
        # Reading blocks of fixed-width data (3 lines per record: personal, insurance, service)
        for personal_info, insurance_info, service_info in MediLink_DataMgmt.read_fixed_width_data(z_dat_path):
            # Parsing the data using slice definitions from the config
            parsed_data = MediLink_DataMgmt.parse_fixed_width_data(personal_info, insurance_info, service_info, config.get('MediLink_Config', config))
        
            # Extract Patient ID and Insurance Name from parsed data
            patient_id = parsed_data.get('PATID')
            insurance_name = parsed_data.get('INAME')
            
            if patient_id and insurance_name:
                patient_id_to_insurance_name[patient_id] = insurance_name
                MediLink_ConfigLoader.log("Mapped Patient ID {} to Insurance Name {}".format(patient_id, insurance_name), config, level="INFO")
    
    except FileNotFoundError:
        MediLink_ConfigLoader.log("File not found: {}".format(z_dat_path), config, level="ERROR")
        raise
    except Exception as e:
        MediLink_ConfigLoader.log("Failed to parse Z.dat: {}".format(str(e)), config, level="ERROR")
        raise

    return patient_id_to_insurance_name

def load_historical_payer_to_patient_mappings(config):
    """
    Loads historical mappings from multiple Carol's CSV files in a specified directory,
    mapping Payer IDs to sets of Patient IDs.

    Args:
        config (dict): Configuration object containing the directory path for Carol's CSV files
                       and other necessary parameters.

    Returns:
        dict: A dictionary where each key is a Payer ID and the value is a set of Patient IDs.
    """
    directory_path = os.path.dirname(config['CSV_FILE_PATH'])
    payer_to_patient_ids = defaultdict(set)

    try:
        # Check if the directory exists
        if not os.path.isdir(directory_path):
            raise FileNotFoundError("Directory '{}' not found.".format(directory_path))

        # Loop through each file in the directory containing Carol's historical CSVs
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if filename.endswith('.csv'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile)
                        found_data = False  # Flag to track if any valid data is found in the CSV
                        for row in reader:
                            if 'Patient ID' not in row or 'Ins1 Payer ID' not in row:
                                continue  # Skip this row if either key is missing
                            if not row.get('Patient ID').strip() or not row.get('Ins1 Payer ID').strip():
                                continue  # Skip this row if either value is missing or empty
                            
                            found_data = True
                            payer_id = row['Ins1 Payer ID'].strip()
                            patient_id = row['Patient ID'].strip()
                            payer_to_patient_ids[payer_id].add(patient_id)
                            MediLink_ConfigLoader.log("Found Patient ID {} with Payer ID {}".format(patient_id, payer_id))
                        if not found_data:
                            MediLink_ConfigLoader.log("CSV file '{}' is empty or does not have either Patient ID or Payer ID.".format(filename))
                except Exception as e:
                    print("Error processing file {}: {}".format(filename, e))
    except FileNotFoundError as e:
        print("Error: {}".format(e))

    if not payer_to_patient_ids:
        print("No historical mappings were generated.")
    
    return dict(payer_to_patient_ids)