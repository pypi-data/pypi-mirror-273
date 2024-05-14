import os

import MediLink_Down
import MediLink_Up
import MediLink_ConfigLoader
import MediLink_837p_encoder

# For UI Functions
import os
import MediLink_UI  # Import UI module for handling all user interfaces
from tqdm import tqdm

# Add parent directory of the project to the Python path
import sys
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_dir)

from MediBot.MediBot_Preprocessor import load_insurance_data_from_mains


"""
Development Tasks for Backend Enhancement in MediSoft Claims Submittal (MediLink) Script:

Implement dynamic configurations for multiple endpoints (Availity, Optum, PNT Data) with environmental settings support.
Enhance file detection with detailed logging and introduce integrity checks for pre-processing validation.
Verify file transmissions via WinSCP log analysis for successful endpoint acknowledgments and secure data transfer.
Automate response file handling from endpoints and integrate feedback into MediSoft with exception alerts.
De-persisting Intermediate Files.
When transmissions fail, there is some retaining of patient data in memory or something that seems to default
any new endpoint changes to Optum. May need to "de-confirm" patients, but leave the suggested endpoints as the previously
confirmed endpoints. This should be similar logic to if the user made a mistake and wants to go back and fix it.
These tasks involve backend enhancements such as dynamic configurations, file detection improvements, file transmission verification, automation of response file handling, and management of intermediate files and transmission failures.

TODO (Low) Availity has a response file that says "File was received at TIME. File was sent for processing." as a confirmation 
that sits in the SendFiles folder after a submittal. 

TODO (Crosswalk) When an endpoint is updated in the UI, the crosswalk should also be updated and saved for that payer ID because that payer ID
would basically forever need to be going to that endpoint for any patient. the suggested_endpoint should eventually be always correct.

BUG Suggested Endpoint when you say 'n' to proceed with transmission is not getting updated with the endpoint 
that was selected previously by the user. However, when we go back to the confirmation list, we do have a persist of the assignment.
This can be confusing for the user.

MediLink
| - import MediLink_Down
|   - import MediLink_ERA_decoder
|   |   - from MediLink_ConfigLoader import load_configuration
|   |   |   - None
|   |   - from MediLink_DataMgmt import consolidate_csvs
|   |   |   - from MediLink import MediLink_ConfigLoader
|   |           - None
|   - from MediLink_DataMgmt import operate_winscp
|       - from MediLink import MediLink_ConfigLoader
|           - None
| - import MediLink_Up
|   - None
| - import MediLink_ConfigLoader
|   - None
| - import MediLink_837p_encoder
|   - import MediLink_ConfigLoader
|   |   - None
|   - from MediLink_DataMgmt import parse_fixed_width_data, read_fixed_width_data
|       - from MediLink import MediLink_ConfigLoader
|           - None
|   - import MediLink_837p_encoder_library
|       - from MediLink import MediLink_ConfigLoader
|           - None
| - import MediLink_UI
|   - None
"""

def detect_and_display_file_summaries(directory_path, config, crosswalk):
    """
    Detects new files in the specified directory and prepares detailed patient data for processing,
    including suggestions for endpoints based on insurance provider information found in the config.
    
    :param directory_path: Path to the directory containing files to be detected.
    :param config: Configuration settings loaded from a JSON file.
    :return: A tuple containing a list of new file paths and the detailed patient data.
    """
    new_files = detect_new_files(directory_path)
    if not new_files:
        print("    No new claims detected. Check Medisoft claims output.\n")
        return False, []

    detailed_patient_data = []  # Initialize list for detailed patient data
    for file_path in new_files:
        detailed_data = extract_and_suggest_endpoint(file_path, config, crosswalk)
        detailed_patient_data.extend(detailed_data)  # Accumulate detailed data for processing

    # Return just the list of new files and the enriched detailed patient data
    return new_files, detailed_patient_data

def detect_new_files(directory_path, file_extension='.DAT'):
    """
    Scans the specified directory for new files with a given extension.
    
    :param directory_path: Path to the directory containing files to be detected.
    :param file_extension: Extension of the files to detect. Defaults to '.csv'.
    :return: A list of paths to new files detected in the directory.
    """
    detected_file_paths = []
    for filename in os.listdir(directory_path):
        if filename.endswith(file_extension):
            file_path = os.path.join(directory_path, filename)
            detected_file_paths.append(file_path)
    return detected_file_paths

