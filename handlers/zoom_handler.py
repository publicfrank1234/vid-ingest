import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def fetch_zoom_metadata(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    title_element = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "#mv-share > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(3) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > span > span",
            )
        )
    )
    title = title_element.text.strip() if title_element else "Zoom Video"

    description = "Zoom Video Description"

    metadata = {
        "url": url,
        "title": title,
        "description": description,
    }

    driver.quit()
    return metadata


def download_zoom_video(url, output_path="."):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the actual video download URL
    video_url = None

    # For recordings
    for link in soup.find_all("a"):
        if "download" in link.get("href", ""):
            video_url = link["href"]
            break

    # If not found in <a> tags, check for <source> tags (common in clips)
    if not video_url:
        for source in soup.find_all("source"):
            if "video/mp4" in source.get("type", ""):
                video_url = source["src"]
                break

    if not video_url:
        raise Exception("Could not find video download URL")

    video_response = requests.get(video_url, stream=True)
    video_response.raise_for_status()
    file_path = os.path.join(output_path, "zoom_video.mp4")
    with open(file_path, "wb") as f:
        for chunk in video_response.iter_content(chunk_size=8192):
            f.write(chunk)
    return file_path


def zoom_handler(url):
    metadata = fetch_zoom_metadata(url)
    file_path = download_zoom_video(url)
    return metadata, file_path


def is_zoom_clip(url):
    return "clips" in url


if __name__ == "__main__":
    public_zoom_url = "https://us05web.zoom.us/clips/share/1qKe_m7qvUeMN3sRDvv1-YiWiE-N7rCv8_RW6rAmUnz2jw6Sh_nPP9_20cGYkmNfJ4n7Tw6wS2RLHZoBi1QJ_lnoUg.AjbHNFxALSen5ByE"

    if is_zoom_clip(public_zoom_url):
        print("Detected a Zoom clip.")
    else:
        print("Detected a Zoom recording.")

    metadata, file_path = zoom_handler(public_zoom_url)
    print(f"Metadata: {metadata}")
    print(f"Video downloaded to: {file_path}")
