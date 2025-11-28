from app.processing.audio.transcribe import transcribe_audio
import os

def test_transcription_pipeline():
    base_dir = os.path.dirname(__file__)
    audio_path = os.path.abspath(
        os.path.join(base_dir, "..", "app", "data", "audio", "Sample_1.mp3")
    )
    assert os.path.exists(audio_path), "Test audio missing"
    
    result = transcribe_audio(audio_path)
    print(result)

    assert "text" in result
    assert isinstance(result["segments"], list)
    assert len(result["segments"]) > 0
    assert "confidence" in result["segments"][0]
