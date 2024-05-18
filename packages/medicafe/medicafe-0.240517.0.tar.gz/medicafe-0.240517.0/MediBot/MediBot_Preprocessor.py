import os
import re
from collections import OrderedDict # so that the field_mapping stays in order.
import re
import sys
import argparse
import MediBot_Crosswalk_Library

# Add parent directory of the project to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_dir)

try: 
    from MediLink import MediLink_ConfigLoader
except ImportError:
    import MediLink_ConfigLoader

try:
    import MediBot_Preprocessor_lib
except ImportError:
    from MediBot import MediBot_Preprocessor_lib

"""
Preprocessing Enhancements
- [X] Preprocess Insurance Policy Numbers and Group Numbers to replace '-' with ''.
- [X] De-duplicate entries in the CSV and only entering the px once even if they show up twice in the file.
- [ ] Implement dynamic field combination in CSV pre-processing for flexibility with various CSV formats.
- [ ] Enhance SSN cleaning logic to handle more variations of sensitive data masking.
- [ ] Optimize script startup and CSV loading to reduce initial latency.

Data Integrity and Validation
- [ ] Conduct a thorough CSV integrity check before processing to flag potential issues upfront.
- [ ] Implement a mechanism to confirm the accuracy of entered data, potentially through a verification step or summary report.
- [ ] Explore the possibility of integrating direct database queries for existing patient checks to streamline the process.
- [ ] Automate the replacement of spaces with underscores ('_') in last names for Medicare entries.
- [ ] Enhance CSV integrity checks to identify and report potential issues with data format, especially concerning insurance policy numbers and special character handling.

Known Issues and Bugs
- [ ] Address the handling of '.' and other special characters that may disrupt parsing, especially under Windows XP.
- [ ] Investigate the issue with Excel modifying long policy numbers in the CSV and provide guidance or a workaround.

Future Work
- [X] Check for PatientID number in La Forma Z to link back to Carol's table for mapping Medisoft insurance name to payerID and payer name and address.
- [X] Check for PatientID to Medisoft custom insurance name mapping in MAPAT.
- [X] Middle Names should all be single letters. Make sure it gets truncated before submitting.
- [ ] Consolidate data from multiple sources (Provider_Notes.csv, Surgery_Schedule.csv, and Carols_CSV.csv) into a single table with Patient ID as the key, ensuring all data elements are aligned and duplicate entries are minimized.
- [ ] Implement logic to verify and match Patient IDs across different files to ensure data integrity before consolidation. (Catching errors between source data)
- [ ] Optimize the preprocessing of surgery dates and diagnosis codes for use in patient billing and scheduling systems.
- [ ] Read Surgery Schedule doc and parse out a Patient ID : Diagnosis Code table.
- [ ] The Minutes & Cancellation data with logic to consolidate into one table in memory.
- [ ] Dynamically list the endpoint for a new Payer ID via API or user interaction to update the crosswalk.json efficiently.
- [ ] Pull listed addresses of insurance from the CSV. (Not really necessary)
- [ ] Retroactively learn Medisoft insurance name and payerID from the provided data sources.

Development Roadmap for crosswalk_update():
- [X] Automation required for updating the crosswalk.json when new Medisoft insurance is discovered.
- [X] New Medisoft insurances are identified based on the payer ID number.
- [X] Check the existence of the payer ID in crosswalk.json under existing endpoints.
- [X] Facilitate grouping of IDs for insurances like CIGNA with multiple addresses but few payer IDs.
- [X] Retroactive learning based on selected insurances in Medisoft 
- [ ] Prompt user via endpoint APIs to add new payer ID to an endpoint if it does not exist.
- [ ] Retain payer IDs without Insurance ID for future assignments.
- [ ] Check for free payer IDs and determine the appropriate endpoint for assignment.
- [ ] Present unrecognized payer IDs with Carol's Insurance Name to users for assignment to Insurance ID. (Try API Call)
- [ ] Integrate API checks to verify payer ID availability and related information.
- [ ] Implement "Fax/Mail or Other" endpoint for unavailable payer IDs.
- [ ] Present user with a list of top insurances for selection based on fuzzy search scores.
- [ ] Establish payer ID to insurance ID relationship based on user selection.
- [ ] Implicitly establish payer ID to endpoint mapping based on user selection.
- [ ] Implement validation mechanisms to prevent incorrect mappings and ensure data integrity.
- [ ] Considerations for extracting insurance addresses (if necessary)
- [ ] Handle better the case where a payer_id doesn't exist (When Carol's CSV doesn't bring the Payer ID).
        Maybe ask the user what the payer ID is for that patient? I dont know.
- [ ] TODO (MED) Crosswalk (both initializing and updating) needs to pull AFTER the Preprocessor for Carol's CSV because
        all that data lives in-memory and then gets corrections or replacements before being used so we need 
        the post-correction data to be used to build and update the crosswalk.
"""
# Load configuration
# Should this also take args? Path for ./MediLink needed to be added for this to resolve
config, crosswalk = MediLink_ConfigLoader.load_configuration()

