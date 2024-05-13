import csv
import os
from datetime import datetime, timedelta
import subprocess 

# Need this for running Medibot and MediLink
try:
    import MediLink_ConfigLoader
except ImportError:
    from . import MediLink_ConfigLoader

# Helper function to slice and strip values
def slice_data(data, slices):
    # Convert slices list to a tuple for slicing operation
    return {key: data[slice(*slices[key])].strip() for key in slices}

# Function to parse fixed-width Medisoft output and extract claim data
def parse_fixed_width_data(personal_info, insurance_info, service_info, config):
    # Load slice definitions from config within the MediLink_Config section
    personal_slices = config['fixedWidthSlices']['personal_slices']
    insurance_slices = config['fixedWidthSlices']['insurance_slices']
    service_slices = config['fixedWidthSlices']['service_slices']

    # Parse each segment
    parsed_data = {}
    parsed_data.update(slice_data(personal_info, personal_slices))
    parsed_data.update(slice_data(insurance_info, insurance_slices))
    parsed_data.update(slice_data(service_info, service_slices))
    
    MediLink_ConfigLoader.log("Successfully parsed data from segments", config, level="INFO")
    
    return parsed_data

# Function to read fixed-width Medisoft output and extract claim data
def read_fixed_width_data(file_path, config):
    # Reads the fixed width data from the file and yields each patient's
    # personal, insurance, and service information.
    MediLink_ConfigLoader.log("Starting to read fixed width data...")
    with open(file_path, 'r') as file:
        lines_buffer = []  # Buffer to hold lines for current patient data
        for line in file:
            stripped_line = line.strip()
            if stripped_line:  # Only process non-empty lines
                lines_buffer.append(stripped_line)
                # Once we have 3 lines of data, yield them as a patient record
                if len(lines_buffer) == 3:
                    personal_info, insurance_info, service_info = lines_buffer
                    MediLink_ConfigLoader.log("Successfully read data from file: {}".format(file_path), config, level="INFO")
                    yield personal_info, insurance_info, service_info
                    lines_buffer.clear()  # Reset buffer for the next patient record
            # If the line is blank but we have already started collecting a patient record,
            # we continue without resetting the buffer, effectively skipping blank lines.

# TODO (Refactor) Consider consolidating with the other read_fixed_with_data 
def read_general_fixed_width_data(file_path, slices):
    # handle any fixed-width data based on provided slice definitions
    with open(file_path, 'r', encoding='utf-8') as file:
        next(file)  # Skip the header
        for line_number, line in enumerate(file, start=1):
            insurance_name = {key: line[start:end].strip() for key, (start, end) in slices.items()}
            yield insurance_name, line_number

