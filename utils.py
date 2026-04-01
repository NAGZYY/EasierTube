from pydub import AudioSegment
import os

def extract_audio(input_path, output_path, high_quality=True):
    try:
        # Charger le fichier (marche pour mp3, m4a, mp4, etc.)
        audio = AudioSegment.from_file(input_path)
        
        # Réglage de la qualité (16000Hz pour basse qualité, 44100Hz sinon)
        frame_rate = 16000 if not high_quality else 44100
        audio = audio.set_frame_rate(frame_rate)
        
        # Exportation en WAV
        # pcm_s16le est le codec standard pour le WAV
        audio.export(output_path, format="wav", codec="pcm_s16le")
        
        return True
    except Exception as e:
        raise Exception(f"Erreur Pydub : {str(e)}")