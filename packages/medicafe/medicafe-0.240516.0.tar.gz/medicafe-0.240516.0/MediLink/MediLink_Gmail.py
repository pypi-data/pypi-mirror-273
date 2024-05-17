"""
This documentation outlines the current functionality and development insights of a Google Apps Script and associated 
client-side Python script designed to facilitate the automated retrieval of secured content from emails. The system 
enables users to extract links and one-time passwords (OTPs) from emails, initiating and managing secure email interactions 
without manual intervention.

**Current Functionality:**
1. **Google Apps Script (Server-side)**:
    - Handles HTTP GET requests, routing them based on the 'action' parameter to perform tasks like retrieving stored 
        OTPs, extracting links from emails, and retrieving email subjects for user selection.
    - Utilizes Gmail search queries to find relevant emails based on sender and date criteria, then extracts data like 
        subjects or specific links contained within these emails.
    - Supports interactive selection of emails via a web app, allowing users to choose an email from a list and extract 
        a specific link.
    - Employs properties service to store and retrieve data like links and OTPs securely.

2. **HTML Client (Server-side)**:
    - Provides a user interface for selecting emails from a list, triggered by server-side scripts.
    - Includes JavaScript to handle client-server communication and user interactions, such as selecting an email and 
        extracting a link.

3. **Python Script (Client-side)**:
    - Interfaces with the server-side web app to initiate processes like link retrieval.
    - Manages opening URLs in the user's browser, allowing for interaction with the web app directly from the client-side 
        environment.

**Future Work:**
- [ ] Consider disabling OTP triggers for now since we don't really use it for the present implementation. The phone solution works.
- [ ] Implement and troubleshoot the OTP extraction and validation system to fully automate the secured content retrieval process.
- [X] Gmail Server-side Authentication flow & Webapp build
- [X] Upgrade to handle multiple possible emails selection
- [ ] Augment to detect Surgery Schedule emails with doc attachments that don't require OTP.
- [X] Upgrade Gmail query to only get emails with the protected links.
- [ ] Something that goes here that I forgot.

**Technical Challenges and Solutions:**
1. **Authentication Limitations on XP Systems:**
    - **Challenge:** The XP operating system could not perform authentication natively outside a browser, and available 
        libraries were not capable of handling dynamic authentication.
    - **Solution:** We centralized all user interactions within an HTML page served by Google Apps Script, thereby 
        eliminating the need for complex client-side operations. The client-side script was simplified to merely opening URLs, reducing the complexity and potential for errors.

2. **Secure Data Handling:**
    - **Challenge:** Initially, handling sensitive data such as OTPs and integrating with O365 protected emails was complex 
        due to security requirements and the transient nature of such data. The solution had to accommodate the specific 
        security protocols of Microsoft's environment without direct interaction.
    - **Solution:** Utilizing Google Apps Script’s property service to store OTPs temporarily and securely. Additionally, 
        we addressed O365 integration by ensuring the browser handled email links directly, respecting Microsoft's security 
        constraints like x-frame options, thus maintaining functionality without compromising security.

3. **User Interaction and Workflow Streamlining:**
    - **Challenge:** Managing the workflow from email selection to secure content access required multiple steps that could 
        potentially confuse the user. The application also had to be efficient under low-bandwidth constraints, and initially, 
        XP could not download attachments directly, requiring manual user intervention.
    - **Solution:** The introduction of an interactive web app interface enabled users to select emails directly through a 
        user-friendly list, significantly simplifying the workflow and minimizing user errors. This method also streamlined 
        the process, making it suitable for low-bandwidth environments and circumventing the need for full email client loads.
"""
import sys
import subprocess
import webbrowser
from MediLink_ConfigLoader import log

def open_browser_with_executable(url, browser_path=None):
    """
    Opens a browser with the specified URL using a provided browser executable path or the default browser.
    """
    try:
        if browser_path:
            log("Attempting to open URL with provided executable: {} {}".format(browser_path, url))
            # Try to open the browser using subprocess.Popen
            process = subprocess.Popen([browser_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                log("Browser opened with provided executable path using subprocess.Popen.")
            else:
                log("Browser failed to open using subprocess.Popen. Return code: {}. Stderr: {}".format(process.returncode, stderr))
        else:
            # Fall back to the default browser if no specific path is provided
            log("No browser path provided. Attempting to open URL with default browser: {}".format(url))
            webbrowser.open(url)
            log("Default browser opened.")
    except Exception as e:
        log("Failed to open browser: {}".format(e))

def initiate_link_retrieval():
    """
    Opens the web application through a direct URL that includes the action parameter.
    """
    log("Initiating link retrieval process.")
    # Direct URL that includes the action parameter to load the HTML content directly
    url = "https://script.google.com/macros/s/AKfycbzlq8d32mDlLdtFxgL_zvLJernlGPB64ftyxyH8F1nNlr3P-VBH6Yd0NGa1pbBc5AozvQ/exec?action=get_link"
    try:
        browser_path = sys.argv[1] if len(sys.argv) > 1 else None
        open_browser_with_executable(url, browser_path)
    except Exception as e:
        log("Error during link retrieval initiation: {}".format(e))

if __name__ == "__main__":
    initiate_link_retrieval()