def consolidate_csvs(source_directory):
    """
    This default overwrites any existing CSV for the same day. We want this for the automated runs but want to switch through 
    the user interaction option if we're running interactive. This has not been implemented, but the helper function exists.
    """
    today = datetime.now()
    consolidated_filename = today.strftime("ERA_%m%d%y.csv")
    consolidated_filepath = os.path.join(source_directory, consolidated_filename)

    consolidated_data = []
    header_saved = False

    # Check if the file already exists and log the action
    if os.path.exists(consolidated_filepath):
        MediLink_ConfigLoader.log("The file {} already exists. It will be overwritten.".format(consolidated_filename))

    for filename in os.listdir(source_directory):
        filepath = os.path.join(source_directory, filename)
        if not filepath.endswith('.csv') or os.path.isdir(filepath) or filepath == consolidated_filepath:
            continue  # Skip non-CSV files, directories, and the target consolidated file itself

        # Check if the file was created within the last day
        modification_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        if modification_time < today - timedelta(days=1):
            continue  # Skip files not modified in the last day

        # Read and append data from each CSV
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Assumes all CSV files have the same header
            if not header_saved:  # Save header from the first file
                consolidated_data.append(header)
                header_saved = True
            consolidated_data.extend(row for row in reader)

        # Delete the source file after its contents have been added to the consolidation list
        os.remove(filepath)

    # Write consolidated data to a new or existing CSV file, overwriting it if it exists
    with open(consolidated_filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(consolidated_data)

    MediLink_ConfigLoader.log("Consolidated CSVs into {}".format(consolidated_filepath))
    
    return consolidated_filepath

def operate_winscp(operation_type, files, endpoint_config, local_storage_path, config):
    """
    General function to operate WinSCP for uploading or downloading files.

    :param operation_type: 'upload' or 'download'
    :param files: List of files to upload or pattern for files to download.
    :param endpoint_config: Dictionary containing endpoint configuration.
    :param local_storage_path: Base local storage path for logs and files.

    # Example of how to call this function for uploads
    upload_files = ['path/to/local/file1.txt', 'path/to/local/file2.txt']
    upload_config = {
        'session_name': 'MySession',
        'remote_directory_up': '/remote/upload/path'
    }

    operate_winscp('upload', upload_files, upload_config, 'path/to/local/storage', config)

    # Example of how to call this function for downloads
    download_config = {
        'session_name': 'MySession',
        'remote_directory_down': '/remote/download/path'
    }

    operate_winscp('download', None, download_config, 'path/to/local/storage', config)
    """
    # Setup paths
    try:
        # TODO (Easy / Config) Get this updated. ??
        winscp_path = config['winscp_path']
    except KeyError:
        winscp_path = os.path.join(os.getcwd(), "Installers", "WinSCP-Portable", "WinSCP.com")
    except Exception as e:
        # Handle any other exceptions here
        print("An error occurred while running WinSCP:", e)
        winscp_path = None
        
    if not os.path.isfile(winscp_path):
        MediLink_ConfigLoader.log("WinSCP.com not found at {}".format(winscp_path))
        return []

    # Setup logging
    log_filename = "winscp_upload.log" if operation_type == "upload" else "winscp_download.log"
    winscp_log_path = os.path.join(local_storage_path, log_filename)

    # Session and directory setup
    session_name = endpoint_config.get('session_name', '')
    remote_directory = endpoint_config['remote_directory_up'] if operation_type == "upload" else endpoint_config['remote_directory_down']

    # Command building
    command = [
        winscp_path,
        '/log=' + winscp_log_path,
        '/loglevel=1',
        '/command',
        'open {}'.format(session_name),
        'cd /',
        'cd {}'.format(remote_directory)
    ]

    # Add commands to WinSCP script
    # BUG (Low SFTP) We really need to fix this path situation.
    #  Unfortunately, this just needs to be a non-spaced path because WinSCP can't
    #  handle the spaces. Also, Windows won't let me use shutil to move the files out of G:\ into C:\ and it it wants an administrator security 
    #  check or verification thing for me to even move the file by hand so that doesn't work either. 
    #  command.append("put {}".format("C:\\Z_optumedi_04161742.txt"))
    if operation_type == "upload":
        for file_path in files:
            normalized_path = os.path.normpath(file_path)
            command.append("put {}".format(normalized_path))
    else:
        command.append('get *')  # Adjust pattern as needed

    command += ['close', 'exit']

    # Check if TestMode is enabled in the configuration
    if config.get("MediLink_Config", {}).get("TestMode", True):
        # TestMode is enabled, do not execute the command
        print("Test Mode is enabled! WinSCP Command not executed.")
        MediLink_ConfigLoader.log("Test Mode is enabled! WinSCP Command not executed.")
        MediLink_ConfigLoader.log("TEST MODE: Simulating WinSCP Upload File List.")
        uploaded_files = []
        for file_path in files:
            normalized_path = os.path.normpath(file_path)
            if os.path.exists(normalized_path):  # Check if the file exists before appending
                uploaded_files.append(normalized_path)
            else:
                MediLink_ConfigLoader.log("TEST MODE: Failed to upload file: {} does not exist.".format(normalized_path))
        return uploaded_files
    else:
        # TestMode is not enabled, execute the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        stdout, stderr = process.communicate()
    
    if process.returncode == 0: # BUG Does this work as intended?
        MediLink_ConfigLoader.log("WinSCP {} attempted.".format(operation_type))
        # Construct a list of downloaded files if operation_type is 'download'
        if operation_type == 'download':
            downloaded_files = []
            for root, dirs, files in os.walk(local_storage_path):
                for file in files:
                    downloaded_files.append(os.path.join(root, file))
            return downloaded_files
        
        if operation_type == 'upload':
            # Return a list of uploaded files
            uploaded_files = []
            for file_path in files:
                normalized_path = os.path.normpath(file_path)
                if os.path.exists(normalized_path):  # Check if the file exists before appending
                    uploaded_files.append(normalized_path)
                else:
                    MediLink_ConfigLoader.log("Failed to upload file: {} does not exist.".format(normalized_path))
            return uploaded_files
    else:
        MediLink_ConfigLoader.log("Failed to {} files. Details: {}".format(operation_type, stderr.decode('utf-8')))
        return []  # Return empty list to indicate failure. BUG check to make sure this doesn't break something else.

# UNUSED CSV Functions
"""
def remove_blank_rows_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        # Read the CSV file and filter out any empty rows
        rows = [row for row in csv.reader(csv_file) if any(field.strip() for field in row)]
    
    # Write the filtered rows back to the CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)

def list_chart_numbers_in_existing_file(filepath):
    # Lists the Chart Numbers contained in an existing CSV file.
    chart_numbers = []
    with open(filepath, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            if len(row) > 2:  # Assuming Chart Number is in the 3rd column
                chart_numbers.append(row[2])
    return chart_numbers
"""