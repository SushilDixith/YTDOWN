import yt_dlp

def list_formats(url):
    ydl_opts = {
        'format': 'bestaudio+bestaudio/best'  # List both audio and video formats
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
    
    return formats

def get_audio_codecs(formats):
    audio_codecs = set()
    for f in formats:
        if f.get('acodec') and f['acodec'] not in audio_codecs:
            audio_codecs.add(f['acodec'])
    return list(audio_codecs)

def get_bitrates(formats, codec):
    bitrates = set()
    for f in formats:
        if f.get('acodec') == codec:
            bitrates.add(f.get('abr', 'N/A'))
    return list(bitrates)

def download_video(url, format_code):
    ydl_opts = {
        'format': format_code
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    url = input("Enter the YouTube video URL: ")

    # List available formats
    formats = list_formats(url)
    if not formats:
        print("No formats available for this video.")
        return

    # Download options
    print("\nDownload options:")
    print("1. Audio only")
    print("2. Video only")
    print("3. Both audio and video")
    download_type_choice = int(input("Enter the number of your desired download type: "))
    
    if download_type_choice == 1:
        audio_codecs = get_audio_codecs(formats)
        print("\nAvailable audio codecs:")
        for i, codec in enumerate(audio_codecs):
            print(f"{i+1}. {codec}")
        codec_choice = int(input("Select the audio codec: ")) - 1
        selected_codec = audio_codecs[codec_choice]

        if selected_codec == "mp3":
            bitrates = get_bitrates(formats, selected_codec)
            print("\nAvailable bitrates (kbps):")
            for i, rate in enumerate(bitrates):
                print(f"{i+1}. {rate} kbps")
            bitrate_choice = int(input("Select the desired bitrate: ")) - 1
            selected_bitrate = bitrates[bitrate_choice]
            format_code = f"bestaudio[abr<={selected_bitrate}]"
        else:
            format_code = f"bestaudio[acodec={selected_codec}]"

        print(f"Downloading audio with codec: {selected_codec} and bitrate: {selected_bitrate}")
        download_video(url, format_code)
        
    elif download_type_choice == 2:
        print("Available video formats:")
        video_formats = [f for f in formats if f.get('vcodec')]
        for i, f in enumerate(video_formats):
            print(f"{i+1}. Format code: {f['format_id']}, Resolution: {f.get('height', 'N/A')}p, Codec: {f['vcodec']}, Bitrate: {f.get('tbr', 'N/A')} kbps")
        video_choice = int(input("Select the desired video format: ")) - 1
        format_code = video_formats[video_choice]['format_id']
        print(f"Downloading video with format code: {format_code}")
        download_video(url, format_code)
        
    elif download_type_choice == 3:
        print("Available formats:")
        for i, f in enumerate(formats):
            print(f"{i+1}. Format code: {f['format_id']}, Resolution: {f.get('height', 'N/A')}p, Codec: {f.get('vcodec', 'none')} / {f.get('acodec', 'none')}, Bitrate: {f.get('tbr', 'N/A')} kbps")
        format_choice = int(input("Select the desired format: ")) - 1
        format_code = formats[format_choice]['format_id']
        print(f"Downloading audio and video with format code: {format_code}")
        download_video(url, format_code)

    else:
        print("Invalid download type selected.")

if __name__ == "__main__":
    main()
