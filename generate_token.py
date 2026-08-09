from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]

flow = InstalledAppFlow.from_client_secrets_file(
    "credentials/google_client.json",
    SCOPES
)

creds = flow.run_local_server(port=8080)

with open("token.json", "w") as token:
    token.write(creds.to_json())

print("token.json created successfully!")