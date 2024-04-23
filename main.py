from __future__ import annotations

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from time import sleep
from replit import db

from localstorage import LocalStorage

# change this to a website like discord.com to enable LocalStorage
SINGLE_PAGE = ""
LANDING_PAGE = "https://uulanding.vercel.app/"


def is_cookies() -> None:
    return len([key for key in db.keys() if key.isnumeric()]) > 0


def assemble_url(cookie: dict) -> str:
    url = ""

    url += "https://" if cookie["secure"] else "http://"

    url += cookie["domain"].lstrip(".")
    url += cookie["path"]

    return url


def save_cookies(driver: Chrome) -> None:
    print("Saving cookies...", end="")
    try:
        for key in [key for key in db.keys() if key.isnumeric()]:
            del db[key]
        for index, value in enumerate(driver.get_cookies()):
            db[str(index)] = value
    except Exception:
        print("fail")
    else:
        print("done")


def load_cookies(driver: Chrome) -> None:
    print("Loading cookies...", end="")
    try:
        for key in sorted([key for key in db.keys() if key.isnumeric()],
                          key=lambda key: int(key)):
            cookie: dict = db[key]
            # url = assemble_url(cookie)
            # if urlparse(driver.current_url).hostname != urlparse(url).hostname:
            #     driver.get(url)
            driver.add_cookie(dict(cookie))
    except Exception:
        print("fail")
    else:
        print("done")


def is_localstorage() -> None:
    return len([key for key in db.keys() if key.isalpha()]) > 0


def save_localstorage(ls: LocalStorage) -> None:
    print("Saving LocalStorage...", end="")
    try:
        for key, value in ls.items():
            db[key] = value
    except Exception:
        print("fail")
    else:
        print("done")


def load_localstorage(ls: LocalStorage) -> None:
    print("Loading LocalStorage...", end="")
    assert SINGLE_PAGE
    try:
        for key, value in [key for key in db.keys() if key.isalpha()]:
            ls[key] = value
    except Exception:
        print("fail")
    else:
        print("done")


if __name__ == "__main__":
    print("Starting Ultimate Chrome 2...")

    chrome_options = ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'--homepage={LANDING_PAGE}')

    # kiosk
    if SINGLE_PAGE:
        chrome_options.add_argument('--kiosk')
    else:
        chrome_options.add_argument("start-maximized")

    driver = Chrome(options=chrome_options)
    ls = LocalStorage(driver)

    if SINGLE_PAGE:
        driver.get(SINGLE_PAGE)

    if is_cookies():
        print("Found some cookies to restore!")
        load_cookies(driver)

    if SINGLE_PAGE and is_localstorage():
        print("Found some LocalStorage data to restore!")
        load_localstorage(ls)

    if not SINGLE_PAGE:
        driver.get(LANDING_PAGE)
    
    print("Done loading! Stop the repl to save cookies.")

    try:
        while True:
            sleep(60)
            save_cookies(driver)
            if SINGLE_PAGE:
                save_localstorage(ls)
    except KeyboardInterrupt:
        print("Recieved an interrupt! Shutting down...")
    finally:
        save_cookies(driver)
        driver.close()