def extract_and_suggest_endpoint(file_path, config, crosswalk):
    """
    Reads a fixed-width file, extracts file details including surgery date, patient ID, 
    patient name, primary insurance, and other necessary details for each record. It suggests 
    an endpoint based on insurance provider information found in the crosswalk and prepares 
    detailed patient data for processing.
    
    Parameters:
    - file_path: Path to the fixed-width file.
    - crosswalk: Crosswalk dictionary loaded from a JSON file.

    Returns:
    - A comprehensive data structure retaining detailed patient claim details needed for processing,
      including new key-value pairs for file path, surgery date, patient name, and primary insurance.
    """
    detailed_patient_data = []
    
    # Load insurance data from MAINS to create a mapping from insurance names to their respective IDs
    insurance_to_id = load_insurance_data_from_mains(config)
    MediLink_ConfigLoader.log("Insurance data loaded from MAINS. {} insurance providers found.".format(len(insurance_to_id)))

    for personal_info, insurance_info, service_info in MediLink_837p_encoder.read_fixed_width_data(file_path, config.get('MediLink_Config', {})):
        parsed_data = MediLink_837p_encoder.parse_fixed_width_data(personal_info, insurance_info, service_info, config.get('MediLink_Config', {}))
        
        primary_insurance = parsed_data.get('INAME')
        
        # Retrieve the insurance ID associated with the primary insurance
        insurance_id = insurance_to_id.get(primary_insurance)
        MediLink_ConfigLoader.log("Primary insurance ID retrieved for '{}': {}".format(primary_insurance, insurance_id))

        # Use insurance ID to retrieve the payer ID(s) associated with the insurance
        payer_ids = []
        if insurance_id:
            for payer_id, payer_data in crosswalk.get('payer_id', {}).items():
                medisoft_ids = [str(id) for id in payer_data.get('medisoft_id', [])]
                # MediLink_ConfigLoader.log("Payer ID: {}, Medisoft IDs: {}".format(payer_id, medisoft_ids))
                if str(insurance_id) in medisoft_ids:
                    payer_ids.append(payer_id)
        if payer_ids:
            MediLink_ConfigLoader.log("Payer IDs retrieved for insurance '{}': {}".format(primary_insurance, payer_ids))
        else:
            MediLink_ConfigLoader.log("No payer IDs found for insurance '{}'".format(primary_insurance))
        
        # Find the suggested endpoint from the crosswalk based on the payer IDs
        suggested_endpoint = 'AVAILITY'  # Default endpoint if no matching payer IDs found
        if payer_ids:
            payer_id = payer_ids[0]  # Select the first payer ID
            suggested_endpoint = crosswalk['payer_id'].get(payer_id, {}).get('endpoint', 'AVAILITY')
            MediLink_ConfigLoader.log("Suggested endpoint for payer ID '{}': {}".format(payer_id, suggested_endpoint))
        else:
            MediLink_ConfigLoader.log("No suggested endpoint found for payer IDs: {}".format(payer_ids))

        # Enrich detailed patient data with additional information and suggested endpoint
        detailed_data = parsed_data.copy()  # Copy parsed_data to avoid modifying the original dictionary
        detailed_data.update({
            'file_path': file_path,
            'patient_id': parsed_data.get('CHART'),
            'surgery_date': parsed_data.get('DATE'),
            'patient_name': ' '.join([parsed_data.get(key, '') for key in ['FIRST', 'MIDDLE', 'LAST']]),
            'amount': parsed_data.get('AMOUNT'),
            'primary_insurance': primary_insurance,
            'suggested_endpoint': suggested_endpoint
        })
        detailed_patient_data.append(detailed_data)

    # Return only the enriched detailed patient data, eliminating the need for a separate summary list
    return detailed_patient_data

def organize_patient_data_by_endpoint(detailed_patient_data):
    """
    Organizes detailed patient data by their confirmed endpoints.
    This simplifies processing and conversion per endpoint basis, ensuring that claims are generated and submitted
    according to the endpoint-specific requirements.

    :param detailed_patient_data: A list of dictionaries, each containing detailed patient data including confirmed endpoint.
    :return: A dictionary with endpoints as keys and lists of detailed patient data as values for processing.
    """
    organized = {}
    for data in detailed_patient_data:
        # Retrieve confirmed endpoint from each patient's data
        endpoint = data['confirmed_endpoint'] if 'confirmed_endpoint' in data else data['suggested_endpoint']
        # Initialize a list for the endpoint if it doesn't exist
        if endpoint not in organized:
            organized[endpoint] = []
        organized[endpoint].append(data)
    return organized

