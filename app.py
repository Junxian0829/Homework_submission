import os
import io
from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credential.json'

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    service = get_drive_service()
    file_metadata = {'name': file.filename}
    media = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype=file.content_type)
    drive_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return jsonify({"status": "File uploaded successfully!", "file_id": drive_file.get('id')}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)
