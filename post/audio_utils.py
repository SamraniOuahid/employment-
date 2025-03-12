# post/audio_utils.py

from pydub import AudioSegment

def convert_audio_to_wav(input_file, output_file="converted.wav", sample_rate=16000):
    """Convertit un fichier audio en format WAV mono 16kHz."""
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_channels(1).set_frame_rate(sample_rate)
    audio.export(output_file, format="wav")
    return output_file