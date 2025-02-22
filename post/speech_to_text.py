# speech_to_text.py

from google.cloud import speech_v1p1beta1 as speech

def transcribe_audio(audio_file_path):
    """Transcrit un fichier audio en texte à l'aide de Google Speech-to-Text."""
    client = speech.SpeechClient()

    # Lire le contenu du fichier audio
    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    # Configurer les paramètres de reconnaissance vocale
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="fr-FR",  # Utilisez "en-US" si vous travaillez en anglais
        sample_rate_hertz=16000
    )

    # Effectuer la transcription
    response = client.recognize(config=config, audio=audio)

    # Extraire et retourner le texte transcrit
    transcribed_text = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcribed_text