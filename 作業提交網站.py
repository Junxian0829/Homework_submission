import streamlit as st
import requests
import concurrent.futures

FLASK_URL = 'https://homework-suny.onrender.com'

st.sidebar.title("作業提交網站")

st.sidebar.subheader("上傳檔案")

uploaded_file = st.sidebar.file_uploader("選擇欲上傳的檔案")

def upload_to_flask(file):
    files = {'file': (file.name, file, file.type)}
    response = requests.post(f"{FLASK_URL}/upload", files=files)
    return response.status_code == 200

if uploaded_file is not None:
     
    file_name = uploaded_file.name
    file_type = uploaded_file.type

    if file_name.endswith('.py'):

        file_content = uploaded_file.read().decode('utf-8')
        st.write("**檔案內容預覽：**")
        st.code(file_content, language='python')
    
    else:
        st.warning("請上傳 Python 檔案（.py）以查看預覽")

    status_text = st.sidebar.text("正在上傳檔案...")
        
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(upload_to_flask, uploaded_file)
        success = future.result()

        status_text.empty()
        
        if success:
            st.sidebar.success("檔案上傳成功")
        else:
            st.sidebar.error("檔案上傳失敗")

    




