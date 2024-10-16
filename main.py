from pytube import YouTube

def download_video(url, resolution=None, video_codec=None, audio_codec=None, download_type="both", bitrate=None):
    yt = YouTube(url)

    if download_type == "audio":
        audio_stream = yt.streams.filter(only_audio=True, abr=bitrate).first()
        if audio_stream:
            print(f"Downloading audio: {audio_stream}")
            audio_stream.download()
        else:
            print("No suitable audio stream found.")
    
    elif download_type == "video":
        video_stream = yt.streams.filter(res=resolution, subtype=video_codec).first()
        if video_stream:
            print(f"Downloading video: {video_stream}")
            video_stream.download()
        else:
            print("No suitable video stream found.")
    
    elif download_type == "both":
        video_stream = yt.streams.filter(res=resolution, subtype=video_codec).first()
        audio_stream = yt.streams.filter(only_audio=True, abr=bitrate).first()
        if video_stream and audio_stream:
            print(f"Downloading video: {video_stream}")
            video_stream.download()
            print(f"Downloading audio: {audio_stream}")
            audio_stream.download()
        else:
            print("No suitable video/audio stream found.")
    else:
        print("Invalid download type selected.")

def main():
    url = input("Enter the YouTube video URL: ")
    yt = YouTube(url)

    # Fetch available resolutions
    available_streams = yt.streams.filter(progressive=True)
    resolutions = list(set([stream.resolution for stream in available_streams if stream.resolution]))
    resolutions.sort()
    print("Available resolutions:")
    for i, resolution in enumerate(resolutions):
        print(f"{i+1}. {resolution}")
    resolution_choice = int(input("Enter the number of your desired resolution: "))
    resolution = resolutions[resolution_choice-1]

    # Fetch available video codecs
    video_codecs = list(set([stream.subtype for stream in available_streams]))
    print("Available video codecs:")
    for i, codec in enumerate(video_codecs):
        print(f"{i+1}. {codec}")
    video_codec_choice = int(input("Enter the number of your desired video codec: "))
    video_codec = video_codecs[video_codec_choice-1]

    # Fetch available audio codecs
    audio_streams = yt.streams.filter(only_audio=True)
    audio_codecs = list(set([stream.audio_codec for stream in audio_streams if stream.audio_codec]))
    print("Available audio codecs:")
    for i, codec in enumerate(audio_codecs):
        print(f"{i+1}. {codec}")
    audio_codec_choice = int(input("Enter the number of your desired audio codec: "))
    audio_codec = audio_codecs[audio_codec_choice-1]

    # Fetch available bitrates if MP3
    bitrate = None
    if audio_codec == "mp3":
        bitrates = list(set([stream.abr for stream in audio_streams if stream.abr]))
        print("Available bitrates (kbps):")
        for i, rate in enumerate(bitrates):
            print(f"{i+1}. {rate}")
        bitrate_choice = int(input("Enter the number of your desired bitrate: "))
        bitrate = bitrates[bitrate_choice-1]

    # Download options
    print("Download options:")
    print("1. Audio only")
    print("2. Video only")
    print("3. Both audio and video")
    download_type_choice = int(input("Enter the number of your desired download type: "))
    download_type = ["audio", "video", "both"][download_type_choice-1]

    # Start downloading
    download_video(url, resolution, video_codec, audio_codec, download_type, bitrate)

if __name__ == "__main__":
    main()
