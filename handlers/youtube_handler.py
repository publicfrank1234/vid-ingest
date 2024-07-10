import yt_dlp
from pytube import YouTube


def youtube_handler(url):
    # Replace https: with http: to bypass TLS fingerprint issue
    url = url.replace("https:", "http:")
    download_youtube_video(url)
    return fetch_youtube_video_metadata(url)


def fetch_youtube_video_metadata(url):
    yt = YouTube(url)
    video_metadata = {
        "id": yt.video_id,
        "title": yt.title,
        "description": yt.description,
        "url": yt.watch_url,
    }
    return video_metadata


def download_youtube_video(url, output_path="."):
    ydl_opts = {
        "outtmpl": f"{output_path}/%(id)s.%(ext)s",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        return f'{output_path}/{info_dict["id"]}.{info_dict["ext"]}'


if __name__ == "__main__":
    youtube_handler("https://www.youtube.com/watch?v=LEjhY15eCx0")
