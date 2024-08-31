from flask import Flask, render_template, jsonify, request
import os
import json

app = Flask(__name__)  #建構flask app
app.static_folder = 'static'  #存儲靜態文件(例如CSS)的資料夾名稱

feedback_list = []

@app.route('/')   #當訪問app URL時執行以下程式
def index():
    return render_template('index.html')  #UI介面

@app.route('/questions.json')  #當flask app讀取到questions.json後執行
def get_questions():
    json_path = os.path.join(app.root_path, 'data', 'questions.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    return jsonify(questions)

@app.route('/save-feedback', methods=['POST'])
def save_feedback():
    global feedback_list 

    feedback_data = request.json
    feedback_file_path = os.path.join(app.root_path, 'data', 'feedback.json')

    formatted_feedback = {
        "問題": feedback_data["question"]
    }

    answers = feedback_data.get("answers", [])
    for i, ans in enumerate(answers, 1):
        formatted_feedback[f"答案{i}"] = {
            "內容": ans.get("text", ""),
            "分數": ans.get("score", 0),
            "評分者": ans.get("rater", "")
        }

    formatted_feedback["最佳答案"] = feedback_data.get("best_answer", "")

    feedback_list.append(formatted_feedback)

    with open(feedback_file_path, 'w', encoding='utf-8') as feedback_file:
        json.dump(feedback_list, feedback_file, ensure_ascii=False, indent=4)

    return jsonify(formatted_feedback)

@app.route('/clear-feedback', methods=['POST'])
def clear_feedback():
    global feedback_list
    feedback_list = [] 

    feedback_file_path = os.path.join(app.root_path, 'data', 'feedback.json')
    with open(feedback_file_path, 'w', encoding='utf-8') as feedback_file:
        feedback_file.write('[]')  

    return "Feedback cleared successfully!"

if __name__ == '__main__':
    app.run(debug=True)
