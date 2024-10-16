from pytube import YouTube

def download_video(url, resolution, video_codec, audio_codec, download_type, bitrate=None):
    yt = YouTube(url)
    
    if download_type == "audio":
        stream = yt.streams.filter(only_audio=True, audio_codec=audio_codec).first()
        stream.download()
    elif download_type == "video":
        stream = yt.streams.filter(resolution=resolution, codec=video_codec).first()
        stream.download()
    elif download_type == "both":
        audio_stream = yt.streams.filter(only_audio=True, audio_codec=audio_codec).first()
        video_stream = yt.streams.filter(resolution=resolution, codec=video_codec).first()
        audio_stream.download()
        video_stream.download()
    else:
        print("Invalid download type")
        return

def main():
    url = input("Enter the YouTube video URL: ")
    yt = YouTube(url)
    
    # Fetch available resolutions
    resolutions = [stream.resolution for stream in yt.streams.filter(progressive=True)]
    print("Available resolutions:")
    for i, resolution in enumerate(resolutions):
        print(f"{i+1}. {resolution}")
    resolution_choice = int(input("Enter the number of your desired resolution: "))
    resolution = resolutions[resolution_choice-1]
    
    # Fetch available video codecs
    video_codecs = [stream.subtype for stream in yt.streams.filter(progressive=True)]
    print("Available video codecs:")
    for i, codec in enumerate(video_codecs):
        print(f"{i+1}. {codec}")
    video_codec_choice = int(input("Enter the number of your desired video codec: "))
    video_codec = video_codecs[video_codec_choice-1]
    
    # Fetch available audio codecs
    audio_codecs = [stream.audio_codec for stream in yt.streams.filter(only_audio=True)]
    print("Available audio codecs:")
    for i, codec in enumerate(audio_codecs):
        print(f"{i+1}. {codec}")
    audio_codec_choice = int(input("Enter the number of your desired audio codec: "))
    audio_codec = audio_codecs[audio_codec_choice-1]
    
    # If MP3 is selected, fetch available bitrates
    bitrate = None
    if audio_codec == "mp3":
        bitrates = [stream.abr for stream in yt.streams.filter(only_audio=True, audio_codec=audio_codec)]
        print("Available bitrates (kbps):")
        for i, rate in enumerate(bitrates):
            print(f"{i+1}. {rate} kbps")
        bitrate_choice = int(input("Enter the number of your desired bitrate: "))
        bitrate = bitrates[bitrate_choice-1]
    
    # Display download options
    print("Download options:")
    print("1. Audio only")
    print("2. Video only")
    print("3. Both audio and video")
    download_type_choice = int(input("Enter the number of your desired download type: "))
    if download_type_choice == 1:
        download_type = "audio"
    elif download_type_choice == 2:
        download_type = "video"
    elif download_type_choice == 3:
        download_type = "both"
    else:
        print("Invalid download type")
        return
    
    download_video(url, resolution, video_codec, audio_codec, download_type, bitrate)

if __name__ == "__main__":
    main()
