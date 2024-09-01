from quart import Quart, request, jsonify
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

app = Quart(__name__)

UPLOAD_FOLDER = '1TD0x7j_7yYpf4NqhFaUGxsdSz0ZkzKzF'
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '/etc/secrets/credentials.json'

async def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

@app.route('/upload', methods=['POST'])
async def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    service = await get_drive_service()
    file_metadata = {
        'name': file.filename,
        'parents': [UPLOAD_FOLDER]
    }
    media = MediaIoBaseUpload(io.BytesIO(await file.read()), mimetype=file.content_type)
    drive_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return jsonify({"status": "File uploaded successfully!", "file_id": drive_file.get('id')}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True, use_reloader=False)
