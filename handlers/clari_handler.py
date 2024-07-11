import os

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def fetch_clari_metadata(url):
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
                "#root > div.Dashboard.is-toggled > div.dashboard__content.h-screen > div > div > div.flex.flex-wrap.flex-col.items-center.flex-grow.bg-white.rounded-sm > div > div.Call__ContextContainer__TitleContainer.SharedCall__titleDiv > div > div > div.headerCall__outerDiv > div.headerCall__titleDiv > span",
            )
        )
    )
    title = title_element.text.strip() if title_element else "Clari Video"

    description = "Clari Video Description"

    metadata = {
        "url": url,
        "title": title,
        "description": description,
    }

    driver.quit()
    return metadata


def download_clari_video(url, output_path="."):
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
            (By.CSS_SELECTOR, "#VideoContainer > div > div > video")
        )
    )
    video_url = (
        video_element.find_element(By.TAG_NAME, "source").get_attribute("src")
        if video_element
        else None
    )

    driver.quit()

    if not video_url:
        raise Exception("Could not find video download URL")

    video_response = requests.get(video_url, stream=True)
    video_response.raise_for_status()
    file_path = os.path.join(output_path, "clari_video.mp4")
    with open(file_path, "wb") as f:
        for chunk in video_response.iter_content(chunk_size=8192):
            f.write(chunk)
    return file_path


def clari_handler(url):
    metadata = fetch_clari_metadata(url)
    file_path = download_clari_video(url)
    return metadata, file_path


if __name__ == "__main__":
    clari_handler("https://copilot.clari.com/guest/sharedCall/668ef26154bbb72f4d082819")
