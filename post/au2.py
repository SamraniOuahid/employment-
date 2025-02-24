import speech_recognition as sr

def transcribe_audio(audio_file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)  # Lire le fichier audio
        try:
            text = recognizer.recognize_sphinx(audio_data, language="fr-FR")  # Transcrire en français
            return text
        except sr.UnknownValueError:
            return "Impossible de comprendre l'audio."
        except sr.RequestError:
            return "Erreur lors du traitement de l'audio."

# Exemple d'utilisation
audio_file_path = "example.wav"
text = transcribe_audio(audio_file_path)
print("Texte transcrit :", text)