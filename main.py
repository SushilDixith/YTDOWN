import yt_dlp
from tqdm import tqdm

# Progress bar hook to show progress
def progress_hook(tq):
    def inner(d):
        if d['status'] == 'downloading':
            tq.total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            tq.update(d['downloaded_bytes'] - tq.n)
        elif d['status'] == 'finished':
            tq.close()
            print(f"\nDownload completed. File saved to {d['filename']}")
    return inner


# Fetch available formats from the YouTube URL
def list_formats(url):
    ydl_opts = {'format': 'bestaudio+bestaudio/best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
    return formats


# Fetch all available audio codecs
def get_audio_codecs(formats):
    audio_codecs = set()
    for f in formats:
        if f.get('acodec') and f['acodec'] != 'none':
            audio_codecs.add(f['acodec'])
    return list(audio_codecs)


# Fetch bitrates for a specific audio codec (MP3, etc.)
def get_bitrates(formats, codec):
    bitrates = set()
    for f in formats:
        if f.get('acodec') == codec and f.get('abr'):
            bitrates.add(f.get('abr', 'N/A'))
    return list(bitrates)


# Function to download video or audio with progress tracking
def download_video(url, format_code):
    with tqdm(unit="B", unit_scale=True, unit_divisor=1024, miniters=1, desc="Downloading") as tq:
        ydl_opts = {
            'format': format_code,
            'progress_hooks': [progress_hook(tq)],  # Use progress bar during download
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


def main():
    url = input("Enter the YouTube video URL: ")

    # List all available formats
    formats = list_formats(url)
    if not formats:
        print("No formats available for this video.")
        return

    # Download options: Audio, Video, or Both
    print("\nDownload options:")
    print("1. Audio only")
    print("2. Video only")
    print("3. Both audio and video")

    try:
        download_type_choice = int(input("Enter the number of your desired download type: "))
    except ValueError:
        print("Invalid input. Please enter a number (1, 2, or 3).")
        return

    if download_type_choice == 1:
        # Fetch and list available audio codecs
        audio_codecs = get_audio_codecs(formats)
        if not audio_codecs:
            print("No audio formats available.")
            return

        print("\nAvailable audio codecs:")
        for i, codec in enumerate(audio_codecs):
            print(f"{i+1}. {codec}")
        try:
            codec_choice = int(input("Select the audio codec: ")) - 1
            if codec_choice < 0 or codec_choice >= len(audio_codecs):
                print("Invalid selection. Please choose a valid option.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        selected_codec = audio_codecs[codec_choice]

        # If codec is MP3, show available bitrates
        if selected_codec == "mp3":
            bitrates = get_bitrates(formats, selected_codec)
            if bitrates:
                print("\nAvailable bitrates (kbps):")
                for i, rate in enumerate(bitrates):
                    print(f"{i+1}. {rate} kbps")
                try:
                    bitrate_choice = int(input("Select the desired bitrate: ")) - 1
                    if bitrate_choice < 0 or bitrate_choice >= len(bitrates):
                        print("Invalid selection. Please choose a valid option.")
                        return
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    return

                selected_bitrate = bitrates[bitrate_choice]
                format_code = f"bestaudio[abr<={selected_bitrate}]"
            else:
                print("No available bitrates for MP3.")
                return
        else:
            format_code = f"bestaudio[acodec={selected_codec}]"

        print(f"Downloading audio with codec: {selected_codec}")
        download_video(url, format_code)

    elif download_type_choice == 2:
        print("Available video formats:")
        video_formats = [f for f in formats if f.get('vcodec') and f['vcodec'] != 'none']
        if not video_formats:
            print("No video formats available.")
            return

        for i, f in enumerate(video_formats):
            print(f"{i+1}. Format code: {f['format_id']}, Resolution: {f.get('height', 'N/A')}p, Codec: {f['vcodec']}, Bitrate: {f.get('tbr', 'N/A')} kbps")
        try:
            video_choice = int(input("Select the desired video format: ")) - 1
            if video_choice < 0 or video_choice >= len(video_formats):
                print("Invalid selection. Please choose a valid option.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        format_code = video_formats[video_choice]['format_id']
        print(f"Downloading video with format code: {format_code}")
        download_video(url, format_code)

    elif download_type_choice == 3:
        print("Available formats:")
        for i, f in enumerate(formats):
            print(f"{i+1}. Format code: {f['format_id']}, Resolution: {f.get('height', 'N/A')}p, Codec: {f.get('vcodec', 'none')} / {f.get('acodec', 'none')}, Bitrate: {f.get('tbr', 'N/A')} kbps")
        try:
            format_choice = int(input("Select the desired format: ")) - 1
            if format_choice < 0 or format_choice >= len(formats):
                print("Invalid selection. Please choose a valid option.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        format_code = formats[format_choice]['format_id']
        print(f"Downloading audio and video with format code: {format_code}")
        download_video(url, format_code)

    else:
        print("Invalid download type selected.")


if __name__ == "__main__":
    main()
