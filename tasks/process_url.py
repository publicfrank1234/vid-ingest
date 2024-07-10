from airflow.decorators import task

from handlers.google_handler import google_handler
from handlers.vimeo_handler import vimeo_handler
from handlers.youtube_handler import youtube_handler

handlers = {
    "google": google_handler,
    "youtube": youtube_handler,
    "vimeo": vimeo_handler,
    # "zoom": zoom_handler.sync_zoom_videos,
    # "gong": gong_handler.sync_gong_videos,
}


@task
def process_urls(urls):
    processed_data = []
    for url in urls:
        print(f"processing {url}")
        data = process_url(url.get("url"), url.get("handler"))
        if data:
            processed_data.append(data)
    return processed_data


def process_url(url, handler_key):
    handler = handlers.get(handler_key)
    if handler:
        return handler(url)
    else:
        print(f"No handler found for key: {handler_key}")
        return {"url": url, "status": "no_handler"}
