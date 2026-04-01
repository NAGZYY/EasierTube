from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import time

def detect_voice_segments(wav_path, sensitivity="normal", padding_ms=120):
    print("🔍 Analyse audio (silences)...")
    start_time = time.time()

    audio = AudioSegment.from_wav(wav_path)

    duration_sec = len(audio) / 1000
    print(f"▶ Durée audio : {round(duration_sec, 2)} sec")

    configs = {
        "doux": {"min_len": 700, "thresh_offset": 12},
        "normal": {"min_len": 500, "thresh_offset": 18},
        "agressif": {"min_len": 300, "thresh_offset": 24}
    }

    cfg = configs.get(sensitivity, configs["normal"])

    nonsilent_ranges = detect_nonsilent(
        audio,
        min_silence_len=cfg["min_len"],
        silence_thresh=audio.dBFS - cfg["thresh_offset"],
        seek_step=10  # 🔥 clé : skip frames → énorme gain
    )

    segments = []
    for start, end in nonsilent_ranges:
        segments.append((
            max(0, start - padding_ms),
            min(len(audio), end + padding_ms)
        ))

    elapsed = round(time.time() - start_time, 2)
    print(f"✔ Segments détectés : {len(segments)}")
    print(f"✔ Temps analyse audio : {elapsed}s")

    return segments