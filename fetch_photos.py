from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
import os

# Set up the flow object
flow = Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/photoslibrary.readonly']
)

# Generate the authorization URL
auth_url, _ = flow.authorization_url(prompt='consent')

print(f"Please visit this URL to authorize the application: {auth_url}")

# After the user grants permission, you'll get a code. Enter it here:
code = input("Enter the authorization code: ")

# Exchange the code for credentials
flow.fetch_token(code=code)

# Get the credentials
credentials = flow.credentials

# Save the credentials for future use
with open('token.json', 'w') as token_file:
    token_file.write(credentials.to_json())

# Build the service
service = build('photoslibrary', 'v1', credentials=credentials)

# Fetch the photos
results = service.mediaItems().list(pageSize=100).execute()
items = results.get('mediaItems', [])

# Process and save the photo data
photo_data = []
for item in items:
    photo_data.append({
        'filename': item['filename'],
        'baseUrl': item['baseUrl'],
        'mimeType': item['mimeType']
    })

# Save the photo data to a JSON file
with open('photo_data.json', 'w') as f:
    json.dump(photo_data, f)

print(f"Fetched and saved data for {len(photo_data)} photos.")