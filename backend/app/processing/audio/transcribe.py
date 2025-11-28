import subprocess, uuid, os, librosa, torch, numpy as np
from transformers import WhisperProcessor, WhisperForConditionalGeneration

MODEL_NAME = "openai/whisper-tiny"

processor = WhisperProcessor.from_pretrained(MODEL_NAME)
model = WhisperForConditionalGeneration.from_pretrained(MODEL_NAME)

def preprocess_audio(path, target_rate=16000):
    temp = f"temp_{uuid.uuid4().hex}.wav"
    cmd = (
        f'ffmpeg -hide_banner -loglevel error -y -i "{path}" '
        f'-vn -acodec pcm_s16le -ac 1 -ar {target_rate} "{temp}"'
    )
    subprocess.run(cmd, shell=True)
    if not os.path.exists(temp):
        raise RuntimeError("FFmpeg failed to decode audio")
    return temp

def parse_whisper_segments(outputs):
    segments = []

    for seg in outputs["segments"][0]:  # <- Your format
        token_ids = seg["tokens"].tolist()

        text = processor.decode(token_ids, skip_special_tokens=True)

        # Convert logprob → probability-like confidence
        score = float(seg["result"]["sequences_scores"])
        confidence = float(np.exp(score / len(token_ids)))

        segments.append({
            "start": float(seg["start"]),
            "end": float(seg["end"]),
            "text": text.strip(),
            "confidence": confidence
        })

    return segments


def transcribe_audio(path):
    wav = preprocess_audio(path)

    audio, _ = librosa.load(wav, sr=16000)
    input_features = processor(audio, sampling_rate=16000, return_tensors="pt").input_features

    forced_ids = processor.get_decoder_prompt_ids(language="en", task="transcribe")

    outputs = model.generate(
        input_features,
        return_timestamps=True,           # gives segment timestamps
        return_dict_in_generate=True,     # enables dict output
        output_scores=True,               # enables confidence
        num_beams=5,                      # forces to return sequence_scores
        forced_decoder_ids=forced_ids,    # ensures transcription mode
    )

    text = processor.decode(outputs["sequences"][0], skip_special_tokens=True)
    segments = parse_whisper_segments(outputs)

    os.remove(wav)

    return {
        "text": text,
        "segments": segments   # [{text, timestamp:[start,end], confidence}, ...]
    }
