import pytube
from pytube import YouTube
import os

def download_video(url, resolution, video_format, audio_format, compression_rate):
    yt = YouTube(url)
    stream = yt.streams.filter(resolution=resolution, file_extension=video_format).first()
    
    if audio_format == "MP3":
        output_file = stream.download(output_path=".")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".mp3"
        os.rename(output_file, new_file)
    elif audio_format == "WAV":
        output_file = stream.download(output_path=".")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".wav"
        os.rename(output_file, new_file)
    elif audio_format == "AAC":
        output_file = stream.download(output_path=".")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".aac"
        os.rename(output_file, new_file)
    elif audio_format == "FLAC":
        output_file = stream.download(output_path=".")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".flac"
        os.rename(output_file, new_file)
    elif audio_format == "OGG":
        output_file = stream.download(output_path=".")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".ogg"
        os.rename(output_file, new_file)
    elif audio_format == "M4A":
        output_file = stream.download(output_path=".")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".m4a"
        os.rename(output_file, new_file)
    elif audio_format == "WMA":
        output_file = stream.download(output_path=".")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".wma"
        os.rename(output_file, new_file)
    else:
        print("Invalid audio format. Please try again.")
    
    print(f"Video downloaded in {video_format} format with a resolution of {resolution} and an audio format of {audio_format} with a compression rate of {compression_rate} kbps.")

def download_audio_only(url, compression_rate, audio_format):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    
    if audio_format == "MP3":
        output_file = stream.download(output_path=".")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".mp3"
        os.rename(output_file, new_file)
    elif audio_format == "WAV":
        output_file = stream.download(output_path=".")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".wav"
        os.rename(output_file, new_file)
    elif audio_format == "AAC":
        output_file = stream.download(output_path=".")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".aac"
        os.rename(output_file, new_file)
    elif audio_format == "FLAC":
        output_file = stream.download(output_path=".")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".flac"
        os.rename(output_file, new_file)
    elif audio_format == "OGG":
        output_file = stream.download(output_path=".")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".ogg"
        os.rename(output_file, new_file)
    elif audio_format == "M4A":
        output_file = stream.download(output_path=".")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".m4a"
        os.rename(output_file, new_file)
    elif audio_format == "WMA":
        output_file = stream.download(output_path=".")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".wma"
        os.rename(output_file, new_file)
    else:
        print("Invalid audio format. Please try again.")
    
    print(f"Audio downloaded in {audio_format} format with a compression rate of {compression_rate} kbps.")

def main():
    url = input("Enter the YouTube video URL: ")
    print("Choose an option:")
    print("1. Video with Audio")
    print("2. Audio Only")
    print("3. Video Only")
    option = int(input("Enter your choice (1/2/3): "))
    
    if option == 1 or option == 3:
        yt = YouTube(url)
        resolutions = [stream.resolution for stream in yt.streams.filter(progressive=True)]
        print("Choose a resolution:")
        for i, resolution in enumerate(resolutions):
            print(f"{i+1}. {resolution}")
        resolution_choice = int(input("Enter your choice (1-{0}): ".
