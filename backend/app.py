from flask import Flask, request, jsonify
from flask_cors import CORS
from generate import generate_pipeline
import os
import subprocess

app = Flask(__name__)
CORS(app)

@app.route("/generate", methods=["POST"])
def generate():
    script = request.form.get("script")
    avatar = request.files.get("avatar")

    if not script:
        return jsonify({"error": "Missing required field: script"}), 400
    if not avatar:
        return jsonify({"error": "Missing required file: avatar"}), 400

    os.makedirs("uploads", exist_ok=True)
    avatar_path = f"uploads/{avatar.filename}"
    avatar.save(avatar_path)

    try:
        video = generate_pipeline(script, avatar_path)
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 503
    except subprocess.CalledProcessError as exc:
        return jsonify({
            "error": "Video generation subprocess failed",
            "command": exc.cmd,
            "return_code": exc.returncode,
        }), 500

    return jsonify({"video": video})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
