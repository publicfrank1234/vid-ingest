from airflow.decorators import task


@task
def fetch_user_urls(user_id):
    # Placeholder function to fetch user URLs from a database or API
    return [
        {
            "url": "https://drive.google.com/drive/folders/12ttmcHo1ZShjaYt3AMoJ4J-zWnxrDcxz",
            "handler": "google",
        },
        {
            "url": "https://vimeo.com/858674286",
            "handler": "vimeo",
        },
        {
            "url": "https://www.youtube.com/watch?v=LEjhY15eCx0",
            "handler": "youtube",
        },
        # {
        #     "url": "https://zoom.us/rec/play/example_public_recording",
        #     "handler": "zoom",
        # },
        # {
        #     "url": "https://gong.io/rec/play/example_public_recording",
        #     "handler": "gong",
        # },
    ]
