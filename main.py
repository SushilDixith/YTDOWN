import yt_dlp
from tqdm import tqdm
import os

def progress_hook(tq):
    def inner(d):
        if d['status'] == 'downloading':
            tq.total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            tq.update(d['downloaded_bytes'] - tq.n)
        elif d['status'] == 'finished':
            tq.close()
            print(f"\nDownload completed. File saved to {d['filename']}")
    return inner

def list_formats(url):
    ydl_opts = {'format': 'bestaudio+bestaudio/best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
    return formats

def get_audio_codecs(formats):
    return list(set(f['acodec'] for f in formats if f.get('acodec') and f['acodec'] != 'none'))

def get_bitrates(formats, codec):
    return list(set(f.get('abr', 'N/A') for f in formats if f.get('acodec') == codec and f.get('abr')))

def download_video(url, format_code, output_path):
    with tqdm(unit="B", unit_scale=True, unit_divisor=1024, miniters=1, desc="Downloading") as tq:
        ydl_opts = {
            'format': format_code,
            'progress_hooks': [progress_hook(tq)],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s')
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
            except Exception as e:
                print(f"An error occurred during download: {e}")

def main():
    url = input("Enter the YouTube video URL: ")
    formats = list_formats(url)
    if not formats:
        print("No formats available for this video.")
        return
        
    print("\nDownload options:")
    print("1. Audio only")
    print("2. Video only")
    print("3. Both audio and video")
    
    try:
        download_type_choice = int(input("Enter the number of your desired download type: "))
    except ValueError:
        print("Invalid input. Please enter a number (1, 2, or 3).")
        return

    output_path = input("Enter the download directory (leave empty for current directory): ") or os.getcwd()

    if download_type_choice == 1:
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
        download_video(url, format_code, output_path)

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
        download_video(url, format_code, output_path)

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
        download_video(url, format_code, output_path)

    else:
        print("Invalid download type selected.")

if __name__ == "__main__":
    main()
