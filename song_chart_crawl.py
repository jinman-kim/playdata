from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as BS
import time

# url = "https://vibe.naver.com/track/54692454"
# driver = webdriver.Chrome()
# time.sleep(2)
# driver.get(url)
# driver.maximize_window()
# time.sleep(1)
#
# app > div.modal > div > div > a.btn_close
# driver.find_element(By.CSS_SELECTOR, "end_section section_lyrics").click()
# driver.find_element(By.CSS_SELECTOR, "#content > div.end_section.section_lyrics > a").send_keys(Keys.ENTER)
# time.sleep(3)

# bs = BS(driver.page_source)
# print(bs.find("div", {'class' : "end_section section_lyrics"}).find("p").text)


chart = "https://vibe.naver.com/chart/total"
driver = webdriver.Chrome()
#get은 url 접근
driver.get(chart)
#page_source는 페이지 html 다갖고옴
chart_bs = BS(driver.page_source)
#그래서 BS에 넣고 태그와 클래스로 찾기 시작
# chart_bs.find("div", class_ = "tracklist").findAll("td", {"class" : "song"})[0].find("a")['href'].split("/")[-1]
total = []
for x in chart_bs.find("div", class_="tracklist").findAll("td", {"class" : "song"}):
    total.append(x.find("a")['href'].split("/")[-1])

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

global title, artist, lyric

def get_lyrics(song_id):

    global title, artist,lyric
    song_url = f"https://vibe.naver.com/track/{song_id}"
    driver.get(song_url)
    time.sleep(0.5)
    title = driver.find_element(By.CLASS_NAME, 'title').text.split('곡명\n')[-1]
    artist = driver.find_element(By.CLASS_NAME, 'link_sub_title').text
    lyric = driver.find_element(By.CLASS_NAME, 'lyrics').text

    with open(f'./lyrics/{title} - {artist}.txt', 'w', encoding='utf-8-sig') as f:  # w,r, wb 쓰기로, rb = read_binary 읽기로
        f.write(lyric)


import tqdm
for song_id in tqdm.tqdm(total):
    get_lyrics(song_id)
    print(title+'-'+artist)