# CSV Preprocessor built for Carol
def preprocess_csv_data(csv_data, crosswalk):
    try:
        # Add the "Ins1 Insurance ID" column to the CSV data.
        # This initializes the column with empty values for each row.
        MediLink_ConfigLoader.log("CSV Pre-processor: Adding 'Ins1 Insurance ID' column to the CSV data...", level="INFO")
        MediBot_Preprocessor_lib.add_insurance_id_column(csv_data)
        
        # Filter out rows without a Patient ID and rows where the Primary Insurance
        # is 'AETNA', 'AETNA MEDICARE', or 'HUMANA MED HMO'.
        MediLink_ConfigLoader.log("CSV Pre-processor: Filtering out missing Patient IDs and 'AETNA', 'AETNA MEDICARE', or 'HUMANA MED HMO'...", level="INFO")
        MediBot_Preprocessor_lib.filter_rows(csv_data)
        
        # Convert 'Surgery Date' from string format to datetime objects for sorting purposes.
        # Sort the patients by 'Surgery Date' and then by 'Patient Last' name alphabetically.
        # Deduplicate patient records based on Patient ID, keeping the entry with the earliest surgery date.
        # Update the CSV data to include only unique patient records.
        # Re-sort the CSV data after deduplication to ensure the correct order.
        MediLink_ConfigLoader.log("CSV Pre-processor: Sorting and de-duplicating patient records...", level="INFO")
        MediBot_Preprocessor_lib.convert_surgery_date(csv_data)
        MediBot_Preprocessor_lib.sort_and_deduplicate(csv_data)
        
        # Convert 'Surgery Date' back to string format if needed for further processing.
        # Combine 'Patient First', 'Patient Middle', and 'Patient Last' into a single 'Patient Name' field.
        # Combine 'Patient Address1' and 'Patient Address2' into a single 'Patient Street' field.
        MediLink_ConfigLoader.log("CSV Pre-processor: Constructing Patient Name and Address for Medisoft...", level="INFO")
        MediBot_Preprocessor_lib.combine_fields(csv_data)
        
        # Retrieve replacement values from the crosswalk.
        # Iterate over each key-value pair in the replacements dictionary and replace the old value
        # with the new value in the corresponding fields of each row.
        MediLink_ConfigLoader.log("CSV Pre-processor: Applying mandatory replacements per Crosswalk...", level="INFO")
        MediBot_Preprocessor_lib.apply_replacements(csv_data, crosswalk)
        
        # Update the "Ins1 Insurance ID" column based on the crosswalk and the "Ins1 Payer ID" column for each row.
        # If the Payer ID is not found in the crosswalk, create a placeholder entry in the crosswalk and mark the row for review.
        MediLink_ConfigLoader.log("CSV Pre-processor: Populating 'Ins1 Insurance ID' based on Crosswalk...", level="INFO")
        MediBot_Preprocessor_lib.update_insurance_ids(csv_data, crosswalk)
    
    except Exception as e:
        message = "An error occurred while pre-processing CSV data. Please repair the CSV directly and try again: {}".format(e)
        MediLink_ConfigLoader.log(message, level="ERROR")
        print(message)

def check_existing_patients(selected_patient_ids, MAPAT_MED_PATH):
    existing_patients = []
    patients_to_process = list(selected_patient_ids)  # Clone the selected patient IDs list

    try:
        with open(MAPAT_MED_PATH, 'r') as file:
            next(file)  # Skip header row
            for line in file:
                if line.startswith("0"): # 1 is a flag for a deleted record so it would need to be re-entered.
                    patient_id = line[194:202].strip()  # Extract Patient ID (Columns 195-202)
                    patient_name = line[9:39].strip()  # Extract Patient Name (Columns 10-39)
                    
                    if patient_id in selected_patient_ids:
                        existing_patients.append((patient_id, patient_name))
                        # Remove all occurrences of this patient_id from patients_to_process as a filter rather than .remove because 
                        # then it only makes one pass and removes the first instance.
    except FileNotFoundError:
        # Handle the case where MAPAT_MED_PATH is not found
        print("MAPAT.med was not found at location indicated in config file.")
        print("Skipping existing patient check and continuing...")
        
    # Filter out all instances of existing patient IDs
    patients_to_process = [id for id in patients_to_process if id not in [patient[0] for patient in existing_patients]]
    
    return existing_patients, patients_to_process

