import os
import threading
import subprocess
import psutil

def is_streamlit_running():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'streamlit' in proc.info['name']:
            return True
    return False

def start_streamlit():
    if not is_streamlit_running():
        streamlit_script = 'project/作業提交網站.py'
        subprocess.Popen(['streamlit', 'run', streamlit_script, '--server.headless', 'true'])
    else:
        print("Streamlit is already running.")

if __name__ == '__main__':

    streamlit_thread = threading.Thread(target=start_streamlit)
    streamlit_thread.start()

    from app import app
    app.run(port=5000, debug=True, threaded=True)
