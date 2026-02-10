from flask import Flask, request, jsonify
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

    return jsonify({"video": video})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
