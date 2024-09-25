import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_token_path(api_service_name, api_version, token_dir, prefix):
    """Generates the token path based on API name, version, and prefix."""
    return os.path.join(token_dir,f'token_{api_service_name}_{api_version}{prefix}.json')

def load_credentials(token_path, scopes):
    """Loads credentials from the token file."""
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)

        if creds and creds.valid:
            return creds
    return None

def save_credentials(creds, token_path):
    """Saves the credentials to a token file"""
    with open(token_path,'w') as token_file:
        token_file.write(creds.to_json())

def create_service(client_secret_file, api_name, api_version, *scopes, prefix=''):
    """Creates the Google API service, managing OAuth 2.0 authentication and token handling."""
    working_dir = os.getcwd() #Get the current working directory
    token_dir = os.path.join(working_dir,"token_files") # Create a directory to store the token files

    # Create token directory if it doesn't exist
    if not os.path.exists(token_dir):
        os.makedirs(token_dir)

    # Get the token path
    token_path = get_token_path(api_name, api_version, token_dir, prefix)

    # Load credentials or initiate OAuth flow if necessary
    creds = load_credentials(token_path, scopes[0]) # scopes[0] is the actual list of scopes

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_file,scopes[0])
        creds = flow.run_local_server(port=0)
        save_credentials(creds,token_path)
    elif creds.expired and creds.refresh_token:
        creds.refresh(Request())
        save_credentials(creds, token_path)

    # Build and return the service
    try:
        service = build(api_name, api_version, credentials=creds, static_discovery=False)
        print(f'{api_name} {api_version} service created successfully')
        return service
    except Exception as e:
        print(f'Failed to create service instance for {api_name}:{e}')
        if os.path.exists(token_path):
            os.remove(token_path)
        return None 