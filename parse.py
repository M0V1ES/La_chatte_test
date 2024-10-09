import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from database import engine, CinemaBase
import time

# Настройка Selenium
def settings():
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    return driver
def open_chrome(driver):
    # Открываем страницу
    driver.get("https://www.imdb.com/list/ls042235283/")
    time.sleep(5)  # Даем время для загрузки
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Прокручиваем вниз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Даем время для загрузки

        # Проверяем новую высоту страницы
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Считываем HTML
    src = driver.page_source
    driver.quit()
    return src
def create_film(film: CinemaBase) -> None:
    with Session(engine) as session:
        session.add(film)
        session.commit()
        session.refresh(film)
def parse_html(src):
    # Парсим HTML
    soup = BeautifulSoup(src, 'html.parser')
    title = soup.find('ul', attrs={'ipc-metadata-list'}).find_all('h3', attrs={'ipc-title__text'})
    description = soup.find('ul', attrs={'ipc-metadata-list'}).find_all('div', attrs={'ipc-html-content-inner-div'})
    raiting = soup.find('ul', attrs={'ipc-metadata-list'}).find_all('span', attrs={'ipc-rating-star--rating'})
    img = soup.find('ul', attrs={'ipc-metadata-list'}).find_all('img', attrs={'ipc-image'})
    for i in range(0,len(title)):
        response = requests.get(img[i]['src'])
        with open(f"img/{i+1}photo.jpg",'wb') as f:
            f.write(response.content)
        film = CinemaBase(title=title[i].get_text().split(". ")[1],description=description[i].get_text(),raiting=raiting[i].get_text(), photo=f"img/{i+1}photo.jpg")
        create_film(film)
def main():
    setting=settings()
    html = open_chrome(setting)
    parse_html(html)

