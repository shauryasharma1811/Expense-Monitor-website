from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.google_integration.crypto import decrypt_token
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def get_google_sheets_service(encrypted_access_token: str, encrypted_refresh_token: str = None):
    """
    Builds an authorized Google Sheets Resource using decrypted credentials.
    Tokens are kept strictly server-side.
    """
    access_token = decrypt_token(encrypted_access_token) if encrypted_access_token else None
    refresh_token = decrypt_token(encrypted_refresh_token) if encrypted_refresh_token else None

    credentials = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id="placeholder_client_id.apps.googleusercontent.com",
        client_secret="placeholder_client_secret"
    )

    service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
    return service

def fetch_spreadsheet_rows(service, spreadsheet_id: str, range_name: str = "Sheet1!A:G") -> List[List[Any]]:
    """
    Reads rows from the given Google Spreadsheet range.
    """
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values