def check_for_new_remittances(config):
    print("\nChecking for new files across all endpoints...")
    endpoints = config['MediLink_Config']['endpoints']
    processed_endpoints = []
    
    if isinstance(endpoints, dict): # BUG This check can probably be removed later.
        for endpoint_key, endpoint_info in tqdm(endpoints.items(), desc="Processing endpoints"):
            if 'remote_directory_down' in endpoint_info:  # Check if the 'remote_directory_down' key exists
                #print("Processing endpoint: ", endpoint_info['name']) 
                # BUG (Debug and verbosity removal) this is really for debug only. Positive statements can be muted.
                try:
                    ERA_path = MediLink_Down.main(desired_endpoint=endpoint_key)
                    processed_endpoints.append((endpoint_info['name'], ERA_path))
                    MediLink_ConfigLoader.log("Results for {} saved to: {}".format(endpoint_info['name'], ERA_path))
                    # TODO (Low SFTP - Download side) This needs to check to see if this actually worked maybe winscplog before saying it completed successfully 
                    # Check if there is commonality with the upload side so we can use the same validation function.
                except Exception as e:
                    print("An error occurred while checking remittances for {}: {}".format(endpoint_info['name'], e))
            else:
                MediLink_ConfigLoader.log("Skipping endpoint '{}' as it does not have 'remote_directory_down' configured.".format(endpoint_info['name']))
    else:
        print("Error: Endpoint config is not a 'dictionary' as expected.")
    # Check if all ERA paths are the same
    unique_era_paths = set(path for _, path in processed_endpoints)
    if len(unique_era_paths) == 1:
        common_era_path = unique_era_paths.pop()  # Get the common ERA path
        endpoints_list = ", ".join(endpoint for endpoint, _ in processed_endpoints)
        print("\nProcessed Endpoints: {}".format(endpoints_list))
        print("File located at: {}\n".format(common_era_path))
        # TODO (MediPost) These prints will eventually be logs when MediPost is made.
        
    else:
        if processed_endpoints:
            print("\nProcessed Endpoints:")
            for endpoint, path in processed_endpoints:
                print("Endpoint: {}, ERA Path: {}".format(endpoint, path))
        else:
            print("No endpoints were processed.")

def user_decision_on_suggestions(detailed_patient_data, config):
    """
    Presents the user with all patient summaries and suggested endpoints,
    then asks for confirmation to proceed with all or specify adjustments manually.
    
    BUG (Med suggested_endpoint) The display summary suggested_endpoint key isn't updating per the user's decision 
    although the user decision is persisting. Possibly consider making the current/suggested/confirmed endpoint 
    part of a class that the user can interact with via these menus. Probably better handling that way.
    """
    # Display summaries of patient details and endpoints.
    MediLink_UI.display_patient_summaries(detailed_patient_data)

    # Ask the user if they want to proceed with all suggested endpoints.
    proceed = MediLink_UI.ask_for_proceeding_with_endpoints()

    # If the user agrees to proceed with all suggested endpoints, confirm them.
    if proceed:
        return confirm_all_suggested_endpoints(detailed_patient_data)
    # Otherwise, allow the user to adjust the endpoints manually.
    else:
        return select_and_adjust_files(detailed_patient_data, config)
    
def confirm_all_suggested_endpoints(detailed_patient_data):
    """
    Confirms all suggested endpoints for each patient's detailed data.
    """
    for data in detailed_patient_data:
        if 'confirmed_endpoint' not in data:
            data['confirmed_endpoint'] = data['suggested_endpoint']
    return detailed_patient_data

