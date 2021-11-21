from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import win32api
import win32con
from bs4 import BeautifulSoup
import csv
import lxml



driver = webdriver.Chrome()

all_links = []
sneakers = {}
count = 0
def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    sleep(10)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def get_data(page_num):
	link = []
	try:
		driver.get(f'https://stockx.com/sneakers?page={page_num}')
		sleep(9)
		#if 'Please verify you are a human' in driver.page_source:
		#	click(260, 390)
		#	sleep(10)
		if page_num == 1:
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="chakra-modal-1"]/button'))).click()
			sleep(2)
		code = driver.page_source
		#with open(f'project{page_num}.html','w') as file:
		#	file.write(str(code, encoding='utf-8', errors = 'ignore'))
		soup = BeautifulSoup(code, 'lxml')
		links = soup.find_all('div', class_='css-1duh0sd-Tile')
		for item in links:
			link.append('https://stockx.com' + item.find('a').get('href'))
		return link
	except Exception as ex:
		print(ex)


def get_links( n_pages):
	links = []
	for page in range(1, n_pages + 1):
		links.extend(get_data(page))
	return links

def get_items(link):
	try:
		driver.get(link)
		sleep(3)
		if 'Please verify you are a human' in driver.page_source:
			click(260, 390)
		file = driver.page_source
		soup = BeautifulSoup(file, 'lxml')
		try:
			photo = soup.find('div', class_='css-1d8x81o').find('img').get('src')
			name = soup.find('a', class_='css-1x3b5qq').text
		except:
			photo = 'нет фото'
			name = soup.find('a', class_='css-1x3b5qq').text

		return name, photo
	except Exception as ex:
		print(ex)

all_links = get_links(3)



with open('sneakers.csv', 'w', encoding='utf-8', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(('Sneakers', 'Photo_url'))
for link in all_links:
		name, photo = get_items(link)
		sneakers[name] = photo
		with open('sneakers.csv', 'a', encoding='utf-8', newline='') as file:
			writer = csv.writer(file)
			writer.writerow((name, photo))
print(sneakers)