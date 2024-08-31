import streamlit as st
import requests

st.sidebar.title("作業提交網站")

st.sidebar.subheader("上傳檔案")

uploaded_file = st.sidebar.file_uploader("選擇欲上傳的檔案")

if uploaded_file is not None:

    file_contents = uploaded_file.read()

    with open(f'uploads/{uploaded_file.name}', 'wb') as f:
        f.write(file_contents)

    st.success("檔案上傳成功")



