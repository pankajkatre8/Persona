import { useState } from "react";
import api from "./api";

function App() {
  const [script, setScript] = useState("");
  const [avatar, setAvatar] = useState(null);
  const [video, setVideo] = useState(null);
  const [loading, setLoading] = useState(false);

  async function generateVideo() {
    if (!script || !avatar) {
      alert("Please enter text and upload an image");
      return;
    }

    const formData = new FormData();
    formData.append("script", script);
    formData.append("avatar", avatar);

    setLoading(true);
    setVideo(null);

    try {
      const res = await api.post("/generate", formData);
      setVideo("http://127.0.0.1:5000" + res.data.video);
    } catch (err) {
      alert("Generation failed. Check backend logs.");
      console.error(err);
    }

    setLoading(false);
  }

  return (
    <div className="container">
      <div className="card">
        <h2>HeyGen-Style Avatar Demo</h2>

        <textarea
          rows="4"
          placeholder="Enter script here…"
          value={script}
          onChange={(e) => setScript(e.target.value)}
        />

        <input
          type="file"
          accept="image/*"
          onChange={(e) => setAvatar(e.target.files[0])}
        />

        <button onClick={generateVideo} disabled={loading}>
          {loading ? "Generating… (this may take a few minutes)" : "Generate Video"}
        </button>

        {video && (
          <div className="video-box">
            <video src={video} controls width="100%" />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
