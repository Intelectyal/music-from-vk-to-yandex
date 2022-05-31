from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


print('Логин')
login = input()
print('Пароль')
password = input()
listSong = []
listArtist = []
count = 0

print('Start')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.implicitly_wait(10)
driver.get("https://vk.com/login")
driver.find_element(by=By.CLASS_NAME, value="FlatButton__in").click()
elem = driver.find_element(by=By.NAME, value="login")
elem.send_keys(login)
elem.send_keys(Keys.RETURN)
print('Login')
elem = driver.find_element(by=By.NAME, value="password")
elem.send_keys(password)
elem.send_keys(Keys.RETURN)
print('password')
driver.find_element(by=By.ID, value="l_aud").click()
elem = driver.find_element(By.LINK_TEXT,value='Моя музыка')
elem.click()
driver.refresh()
print('Starting load page')
lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match = False
while (match == False):
    lastCount = lenOfPage
    time.sleep(0.5)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount == lenOfPage:
        match = True
print('End load page')
with open("index.html","w",encoding='utf-8') as file:
    file.write(driver.page_source)

driver.close()
driver.quit()

with open ('index.html', 'r',encoding='utf-8') as f:
  old_data = f.read()

new_data = old_data.replace('<meta http-equiv="content-type" content="text/html; charset=windows-1251">', '<meta http-equiv="content-type" content="text/html; charset=utf-8">')

with open ('index.html', 'w',encoding='utf-8') as f:
  f.write(new_data)
print('Write in file')

with open("index.html",encoding="utf-8") as inf:
    soup = BeautifulSoup(inf.read(),features="lxml")
name_songs = soup.find_all('a',class_='audio_row__title_inner _audio_row__title_inner')
artists = soup.find_all('div',class_='audio_row__performer_title')
for artist in artists:
    count += 1
    if count > 18:
        a = artist.find('div',class_='audio_row__performers').find('a')
        listArtist.append(a.text)
count = 0
for name_song in name_songs:
    count += 1
    if count > 18:
        listSong.append(name_song.text)
file = open("outs.txt", 'w',encoding="utf-8")
a= len(listSong)
for i in range(a):
    file.write(listArtist[i]+' '+listSong[i]+'\n')
file.close()