def select_and_adjust_files(detailed_patient_data, config):
    """
    Allows users to select patients and adjust their endpoints by interfacing with UI functions.
    
    BUG (Med suggested_endpoint) After the user is done making their selection (probably via a class?), 
    Then suggested_endpoint should update to persist the user selection as priority over its original suggestion. 
    Which means the crosswalk should persist the change in the endpoint as well.
    """
    # Display options for patients
    MediLink_UI.display_patient_options(detailed_patient_data)

    # Get user-selected indices for adjustment
    selected_indices = MediLink_UI.get_selected_indices(len(detailed_patient_data))
    
    # Get an ordered list of endpoint keys
    endpoint_keys = list(config['MediLink_Config']['endpoints'].keys())

    # Iterate over each selected index and process endpoint changes
    for i in selected_indices:
        data = detailed_patient_data[i]
        MediLink_UI.display_patient_for_adjustment(data['patient_name'], data.get('suggested_endpoint', 'N/A'))
        
        endpoint_change = MediLink_UI.get_endpoint_decision()
        if endpoint_change == 'y':
            MediLink_UI.display_endpoint_options(config['MediLink_Config']['endpoints'])
            endpoint_index = int(MediLink_UI.get_new_endpoint_choice()) - 1  # Adjusting for zero-based index
            
            if 0 <= endpoint_index < len(endpoint_keys):
                selected_endpoint_key = endpoint_keys[endpoint_index]
                data['confirmed_endpoint'] = selected_endpoint_key
                print("Endpoint changed to {0} for patient {1}.".format(config['MediLink_Config']['endpoints'][selected_endpoint_key]['name'], data['patient_name']))
                # BUG (Med, Crosswalk & suggested_endpoint) Probably update crosswalk and suggested endpoint here???
            else:
                print("Invalid selection. Keeping the suggested endpoint.")
        else:
            data['confirmed_endpoint'] = data.get('suggested_endpoint', 'N/A')

    return detailed_patient_data

def main_menu():
    """
    Initializes the main menu loop and handles the overall program flow,
    including loading configurations and managing user input for menu selections.
    """
    # Load configuration settings and display the initial welcome message.
    config, crosswalk = MediLink_ConfigLoader.load_configuration() 
    # BUG (Low, Config) does this need an argument? Not sure.
    
    # TODO (Test Mode) Add here a check in config.json for key "MediLink_Config": { "TestMode": true, ...}. If it is true,
    # prompt the user to say that MediLink is in Test Mode and ask if the user wants to stay in test mode? 
    # Then put placeholder text for now because I don't know what the logic should be.
    
    # Display Welcome Message
    MediLink_UI.display_welcome()

    # Normalize the directory path for file operations.
    directory_path = os.path.normpath(config['MediLink_Config']['inputFilePath'])

    # Detect new files and collect detailed patient data if available.
    new_files, detailed_patient_data = detect_and_display_file_summaries(directory_path, config, crosswalk)

    while True:
        # Define the menu options. Base options include checking remittances and exiting the program.
        options = ["Check for new remittances", "Exit"]
        # If new files are detected, add the option to submit claims.
        if new_files:
            options.insert(1, "Submit claims")

        # Display the dynamically adjusted menu options.
        MediLink_UI.display_menu(options)
        # Retrieve user choice and handle it.
        choice = MediLink_UI.get_user_choice()

        if choice == '1':
            # Handle remittance checking.
            check_for_new_remittances(config)
        elif choice == '2' and new_files:
            # Handle the claims submission flow if new files are present.
            handle_submission(detailed_patient_data, config)
        elif choice == '3' or (choice == '2' and not new_files):
            # Exit the program if the user chooses to exit or if no new files are present.
            MediLink_UI.display_exit_message()
            break
        else:
            # Display an error message if the user's choice does not match any valid option.
            MediLink_UI.display_invalid_choice()

def handle_submission(detailed_patient_data, config):
    """
    Handles the submission process for claims based on detailed patient data.
    This function orchestrates the flow from user decision on endpoint suggestions to the actual submission of claims.
    """
    # Initiate user interaction to confirm or adjust suggested endpoints.
    adjusted_data = user_decision_on_suggestions(detailed_patient_data, config)
    # Confirm all remaining suggested endpoints.
    confirmed_data = confirm_all_suggested_endpoints(adjusted_data)
    if confirmed_data:  # Proceed if there are confirmed data entries.
        # Organize data by confirmed endpoints for submission.
        organized_data = organize_patient_data_by_endpoint(confirmed_data)
        # Confirm transmission with the user and check for internet connectivity.
        if MediLink_Up.confirm_transmission(organized_data):
            if MediLink_Up.check_internet_connection():
                # Submit claims if internet connectivity is confirmed.
                _ = MediLink_Up.submit_claims(organized_data, config)
                # TODO submit_claims will have a receipt return in the future.
            else:
                # Notify the user of an internet connection error.
                print("Internet connection error. Please ensure you're connected and try again.")
        else:
            # Notify the user if the submission is cancelled.
            print("Submission cancelled. No changes were made.")

if __name__ == "__main__":
    main_menu()