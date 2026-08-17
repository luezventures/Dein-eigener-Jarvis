# Jarvis

Ein Python-Projekt für einen sprachgesteuerten Assistenten. Aktuell implementiert: Audioaufnahme über das Mikrofon mit automatischer Stille-Erkennung (Recording stoppt, sobald es lange genug still ist).

## Status

🚧 Frühe Entwicklungsphase. `Main.py` ist als Einstiegspunkt vorgesehen, aber noch leer. Die Spracherkennung (`faster-whisper`) ist als Abhängigkeit vorbereitet, aber noch nicht in den Code integriert.

## Features

- **[Sound.py](Sound.py)**: Nimmt Audio vom Standardmikrofon auf, berechnet pro Chunk den RMS-Pegel und beendet die Aufnahme automatisch nach einer konfigurierbaren Stille-Dauer. Danach wird die Aufnahme zur Kontrolle abgespielt.

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

Nimmt Audio auf, bis 2 Sekunden Stille erkannt wurden, und spielt die Aufnahme anschließend ab.

## Konfiguration

Die wichtigsten Parameter befinden sich am Anfang von [Sound.py](Sound.py):

| Parameter | Beschreibung | Default |
|---|---|---|
| `fs` | Sample-Rate | `48000` |
| `blocksize` | Chunk-Größe in Samples | `1024` |
| `threshold` | RMS-Schwelle für "Stille" | `0.01` |
| `silence_duration` | Sekunden Stille bis Stopp | `2.0` |

## Abhängigkeiten

Siehe [requirements.txt](requirements.txt):

- [sounddevice](https://pypi.org/project/sounddevice/) – Audio I/O
- [numpy](https://pypi.org/project/numpy/) – Signalverarbeitung
- [faster-whisper](https://pypi.org/project/faster-whisper/) – geplante Spracherkennung
- [scipy](https://pypi.org/project/scipy/) – Audioverarbeitung

## Lizenz

[MIT](LICENSE)
