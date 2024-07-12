import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def get_google_photos_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=8080)  # Specify port 8080 here
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('photoslibrary', 'v1', credentials=creds)

def fetch_photos():
    service = get_google_photos_service()
    
    results = service.mediaItems().list(pageSize=100).execute()
    items = results.get('mediaItems', [])

    photo_data = []
    for item in items:
        photo_data.append({
            'filename': item['filename'],
            'baseUrl': item['baseUrl'],
            'mimeType': item['mimeType']
        })

    with open('photo_data.json', 'w') as f:
        json.dump(photo_data, f)

    print(f"Fetched and saved data for {len(photo_data)} photos.")

if __name__ == '__main__':
    fetch_photos()