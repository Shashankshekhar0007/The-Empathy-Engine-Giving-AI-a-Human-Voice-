import os
import requests
import nltk
from dotenv import load_dotenv
from transformers import pipeline, logging
from nltk.tokenize import sent_tokenize

# =========================
# INITIAL SETUP
# =========================
logging.set_verbosity_error()
nltk.download("punkt")

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

if not ELEVENLABS_API_KEY:
    raise ValueError("Missing ELEVENLABS_API_KEY in .env file")

# =========================
# LOAD EMOTION MODEL
# =========================
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)

# =========================
# EMOTION DETECTION
# =========================
def detect_emotion(text):
    outputs = emotion_classifier(text)

    if isinstance(outputs[0], list):
        preds = outputs[0]
    else:
        preds = outputs

    top = max(preds, key=lambda x: x["score"])

    label = top["label"].lower()
    intensity = float(top["score"])

    if label in ["joy", "surprise"]:
        return "happy", intensity

    if label in ["anger", "sadness", "fear", "disgust"]:
        return "frustrated", intensity

    return "neutral", intensity



# =========================
# EMOTION → VOICE MAPPING
# =========================
def emotion_to_voice_params(emotion, intensity):
    if emotion == "happy":
        return {
            "stability": round(max(0.2, 0.45 - intensity), 2),
            "similarity_boost": 0.85,
            "style": round(min(1.0, 0.6 + intensity), 2)
        }

    if emotion == "frustrated":
        return {
            "stability": round(min(1.0, 0.6 + intensity), 2),
            "similarity_boost": 0.65,
            "style": 0.3
        }

    return {
        "stability": 0.55,
        "similarity_boost": 0.75,
        "style": 0.5
    }


# =========================
# ELEVENLABS CALL
# =========================
def call_elevenlabs(text, voice_settings):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice_settings": voice_settings
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"TTS failed: {response.text}")

    return response.content


# =========================
# SENTENCE-LEVEL SYNTHESIS
# =========================
def synthesize_speech(text, output_file="output.mp3"):
    sentences = sent_tokenize(text)

    print("\n--- Sentence-Level Emotional Analysis ---")

    audio_chunks = []

    for sentence in sentences:
        emotion, intensity = detect_emotion(sentence)
        voice_settings = emotion_to_voice_params(emotion, intensity)

        print(f"Sentence: {sentence}")
        print(f"→ Emotion: {emotion.upper()} | Intensity: {round(intensity,3)}")
        print(f"→ Voice Params: {voice_settings}\n")

        audio_data = call_elevenlabs(sentence, voice_settings)
        audio_chunks.append(audio_data)
        
    # Merge audio chunks
    with open(output_file, "wb") as f:
        for chunk in audio_chunks:
            f.write(chunk)

    print(f"🎧 Final Audio Generated → {output_file}")
    return output_file


# =========================
# CLI ENTRY
# =========================
if __name__ == "__main__":
    print("\n=== Empathy Engine (Sentence-Level Modulation Enabled) ===")

    while True:
        text = input("\nEnter text (q to quit): ").strip()
        if text.lower() == "q":
            break

        synthesize_speech(text)
