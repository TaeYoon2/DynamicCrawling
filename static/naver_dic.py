# 네이버 사전 검색
import os
import sys
import requests
from crawlingtools import *
from bs4 import BeautifulSoup
root_URL = 'https://brunch.co.kr'
URI = '/magazine'
URL = root_URL + URI

url_pattern = 'https://terms.naver.com/entry.nhn?docId={docId}'
tail = '&cid={cid}&categoryId={categooryId}'

for i in range(100000):
    response = requests.get(url_pattern.format(docId=i))
    # CSS Selector를 통해 html요소들을 찾아낸다.
    print(response.text)
    print(response.url)
# my_titles = select_by(response, '.list_menu > li > a')
# sub_URIs = get_href_list(my_titles)

# writer_list
writer_list = []