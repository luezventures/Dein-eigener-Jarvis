import sounddevice as sd
import numpy as np
import time as ti
from faster_whisper import WhisperModel
import pyttsx3

# ---- Konfiguration Aufnahme ----
fs = 48000
blocksize = 1024
threshold = 0.01
silence_duration = 2.0
chunk_duration = blocksize / fs

# ---- Konfiguration TTS ----
GERMAN_VOICE_ID = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_DE-DE_HEDDA_11.0'


def record_until_silence():
    """Nimmt auf bis silence_duration Sekunden am Stück Stille herrschen.
    Gibt ein 1D float32 NumPy-Array bei 48kHz zurück."""
    chunks = []
    state = {"silence_counter": 0.0, "done": False}

    def audio_callback(indata, frames, time, status):
        if status:
            print("Status-Warnung:", status)
        chunks.append(indata.copy())
        rms = np.sqrt(np.mean(indata ** 2))
        if rms < threshold:
            state["silence_counter"] += chunk_duration
        else:
            state["silence_counter"] = 0.0
        if state["silence_counter"] >= silence_duration:
            state["done"] = True

    print("Rede los, sobald du fertig bist wird automatisch gestoppt...")
    with sd.InputStream(samplerate=fs, channels=1, dtype="float32",
                         blocksize=blocksize, callback=audio_callback):
        while not state["done"]:
            ti.sleep(0.05)

    audio = np.concatenate(chunks)
    return audio


def transcribe(audio, fs, model):
    """Nimmt das 48kHz-Array, macht es Whisper-tauglich (16kHz, 1D) und transkribiert."""
    # (N, 1) -> (N,)  falls nötig
    audio_1d = np.squeeze(audio)

    # 48000 -> 16000 Hz resampeln (einfaches, aber ausreichend gutes Verfahren
    # für Sprache: lineares Interpolieren über scipy)
    from scipy.signal import resample
    target_len = int(len(audio_1d) * 16000 / fs)
    audio_16k = resample(audio_1d, target_len).astype(np.float32)

    segments, info = model.transcribe(audio_16k, language="de")
    text = " ".join(segment.text.strip() for segment in segments)
    return text


def speak(text):
    """Spricht einen Text komplett als EINEN String."""
    engine = pyttsx3.init()
    engine.setProperty('voice', GERMAN_VOICE_ID)
    engine.setProperty('rate', 165)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


if __name__ == "__main__":
    print("Lade Whisper-Modell (base)...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    # base statt small: im Benchmark ~3x schneller (0.8s vs 2.4s) bei
    # vergleichbarer Genauigkeit auf CPU -> besserer Kompromiss fuer Echtzeit
    # compute_type='int8' macht die CPU-Inferenz zusaetzlich schneller
    # als der float32-Standard, bei kaum merkbarem Genauigkeitsverlust

    audio = record_until_silence()
    print("Aufnahme fertig, transkribiere...")

    start = ti.time()
    text = transcribe(audio, fs, model)
    elapsed = ti.time() - start

    print(f"Erkannter Text: {text}")
    print(f"Transkriptionszeit: {elapsed:.2f} Sekunden")

    speak("Du hast gesagt: " + text)