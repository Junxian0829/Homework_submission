import os
import streamlit as st

st.sidebar.title("作業提交網站")

st.sidebar.subheader("上傳檔案")

uploaded_file = st.sidebar.file_uploader("選擇欲上傳的檔案")

if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.read())
    
    st.sidebar.success("檔案上傳成功")
    st.write(f"文件保存路径: {file_path}")



