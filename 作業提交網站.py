import streamlit as st
import requests
import concurrent.futures

FLASK_URL = 'https://homework-suny.onrender.com'

st.sidebar.title("作業提交網站")

st.sidebar.subheader("上傳檔案")

uploaded_file = st.sidebar.file_uploader("選擇欲上傳的檔案")

def upload_to_flask(file_name, file_content, file_type):
    files = {'file': (file_name, file_content, file_type)}
    response = requests.post(f"{FLASK_URL}/upload", files=files)
    return response.status_code == 200

if uploaded_file is not None:
     
    file_name = uploaded_file.name
    file_type = uploaded_file.type

    # 读取文件内容并保留以供上传
    file_content = uploaded_file.read()

    if file_name.endswith('.py'):
        st.write("**檔案內容預覽：**")
        st.code(file_content.decode('utf-8'), language='python')
    elif file_type.startswith('image/'):
        st.image(file_content, caption=file_name, use_column_width=True)
    else:
        st.warning("檔案類型不支援預覽")

    if st.sidebar.button("提交檔案"):
        
        status_text = st.sidebar.text("正在上傳檔案...")
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(upload_to_flask, file_name, file_content, file_type)
            success = future.result()

            status_text.empty()
        
            if success:
                st.sidebar.success("檔案上傳成功")
            else:
                st.sidebar.error("檔案上傳失敗")
