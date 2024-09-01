import os
import io
from flask import Flask, request, jsonify
from flask_async import Async
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

app = Flask(__name__)

UPLOAD_FOLDER = '1TD0x7j_7yYpf4NqhFaUGxsdSz0ZkzKzF'
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '/etc/secrets/credentials.json'

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

@async_app.route('/upload', methods=['POST'])
async def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_content = file.read()
    file_name = file.filename
    mime_type = file.content_type

    drive_service = await asyncio.get_event_loop().run_in_executor(None, get_drive_service)
    file_metadata = {'name': file_name, 'parents': [UPLOAD_FOLDER]}
    media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype=mime_type)
    drive_file = await asyncio.get_event_loop().run_in_executor(None, lambda: drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute())
    
    return jsonify({"status": "File uploaded successfully!", "file_id": drive_file.get('id')}), 200
    
if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)
