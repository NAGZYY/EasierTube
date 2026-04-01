import os
from utils import extract_audio
from silence import detect_voice_segments
from export_xml import export_fcp_xml

INPUT_VIDEO = "input/video.mp4"
OUTPUT_AUDIO = "output/audio.wav"
OUTPUT_XML = "output/EasierTube_Project.xml"

os.makedirs("output", exist_ok=True)

print("🎬 EasierTube – Extraction audio...")
extract_audio(INPUT_VIDEO, OUTPUT_AUDIO)

print("🔊 Analyse des silences...")
segments = detect_voice_segments(OUTPUT_AUDIO)

print(f"✂️ {len(segments)} segments détectés")

print("📄 Génération du projet Premiere (XML)...")
export_fcp_xml(
    os.path.abspath(INPUT_VIDEO),
    segments,
    OUTPUT_XML
)

print("✅ Terminé !")
print("➡️ Importe EasierTube_Project.xml dans Premiere Pro")