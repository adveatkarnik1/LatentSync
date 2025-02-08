import subprocess

def extract_audio_ffmpeg(video_path, output_audio_path):
    command = [
        "ffmpeg",
        "-i", video_path,        # Input video
        "-vn",                   # Disable video
        "-acodec", "pcm_s16le",   # WAV format
        "-ar", "44100",           # Sample rate
        "-ac", "2",               # Stereo
        output_audio_path
    ]
    subprocess.run(command, check=True)

# Example usage:
extract_audio_ffmpeg("assets/demo1_video.mp4", "assets/demo1_audio.wav")