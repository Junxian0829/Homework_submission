import io
import threading
from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

app = Flask(__name__)

UPLOAD_FOLDER = '1TD0x7j_7yYpf4NqhFaUGxsdSz0ZkzKzF'
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '/etc/secrets/credentials.json'

def upload_file_to_drive(file_content, filename, content_type):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': filename, 'parents': [UPLOAD_FOLDER]}
    media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype=content_type)

    drive_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return drive_file.get('id')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_content = file.read()  # 确保文件内容完整读取
    filename = file.filename
    content_type = file.content_type

    # 打印内容长度进行调试
    print(f"Uploading file: {filename}, size: {len(file_content)} bytes, content type: {content_type}")

    def async_upload(content, fname, ctype):
        file_id = upload_file_to_drive(content, fname, ctype)
        print(f"File uploaded with ID: {file_id}")

    # 将文件内容传递给线程
    thread = threading.Thread(target=async_upload, args=(file_content, filename, content_type))
    thread.start()

    return jsonify({"status": "File upload started"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)