def intake_scan(csv_headers, field_mapping):
    identified_fields = OrderedDict()
    missing_fields_warnings = []
    required_fields = config["required_fields"]
    
    # MediLink_ConfigLoader.log("Intake Scan - Field Mapping: {}".format(field_mapping))
    # MediLink_ConfigLoader.log("Intake Scan - CSV Headers: {}".format(csv_headers))
    
    # Iterate over the Medisoft fields defined in field_mapping
    for medisoft_field in field_mapping.keys():
        for pattern in field_mapping[medisoft_field]:
            matched_headers = [header for header in csv_headers if re.search(pattern, header, re.IGNORECASE)]
            if matched_headers:
                # Assuming the first matched header is the desired one
                identified_fields[matched_headers[0]] = medisoft_field
                # MediLink_ConfigLoader.log("Found Header: {}".format(identified_fields[matched_headers[0]]))
                break
        else:
            # Check if the missing field is a required field before appending the warning
            if medisoft_field in required_fields:
                missing_fields_warnings.append("WARNING: No matching CSV header found for Medisoft field '{0}'".format(medisoft_field))
   
    # CSV Integrity Checks
    # Check for blank or partially blank CSV
    if len(csv_headers) == 0 or all(header == "" for header in csv_headers):
        missing_fields_warnings.append("WARNING: The CSV appears to be blank or contains only headers without data.")

    # Display the identified fields and missing fields warnings
    #MediLink_ConfigLoader.log("The following Medisoft fields have been identified in the CSV:")
    #for header, medisoft_field in identified_fields.items():
    #    MediLink_ConfigLoader.log("{} (CSV header: {})".format(medisoft_field, header))

    # This section interprets the information from identified_fields and decides if there are significant issues.
    # e.g. If the 'Street' value:key is 'Address', then any warnings about City, State, Zip can be ignored.
    for header, field in identified_fields.items():
        # Insurance Policy Numbers should be all alphanumeric with no other characters. 
        if 'Insurance Policy Number' in field:
            policy_number = identified_fields.get(header)
            if not bool(re.match("^[a-zA-Z0-9]*$", policy_number)):
                missing_fields_warnings.append("WARNING: Insurance Policy Number '{}' contains invalid characters.".format(policy_number))
        # Additional checks can be added as needed for other fields
    
    if missing_fields_warnings:
        MediLink_ConfigLoader.log("\nSome required fields could not be matched:")
        for warning in missing_fields_warnings:
            MediLink_ConfigLoader.log(warning)

    return identified_fields

def main():
    parser = argparse.ArgumentParser(description='Run MediLink Data Management Tasks')
    parser.add_argument('--update-crosswalk', action='store_true',
                        help='Run the crosswalk update independently')
    parser.add_argument('--init-crosswalk', action='store_true',
                        help='Initialize the crosswalk using historical data from MAPAT and Carols CSV')
    parser.add_argument('--load-csv', action='store_true',
                        help='Load and process CSV data')
    parser.add_argument('--preprocess-csv', action='store_true',
                        help='Preprocess CSV data based on specific rules')
    parser.add_argument('--open-csv', action='store_true',
                        help='Open CSV for manual editing')

    args = parser.parse_args()

    config, crosswalk = MediLink_ConfigLoader.load_configuration()
    
    # If no arguments provided, print usage instructions
    if not any(vars(args).values()):
        parser.print_help()
        return

    if args.update_crosswalk:
        print("Updating the crosswalk...")
        MediBot_Crosswalk_Library.crosswalk_update(config, crosswalk)

    if args.init_crosswalk:
        MediBot_Crosswalk_Library.initialize_crosswalk_from_mapat()

    if args.load_csv:
        print("Loading CSV data...")
        csv_data = MediBot_Preprocessor_lib.load_csv_data(config['CSV_FILE_PATH'])
        print("Loaded {} records from the CSV.".format(len(csv_data)))

    if args.preprocess_csv:
        if 'csv_data' in locals():
            print("Preprocessing CSV data...")
            preprocess_csv_data(csv_data, crosswalk)
        else:
            print("Error: CSV data needs to be loaded before preprocessing. Use --load-csv.")
    
    if args.open_csv:
        print("Opening CSV for editing...")
        MediBot_Preprocessor_lib.open_csv_for_editing(config['CSV_FILE_PATH'])

if __name__ == '__main__':
    main()