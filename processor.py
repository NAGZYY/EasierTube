from utils import extract_audio
from silence import detect_voice_segments
from export_xml import export_fcp_xml
import os

def process_video(video_path, output_xml, progress_callback=None):
    audio_path = "output/audio.wav"

    # Étape 1 : extraction audio
    extract_audio(video_path, audio_path)
    if progress_callback:
        progress_callback(10, "Analyse de l'audio...")

    # Étape 2 : détection des silences
    segments = detect_voice_segments(audio_path)
    if progress_callback:
        progress_callback(50, "Détection des silences...")

    # Étape 3 : export XML
    export_fcp_xml(os.path.abspath(video_path), segments, output_xml)
    if progress_callback:
        progress_callback(100, "Export prêt !")