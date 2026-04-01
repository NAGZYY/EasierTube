from utils import extract_audio
from silence import detect_voice_segments
from export_xml import export_fcpxml
import os, time

def process_video(video_path, output_xml, job_id, sensitivity, margin_ms):
    audio_path = os.path.join("output", f"{job_id}_analysis.wav")

    yield 5, "Préparation du projet..."
    time.sleep(0.2)

    yield 10, "Extraction audio (analyse)..."
    extract_audio(video_path, audio_path)

    for p in range(12, 25, 3):
        time.sleep(0.15)
        yield p, "Extraction audio en cours..."

    yield 30, f"Analyse des silences ({sensitivity})..."
    segments = detect_voice_segments(
        audio_path,
        sensitivity=sensitivity,
        padding_ms=margin_ms
    )

    for p in range(35, 70, 5):
        time.sleep(0.2)
        yield p, "Analyse audio en cours..."

    yield 80, "Génération du XML vidéo (Premiere)..."
    export_fcpxml(
        os.path.abspath(video_path),
        segments,
        output_xml
    )

    for p in range(85, 95, 2):
        time.sleep(0.15)
        yield p, "Écriture du projet XML..."

    if os.path.exists(audio_path):
        os.remove(audio_path)

    yield 100, "Montage prêt 🎬"