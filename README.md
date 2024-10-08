# Google Projects

This project provides a set of services for interacting with Google APIs, including Google Sheets and Gmail. The API services facilitate various functionalities like sending emails, fetching spreadsheets, and more.

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

google_projects/ ├── api_services/ │ ├── api_calls/ # Your package code │ ├── tests/ # Your test cases │ ├── requirements.txt # List of dependencies │ ├── setup.py # Setup script │ └── .gitignore # Git ignore file ├── venv/ # Virtual environment directory

## Installation

Follow the steps below to set up the project locally:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/ayo-dev7/google_projects.git
    cd google_projects/api_services
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    **On Windows:**
    ```bash
    venv\Scripts\activate
    ```
    **On macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```

4. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Google Sheets Client**  
   To use the `GoogleSheetsClient`, instantiate it with the appropriate client secret file and scopes:
    ```python
    from api_services.api_calls.sheet_client import GoogleSheetsClient

    client = GoogleSheetsClient(client_secret_file='path/to/client_secret.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
    ```

2. **Gmail Client**  
   To send an email using the `GmailClient`:
    ```python
    from api_services.api_calls.gmail_client import GoogleGmailClient

    gmail_client = GoogleGmailClient(client_secret_file='path/to/client_secret.json', scopes=['https://www.googleapis.com/auth/gmail.send'])
    gmail_client.send_email(sender='you@example.com', to='recipient@example.com', subject='Subject Here', message_text='Email body here.')
    ```

## Running Tests

To run the tests for this project, ensure you are in the virtual environment and then execute:
```bash
pytest
```

## **Contributing**
Contributions are welcome! Please follow these steps to contribute:

- Fork the repository.
- Create a new branch (git checkout -b feature-branch).
- Make your changes and commit them (git commit -m 'Add some feature').
- Push to the branch (git push origin feature-branch).
- Open a pull request.

## **License**
This project is licensed under the MIT License. See the LICENSE file for details.






