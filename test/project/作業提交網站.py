import streamlit as st
import requests

FLASK_URL = 'http://127.0.0.1:5000'

st.sidebar.title("作業提交網站")

st.sidebar.subheader("上傳檔案")

uploaded_file = st.sidebar.file_uploader("選擇欲上傳的檔案")

if uploaded_file is not None:
    files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post(f"{FLASK_URL}/upload", files=files)
    
    if response.status_code == 200:
        st.sidebar.success("檔案上傳成功")
    else:
        st.sidebar.error("檔案上傳失敗")



