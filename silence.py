from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def detect_voice_segments(
    wav_path,
    min_silence_len=400,
    silence_offset_db=16,
    padding_ms=120
):
    audio = AudioSegment.from_wav(wav_path)

    nonsilent_ranges = detect_nonsilent(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=audio.dBFS - silence_offset_db
    )

    segments = []
    for start, end in nonsilent_ranges:
        segments.append((
            max(0, start - padding_ms),
            min(len(audio), end + padding_ms)
        ))

    return segments