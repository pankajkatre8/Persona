def generate_pipeline(script, avatar_path):
    audio = f"temp/{uuid.uuid4()}.wav"

    # 1. TTS
    text_to_speech(script, audio)

    # 2. MuseTalk / InfiniteTalk (audio-driven)
    video = run_musetalk(avatar_path, audio)

    return video
