import os

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def fetch_mindtickle_metadata(url):
    # Using Selenium to open the browser and fetch the page
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
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
                "#root > section > div.sc-cvdZrU.eYrywk > div > div > div.sc-dYCqDv.hGvin.externalTitle",
            )
        )
    )
    title = title_element.text.strip() if title_element else "MindTickle Video"

    description = "MindTickle Video Description"

    metadata = {
        "url": url,
        "title": title,
        "description": description,
    }

    driver.quit()
    return metadata


def download_mindtickle_video(url, output_path="."):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    video_element = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "#root > section > main > div > div > div > div > div > div > div.video-internal-wrapper.video-player > div.sc-lmOJGc.gKpAww._videoRoot.sc-hcCorJ.cPyDCr > div:nth-child(1) > div > video",
            )
        )
    )
    video_url = video_element.get_attribute("src") if video_element else None

    driver.quit()

    if not video_url:
        raise Exception("Could not find video download URL")

    # Handle relative URLs by appending the scheme
    if video_url.startswith("//"):
        video_url = "https:" + video_url

    video_response = requests.get(video_url, stream=True)
    video_response.raise_for_status()
    file_path = os.path.join(output_path, "mindtickle_video.mp4")
    with open(file_path, "wb") as f:
        for chunk in video_response.iter_content(chunk_size=8192):
            f.write(chunk)
    return file_path


def mindtickle_handler(url):
    metadata = fetch_mindtickle_metadata(url)
    file_path = download_mindtickle_video(url)
    return metadata, file_path


if __name__ == "__main__":
    mindtickle_handler(
        "https://boostup.callai.mindtickle.com/external/recording/2392245020868898900?activeMenuKey=transcription&activeMenuKey=comments"
    )
