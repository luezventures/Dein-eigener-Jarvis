import sounddevice as sd
import numpy as np
import time as ti

# ---- Konfiguration ----
fs = 48000              # Sample rate
blocksize = 1024        # Größe eines einzelnen Audio-Häppchens (Samples)
threshold = 0.01         # RMS-Schwelle: alles darunter gilt als "Stille"
silence_duration = 2.0   # Sekunden am Stück still, bevor Aufnahme stoppt

chunk_duration = blocksize / fs  # Dauer eines Chunks in Sekunden

# ---- Zustand, den der Callback von außen sehen/verändern muss ----
chunks = [] # hier sammeln Samples der einzelnen Chunks
state = {"silence_counter": 0.0, "done": False}


def audio_callback(indata, frames, time, status):
    if status:
        print("Status-Warnung:", status)

    # 1. Chunk einsammeln
    chunks.append(indata.copy())

    # 2. Lautstärke (RMS) dieses Chunks berechnen
    rms = np.sqrt(np.mean(indata ** 2))

    # 3. Gegen Schwelle prüfen und Stille-Zähler updaten
    if rms < threshold:
        state["silence_counter"] += chunk_duration
    else:
        state["silence_counter"] = 0.0

    # 4. Fertig-Flag setzen, sobald genug Stille am Stück war
    if state["silence_counter"] >= silence_duration:
        state["done"] = True


print("Recording...")

with sd.InputStream(samplerate=fs, channels=1, dtype="float32", blocksize=blocksize, callback=audio_callback):
    while not state["done"]:
        ti.sleep(0.05)

print("Fertig, Stille erkannt.")

# ---- Chunks zu einem einzigen Array zusammenfügen ----
audio = np.concatenate(chunks)
print("Aufnahme-Shape:", audio.shape, "| Länge in Sekunden:", len(audio) / fs)

# ---- Zur Kontrolle abspielen ----
sd.play(audio, fs)
sd.wait()



