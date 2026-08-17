import pyttsx3

Deutsche_Stimme = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_DE-DE_HEDDA_11.0"

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', Deutsche_Stimme)
    engine.setProperty('rate', 165)  # Sprechgeschwindigkeit anpassen (Standard: 200)
    engine.setProperty('volume', 1.0)  # Lautstärke anpassen (0.0 bis 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

if __name__ == "__main__":
    # Kleiner Testlauf, wenn du diese Datei direkt ausführst
    speak("Hallo, ich bin dein Jarvis. Test eins, zwei, drei.")
    speak("Und hier ist noch ein zweiter, komplett separater Aufruf.")