from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from generate import generate_pipeline
import os

app = Flask(__name__)
CORS(app)

@app.route("/generate", methods=["POST"])
def generate():
    script = request.form["script"]
    avatar = request.files["avatar"]

    os.makedirs("uploads", exist_ok=True)
    avatar_path = f"uploads/{avatar.filename}"
    avatar.save(avatar_path)

    video = generate_pipeline(script, avatar_path)
    return jsonify({"video": "/" + video})

@app.route("/outputs/<path:filename>")
def serve_video(filename):
    return send_from_directory("outputs", filename)

app.run(debug=True)
