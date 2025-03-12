# post/audio_transcription.py

import speech_recognition as sr

def transcribe_audio(audio_file_path, language="fr-FR"):
    """Transcrit un fichier audio en texte à l'aide de PocketSphinx."""
    recognizer = sr.Recognizer()

    # Lire le fichier audio
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)  # Lire tout le fichier audio

    try:
        # Utiliser PocketSphinx pour transcrire le fichier audio
        text = recognizer.recognize_sphinx(audio_data, language=language)
        return text
    except sr.UnknownValueError:
        return "Impossible de comprendre l'audio."
    except sr.RequestError:
        return "Erreur lors du traitement de l'audio."