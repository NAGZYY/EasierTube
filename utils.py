import subprocess
import time

def extract_audio(video_path, output_wav):
    print("🎧 Extraction audio (ffmpeg)...")
    start = time.time()

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-ac", "1",          # 🔥 mono = 2x plus rapide
        "-ar", "16000",      # 🔥 16kHz largement suffisant pour voix
        "-vn",
        output_wav
    ]

    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    elapsed = round(time.time() - start, 2)
    print(f"✔ Audio extrait en {elapsed}s")