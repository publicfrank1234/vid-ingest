import yt_dlp


def vimeo_handler(url):
    # Replace https: with http: to bypass TLS fingerprint issue
    url = url.replace("https:", "http:")
    # download_vimeo_video(url)
    return fetch_vimeo_video_metadata(url)


def fetch_vimeo_video_metadata(url):
    ydl_opts = {
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_metadata = {
            "id": info.get("id"),
            "title": info.get("title"),
            "description": info.get("description"),
            "url": url,
        }
        return video_metadata


def download_vimeo_video(url, output_path="."):
    ydl_opts = {
        "outtmpl": f"{output_path}/%(id)s.%(ext)s",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        return f'{output_path}/{info_dict["id"]}.{info_dict["ext"]}'


if __name__ == "__main__":
    vimeo_handler("https://vimeo.com/858674286")
