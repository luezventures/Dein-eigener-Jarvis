# Jarvis

Ein Python-Projekt für einen sprachgesteuerten Assistenten. Aktuell implementiert: Audioaufnahme über das Mikrofon mit automatischer Stille-Erkennung, lokale Transkription per Whisper und Sprachausgabe der Antwort per TTS.

## Status

🚧 Frühe Entwicklungsphase. `Main.py` ist als Einstiegspunkt vorgesehen, aber noch leer. `Sound.py` deckt bereits den kompletten Ablauf Aufnahme → Transkription → Sprachausgabe ab.

## Features

- **[Sound.py](Sound.py)**: Nimmt Audio vom Standardmikrofon auf, berechnet pro Chunk den RMS-Pegel und beendet die Aufnahme automatisch nach einer konfigurierbaren Stille-Dauer. Die Aufnahme wird anschließend auf 16kHz resampelt und mit `faster-whisper` (Modell `base`, Sprache Deutsch) transkribiert. Der erkannte Text wird per `pyttsx3` (deutsche Windows-TTS-Stimme) vorgelesen.
- **[tts.py](tts.py)**: Eigenständiges Test-Skript für die Sprachausgabe (`pyttsx3`) ohne Aufnahme/Transkription.

## Installation

```bash
git clone https://github.com/<dein-username>/Jarvis.git
cd Jarvis
pip install -r requirements.txt
```

## Verwendung

```bash
python Sound.py
```

Nimmt Audio auf, bis 2 Sekunden Stille erkannt wurden, transkribiert die Aufnahme und liest das Ergebnis ("Du hast gesagt: ...") anschließend vor.

```bash
python tts.py
```

Spielt zwei Testsätze über die deutsche TTS-Stimme ab.

## Konfiguration

Die wichtigsten Parameter befinden sich am Anfang von [Sound.py](Sound.py):

| Parameter | Beschreibung | Default |
|---|---|---|
| `fs` | Sample-Rate der Aufnahme | `48000` |
| `blocksize` | Chunk-Größe in Samples | `1024` |
| `threshold` | RMS-Schwelle für "Stille" | `0.01` |
| `silence_duration` | Sekunden Stille bis Stopp | `2.0` |
| `GERMAN_VOICE_ID` | Registry-ID der Windows-TTS-Stimme | `TTS_MS_DE-DE_HEDDA_11.0` |

> **Hinweis:** `GERMAN_VOICE_ID` ist ein Windows-Registry-Pfad zu einer lokal installierten Sprachpaket-Stimme (kein Secret). Er funktioniert nur, wenn die entsprechende deutsche Stimme unter Windows installiert ist.

## Abhängigkeiten

Siehe [requirements.txt](requirements.txt):

- [sounddevice](https://pypi.org/project/sounddevice/) – Audio I/O
- [numpy](https://pypi.org/project/numpy/) – Signalverarbeitung
- [faster-whisper](https://pypi.org/project/faster-whisper/) – Spracherkennung (lokal, CPU, `int8`)
- [scipy](https://pypi.org/project/scipy/) – Resampling der Audiodaten
- [pyttsx3](https://pypi.org/project/pyttsx3/) – Text-to-Speech (Windows SAPI5)

## Lizenz

[MIT](LICENSE)
