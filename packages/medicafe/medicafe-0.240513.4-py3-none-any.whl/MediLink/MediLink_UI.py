from datetime import datetime

"""
Development Tasks for User Interface (UI) Enhancement in MediSoft Claims Submittal (MediLink) Script:

- [ ] Streamline user interaction for endpoint selection and patient adjustments with automated endpoint validation.
- [ ] Strengthen error handling in file conversion, transmission, and user inputs with actionable user feedback.
- [ ] Expand logging levels and develop a user notification system for process milestones and errors.
- [ ] Focus workflow on patient details for endpoint adjustments, facilitating patient-centric file submissions.
- [ ] Implement internet connectivity checks with retry options for submissions and offer pause/resume capabilities.
- [ ] Include final review and confirmation steps before submission, allowing for endpoint adjustments per patient.
- [ ] TODO Need to resolve suggested endpoint issues/refresh/quasi-persist (this is partially implemented, careful)
- [ ] TODO Augment the menu for displaying the insurance type information before submittal.
"""

def display_welcome():
    print("\n" + "-" * 60)
    print("          *~^~*:    Welcome to MediLink!    :*~^~*")
    print("-" * 60 + "\n")

def display_menu(options):
    print("Menu Options:")
    for i, option in enumerate(options):
        print("{0}. {1}".format(i+1, option))

def get_user_choice():
    return input("Enter your choice: ").strip()

def display_exit_message():
    print("\nExiting MediLink.")

def display_invalid_choice():
    print("Invalid choice. Please select a valid option.")

def display_patient_options(detailed_patient_data):
    """
    Displays a list of patients with their current suggested endpoints, prompting for selections to adjust.
    """
    print("\nPlease select the patients to adjust by entering their numbers separated by commas\n(e.g., 1,3,5):")
    # Can disable this extra print for now because the px list would already be on-screen.
    #for i, data in enumerate(detailed_patient_data, start=1):
    #    patient_info = "{0} ({1}) - {2}".format(data['patient_name'], data['patient_id'], data['surgery_date'])
    #    endpoint = data.get('suggested_endpoint', 'N/A')
    #    print("{:<3}. {:<30} Current Endpoint: {}".format(i, patient_info, endpoint))

def get_selected_indices(patient_count):
    """
    Collects user input for selected indices to adjust endpoints.
    """
    selected_indices_input = input("> ")
    selected_indices = [int(index.strip()) - 1 for index in selected_indices_input.split(',') if index.strip().isdigit() and 0 <= int(index.strip()) - 1 < patient_count]
    return selected_indices

def display_patient_for_adjustment(patient_name, suggested_endpoint):
    """
    Displays the current endpoint for a selected patient and prompts for a change.
    """
    print("\n- {0} | Current Endpoint: {1}".format(patient_name, suggested_endpoint))

def get_endpoint_decision():
    """
    Asks the user if they want to change the endpoint.
    """
    return input("Change endpoint? (Y/N): ").strip().lower()

def display_endpoint_options(endpoints_config):
    """
    Displays the endpoint options to the user based on the provided mapping.

    Args:
        endpoints_config (dict): A dictionary mapping endpoint keys to their properties, 
                                 where each property includes a 'name' key for the user-friendly name.
                                 Example: {'Availity': {'name': 'Availity'}, 'OptumEDI': {'name': 'OptumEDI'}, ...}

    Returns:
        None
    """
    print("Select the new endpoint for the patient:")
    for index, (key, details) in enumerate(endpoints_config.items(), 1):
        print("{0}. {1}".format(index, details['name']))

def get_new_endpoint_choice():
    """
    Gets the user's choice for a new endpoint.
    """
    return input("Select desired endpoint (e.g. 1, 2): ").strip()

def display_patient_summaries(detailed_patient_data):
    """
    Displays summaries of all patients and their suggested endpoints.
    """
    print("\nSummary of patient details and suggested endpoint:")
    for index, summary in enumerate(detailed_patient_data, start=1):
        try:
            display_file_summary(index, summary)
        except KeyError as e:
            print("Summary at index {} is missing key: {}".format(index, e))

def ask_for_proceeding_with_endpoints():
    """
    Asks the user if they want to proceed with all suggested endpoints.
    """
    proceed = input("\nDo you want to proceed with all suggested endpoints? (Y/N): ").strip().lower()
    return proceed == 'y'

def display_file_summary(index, summary):
    # Ensure surgery_date is converted to a datetime object
    surgery_date = datetime.strptime(summary['surgery_date'], "%m-%d-%y")

    # Displays the summary of a file.
    print("{:02d}. {:5} (ID: {:<8}) {:20} {:15} Suggested Endpoint: {}".format(
        index,
        surgery_date.strftime("%m-%d"),
        summary['patient_id'],
        summary['patient_name'][:20],
        summary['primary_insurance'][:15],
        summary['suggested_endpoint'])
    )