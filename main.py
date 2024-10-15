import os
import requests
from bs4 import BeautifulSoup
from pytube import YouTube

def download_video(url, resolution, format):
    yt = YouTube(url)
    stream = yt.streams.filter(resolution=resolution, file_extension=format).first()
    stream.download()

def download_audio(url, format):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True, file_extension=format).first()
    stream.download()

def main():
    url = input("Enter the YouTube video URL: ")
    print("Available formats and resolutions:")
    yt = YouTube(url)
    for stream in yt.streams:
        print(f"{stream.resolution} - {stream.file_extension}")
    resolution = input("Enter the desired resolution: ")
    format = input("Enter the desired format (MP4, WebM, etc.): ")
    download_video(url, resolution, format)

if __name__ == "__main__":
    main()
