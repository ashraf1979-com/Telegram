import os
import speech_recognition as sr
from pydub import AudioSegment
import logging
from config import TEMP_AUDIO_PATH

os.makedirs(TEMP_AUDIO_PATH, exist_ok=True)

def convert_ogg_to_wav(ogg_path: str) -> str:
    wav_path = ogg_path.replace(".ogg", ".wav")
    audio = AudioSegment.from_ogg(ogg_path)
    audio.export(wav_path, format="wav")
    return wav_path

def transcribe_with_google(wav_path: str) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language="ar-EG")
    except sr.UnknownValueError:
        return "❌ لم أفهم الصوت."
    except sr.RequestError:
        return "❌ تعذر الاتصال بخدمة Google."
