from airflow.decorators import task

from handlers.clari_handler import clari_handler
from handlers.google_handler import google_handler
from handlers.loom_handler import loom_handler
from handlers.mindtickle_handler import mindtickle_handler
from handlers.vimeo_handler import vimeo_handler
from handlers.youtube_handler import youtube_handler
from handlers.zoom_handler import zoom_handler

handlers = {
    "google": google_handler,
    "youtube": youtube_handler,
    "vimeo": vimeo_handler,
    "zoom": zoom_handler,
    "mindtickle": mindtickle_handler,
    "clari": clari_handler,
    "loom": loom_handler,
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
