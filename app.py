import os
import threading
from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

app = Flask(__name__)

UPLOAD_FOLDER = '1TD0x7j_7yYpf4NqhFaUGxsdSz0ZkzKzF'
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '/etc/secrets/credentials.json'

def upload_file_to_drive(local_path, filename, content_type):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': filename, 'parents': [UPLOAD_FOLDER]}
    media = MediaFileUpload(local_path, mimetype=content_type)

    drive_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return drive_file.get('id')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = file.filename
    content_type = file.content_type

    temp_local_path = os.path.join("/tmp", filename)

    # 保存文件前打印文件内容或大小
    file_content = file.read()
    print(f"Received file: {filename}, size: {len(file_content)} bytes")
    
    # 保存文件
    with open(temp_local_path, 'wb') as f:
        f.write(file_content)

    # 确认文件已正确保存
    saved_size = os.path.getsize(temp_local_path)
    print(f"File saved: {temp_local_path}, size: {saved_size} bytes")

    # 上传到 Google Drive
    file_id = upload_file_to_drive(temp_local_path, filename, content_type)
    print(f"File uploaded with ID: {file_id}")

    # 删除本地临时文件
    os.remove(temp_local_path)

    return jsonify({"status": "File uploaded successfully", "file_id": file_id}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)
