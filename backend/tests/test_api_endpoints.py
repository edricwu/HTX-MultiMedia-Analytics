import os

def test_upload_and_retrieve_video_audio(client):
    base_dir = os.path.dirname(__file__)
    video_path = os.path.abspath(
        os.path.join(base_dir, "..", "app", "data", "videos", "video_08.mp4")
    )
    audio_path = os.path.abspath(
        os.path.join(base_dir, "..", "app", "data", "audio", "Sample_1.mp3")
    )
    # upload video
    with open(video_path, "rb") as f:
        response = client.post("/process/video", files={"file": ("v.mp4", f, "video/mp4")})
    assert response.status_code == 200

    # upload audio
    with open(audio_path, "rb") as f:
        response = client.post("/process/audio", files={"file": ("a.wav", f, "audio/wav")})
    assert response.status_code == 200

    # Get videos
    res = client.get("/videos")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
