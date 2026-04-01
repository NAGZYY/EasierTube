import subprocess
import os

def extract_audio(video_path, output_wav):
    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-ac", "2",
        "-ar", "48000",
        output_wav
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def mp3_to_wav(mp3_path, wav_path):
    command = [
        "ffmpeg",
        "-y",
        "-i", mp3_path,
        wav_path
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)