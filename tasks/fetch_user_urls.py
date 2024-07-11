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
        {
            "url": "https://us05web.zoom.us/clips/share/1qKe_m7qvUeMN3sRDvv1-YiWiE-N7rCv8_RW6rAmUnz2jw6Sh_nPP9_20cGYkmNfJ4n7Tw6wS2RLHZoBi1QJ_lnoUg.AjbHNFxALSen5ByE",
            "handler": "zoom",
        },
        {
            "url": "https://boostup.callai.mindtickle.com/external/recording/2392245020868898900?activeMenuKey=transcription&activeMenuKey=comments",
            "handler": "mindtickle",
        },
        {
            "url": "https://copilot.clari.com/guest/sharedCall/668ef26154bbb72f4d082819",
            "handler": "clari",
        },
        {
            "url": "https://www.loom.com/share/aeebbb5f18044bd2a99ee63155c67e83?sid=9b633243-f4bb-41bb-aa2b-ceee17266449",
            "handler": "loom",
        },
    ]
