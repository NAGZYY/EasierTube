from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def detect_voice_segments(wav_path, sensitivity="normal", padding_ms=120):
    audio = AudioSegment.from_wav(wav_path)
    
    # Mapping de la sensibilité
    configs = {
        "doux": {"min_len": 600, "thresh_offset": 10},
        "normal": {"min_len": 400, "thresh_offset": 16},
        "agressif": {"min_len": 200, "thresh_offset": 22}
    }
    
    cfg = configs.get(sensitivity, configs["normal"])

    nonsilent_ranges = detect_nonsilent(
        audio,
        min_silence_len=cfg["min_len"],
        silence_thresh=audio.dBFS - cfg["thresh_offset"]
    )

    segments = []
    for start, end in nonsilent_ranges:
        segments.append((
            max(0, start - padding_ms),
            min(len(audio), end + padding_ms)
        ))

    return segments