from utils import extract_audio
from silence import detect_voice_segments
from export_xml import export_fcp_xml
import os

def process_video(video_path, output_xml, job_id, sensitivity, margin_ms):
    # Utilisation du job_id pour éviter les conflits de fichiers audio
    audio_path = os.path.join("output", f"{job_id}.wav")

    yield 10, "Extraction de l'audio..."
    extract_audio(video_path, audio_path)

    yield 30, f"Analyse des silences ({sensitivity})..."
    # On adapte les paramètres de silence.py selon le choix utilisateur
    segments = detect_voice_segments(audio_path, sensitivity=sensitivity, padding_ms=margin_ms)

    yield 80, "Génération du XML Premiere..."
    export_fcp_xml(os.path.abspath(video_path), segments, output_xml)

    # Nettoyage de l'audio temporaire pour économiser l'espace
    if os.path.exists(audio_path):
        os.remove(audio_path)
    
    yield 95, "Finalisation..."