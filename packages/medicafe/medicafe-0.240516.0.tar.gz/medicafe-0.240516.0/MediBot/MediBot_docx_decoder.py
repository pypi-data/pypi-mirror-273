"""
Using docx-utils 0.1.3,

This script parses a .docx file containing a table of patient information and extracts
relevant data into a dictionary. Each row in the table corresponds to a new patient, 
and the data from each cell is parsed into specific variables. The resulting dictionary 
uses the 'Patient ID Number' as keys and lists containing 'Diagnosis Code', 
'Left or Right Eye', and 'Femto yes or no' as values.

Functions:
    parse_docx(filepath): Reads the .docx file and constructs the patient data dictionary.
    parse_patient_id(text): Extracts the Patient ID Number from the text.
    parse_diagnosis_code(text): Extracts the Diagnosis Code from the text.
    parse_left_or_right_eye(text): Extracts the eye information (Left or Right) from the text.
    parse_femto_yes_or_no(text): Extracts the Femto information (yes or no) from the text.
"""

from docx import Document

def parse_docx(filepath):
    # Open the .docx file
    doc = Document(filepath)
    
    # Initialize the dictionary to store data
    patient_data = {}
    
    # Assuming the first table contains the required data
    table = doc.tables[0]
    
    # Iterate over the rows in the table
    for row in table.rows[1:]:  # Skip header row if it exists
        cells = row.cells
        
        # Extract and parse data from each cell
        patient_id = parse_patient_id(cells[0].text.strip())
        diagnosis_code = parse_diagnosis_code(cells[1].text.strip())
        left_or_right_eye = parse_left_or_right_eye(cells[2].text.strip())
        femto_yes_or_no = parse_femto_yes_or_no(cells[3].text.strip())
        
        # Construct the dictionary entry
        patient_data[patient_id] = [diagnosis_code, left_or_right_eye, femto_yes_or_no]
    
    return patient_data

def parse_patient_id(text):
    # Implement parsing logic for Patient ID Number
    # Example: Assume the ID is the first part of the text, separated by a space or newline
    return text.split()[0]

def parse_diagnosis_code(text):
    # Implement parsing logic for Diagnosis Code
    # Example: Extract the code from a known pattern or location in the text
    return text.split(':')[1].strip() if ':' in text else text

def parse_left_or_right_eye(text):
    # Implement parsing logic for Left or Right Eye
    # Example: Assume the text contains 'Left' or 'Right' and extract it
    if 'Left' in text:
        return 'Left'
    elif 'Right' in text:
        return 'Right'
    else:
        return 'Unknown'

def parse_femto_yes_or_no(text):
    # Implement parsing logic for Femto yes or no
    # Example: Check for presence of keywords 'yes' or 'no'
    if 'yes' in text.lower():
        return 'Yes'
    elif 'no' in text.lower():
        return 'No'
    else:
        return 'Unknown'

# Placeholder function call (replace 'path_to_docx' with the actual file path)
filepath = 'path_to_docx'
patient_data_dict = parse_docx(filepath)

# Print the resulting dictionary
print(patient_data_dict)
