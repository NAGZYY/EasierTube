from utils import extract_audio
from silence import detect_voice_segments
from export_xml import export_fcp_xml
import os

def process_video(video_path, output_xml):
    audio_path = "output/audio.wav"

    extract_audio(video_path, audio_path)
    segments = detect_voice_segments(audio_path)
    export_fcp_xml(os.path.abspath(video_path), segments, output_xml)