import os
import re
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from arithmetic import call_function
from notes_summary import generate_summary
from web_search import web_search
from reasoning import infer_reasoning

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_query(query):
    query = query.lower().strip()

    math_match = re.match(r"(\d+)\s*([\+\-\*/])\s*(\d+)", query)
    if math_match:
        a, operator, b = int(math_match.group(1)), math_match.group(2), int(math_match.group(3))
        op_map = {"+": "add", "-": "subtract", "*": "multiply", "/": "divide"}
        return call_function(op_map[operator], a, b)

    tokens = query.split()
    if tokens[0] in ["add", "subtract", "multiply", "divide"] and len(tokens) == 3:
        a, b = int(tokens[1]), int(tokens[2])
        return call_function(tokens[0], a, b)

    if "summarize" in query or "notes" in query:
        return generate_summary(query)

    if "search" in query:
        clean_query = query.replace("search", "").strip()
        if clean_query.startswith("for "):
            clean_query = clean_query[4:].strip()
        return web_search(clean_query)
    return infer_reasoning(query)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    response = process_query(user_message)
    return jsonify({"response": response})

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        summary = generate_summary(content)
        return jsonify({"response": summary})
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == "__main__":
    app.run(debug=True)
