from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from generate import generate_pipeline
import os
import subprocess

app = Flask(__name__)
CORS(app)

@app.route("/generate", methods=["POST"])
def generate():
    # 1. Validation
    if 'script' not in request.form:
        return jsonify({"error": "Missing required field: script"}), 400
    if 'avatar' not in request.files:
        return jsonify({"error": "Missing required file: avatar"}), 400

    script = request.form["script"]
    avatar = request.files["avatar"]

    if avatar.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 2. Save Upload
    os.makedirs("uploads", exist_ok=True)
    avatar_path = os.path.join("uploads", avatar.filename)
    avatar.save(avatar_path)

    # 3. Run Pipeline
    try:
        video_path = generate_pipeline(script, avatar_path)
        # Return just the filename so the frontend can request it via /outputs/
        return jsonify({"video": f"/outputs/{os.path.basename(video_path)}"})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# Serve the generated videos
@app.route("/outputs/<path:filename>")
def serve_video(filename):
    return send_from_directory("outputs", filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)