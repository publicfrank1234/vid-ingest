import yt_dlp


def fetch_loom_metadata(url):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        metadata = {
            "url": url,
            "title": info_dict.get("title", "Loom Video"),
            "description": info_dict.get("description", "Loom Video Description"),
        }
    return metadata


def download_loom_video(url, output_path="."):
    ydl_opts = {
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def loom_handler(url):
    metadata = fetch_loom_metadata(url)
    download_loom_video(url)
    return metadata


if __name__ == "__main__":
    loom_handler(
        "https://www.loom.com/share/aeebbb5f18044bd2a99ee63155c67e83?sid=9b633243-f4bb-41bb-aa2b-ceee17266449"
    )
