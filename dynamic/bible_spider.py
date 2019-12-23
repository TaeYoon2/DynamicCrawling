#!/bin/python
### written by Lee, Taeyoon. 2019.07.15
# -*- coding: utf-8 -*-
import os
import json
import requests
from time import sleep
from random import randint
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class BibleSpider():
	def __init__(self):
		self.url_to_crawl = "https://listen.talkingbibles.org/en/language/spa"
		self.save_root = "/mnt/data2/sunkist/projects/crawler/"
		self.book_finder = "item list-item-anthology"
		self.chap_finder = "item list-item-chapter"
		self.capitulos = []
		self.sub_urls = []
		self.page_items = []
		self.page_nums = 0

	# Open headless chromedriver
	def start_driver(self):
		print('starting driver...')
		self.display = Display(visible=0, size=(800, 600))
		self.display.start()

		# 크롬 드라이버 옵션 설정
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_argument('window-size=1920x1080')
		options.add_argument("disable-gpu")
		options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
		profile = {"download.default_directory" : save_root,
					"download.prompt_for_download": False,
					"download.directory_upgrade": True}
		options.add_experimental_option("prefs", profile)
		options.add_argument("--disable-extensions")
		options.add_argument("--disable-print-preview")
		# options.add_argument("lang=ko_KR") # 한국어!

		# 네트워크 로그 저장 기능 추가
		caps = DesiredCapabilities.CHROME
		caps['loggingPrefs'] = {'performance': 'ALL'}

		# 드라이버 불러오기
		self.driver = webdriver.Chrome("/var/chromedriver/chromedriver", chrome_options=options, desired_capabilities=caps)
		sleep(4)

	# Close chromedriver
	def close_driver(self):
		print('closing driver...')
		self.display.stop()
		self.driver.quit()
		print('closed!')


	# Batch process
	def batch_process(self, items, func):
		for source_item in items:
			func(source_item)


	# Tell the browser to get a page
	def get_page(self, url):
		print('getting page...')
		self.driver.get(url)
		sleep(randint(2,3))

	# 브라우저 단위 로그 처리
	def process_browser_log_entry(self, entry):
		response = json.loads(entry['message'])['message']
		return response

	# 동적 자바스크립트 네트워크 응답 검색
	def dynamic_search(self, pattern):
		# 브라우저 로그 정보 획득
		browser_log = self.driver.get_log('performance')
		events = [self.process_browser_log_entry(entry) for entry in browser_log]
		# 네트워크 응답 로그 정보 획득
		events = [event for event in events if 'Network.response' in event['method']]
		# url 정보 획득
		events = [event['params']['response']['url'] for event in events]
		# 해당 패턴이 포함된 주소 정보 획득
		events = [event if pattern in event else None for event in events]
		return events

	# 옵션 : 로그인
	def login(self):
		print('getting pass the gate page...')
		try:
			form = self.driver.find_element_by_xpath('//*[@class="signup-login-form"]')
			form.find_element_by_xpath('.//*[@class="user-input email"]').send_keys('iam@alexhoang.net')
			form.find_element_by_xpath('.//*[@class="user-input zip-code"]').send_keys('94011')
			form.find_element_by_xpath('.//*[@class="large orange button"]').click()
			sleep(randint(3,5))
		except Exception:
			pass

	# 클래스가 일치하는 a 태그 리스트 검색
	def grab_list_items(self, finder):
		print(finder)
		list_items = self.driver.find_elements_by_xpath('//a[@class="{}"]'.format(finder))

		# for download urls
		self.page_items = []
		return list_items

	# 미사용
	def get_pages_num(self, tag):
		href = tag.get_attribute("href")
		print("###", href)
		return href

	# 다운로드 링크를 얻어와 저장
	def process_download(self, tag):
		print("# capitulos")
		# 오디오 재생 클릭
		out = self.driver.execute_script("arguments[0].click();", tag)

		# Audio 응답이 오기까지 대기
		sleep(1)

		# Audio 리소스 주소 검색
		audios = self.dynamic_search('cloudfront.net')

		for audio in audios:
			if audio not in self.page_items and audio is not None:
				self.page_items.append(audio)
				# url 정보 parsing
				info_url = audio.split('?')[0].split('/')
				mp3 = info_url[-1]
				folder_name = info_url[-2]
				folder_path = os.path.join(self.save_root, folder_name)
				print(folder_path)

				# make chapter folder
				os.makedirs(folder_path, exist_ok=True)

				# get mp3
				r = requests.get(audio, stream=True)
				if r.status_code == 200:
					book_mp3_path = os.path.join(folder_path, mp3)
					with open(book_mp3_path, 'wb') as f:
						for chunk in r.iter_content(1024):
							f.write(chunk)


	def parse(self):
		# 브라우저 드라이버 시작
		self.start_driver()
		# 페이지 시작
		self.get_page(self.url_to_crawl)
		# 로그인(옵션)
		# self.login()
		# 성경 책 리스트
		book_list = self.grab_list_items(self.book_finder)
		self.page_nums = len(book_list)
		# 성경 각 책별 장 리스트
		for i in range(self.page_nums):
			books = self.grab_list_items(self.book_finder)
			# 해당 태그 클릭
			self.driver.execute_script("arguments[0].click();", books[i])
			chapters = self.grab_list_items(self.chap_finder)
			# 성경 각 장별로 음성 저장
			for chap in chapters:
				self.process_download(chap)
			# 이전 페이지로 이동
			self.driver.back()
		# 브라우저 드라이버 종료
		self.close_driver()


if __name__ == '__file__':
	# Run spider
	bible = BibleSpider()
	bible.parse()