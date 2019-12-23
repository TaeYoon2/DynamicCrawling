# static 초기 버전
import os
import sys
import requests
from crawlingtools import *
from bs4 import BeautifulSoup
root_URL = 'https://brunch.co.kr'
URI = '/magazine'
URL = root_URL + URI


response = requests.get(URL)
my_titles = select_by(response, '.list_menu > li > a')
sub_URIs = get_href_list(my_titles)

# writer_list
writer_list = []

for uri in sub_URIs:
    url = root_URL + uri
    res = requests.get(url)
    magazines = select_by(res, '.list_more > li > a')
    magazine_hrefs = get_href_list(magazines)

    # 요일별 매거진
    for magazine_href in magazine_hrefs:
        m_url = root_URL + magazine_href
        print(m_url)
        swriter = requests.get(m_url)
        writers = select_by(swriter, '.list_article > li > a')
        writer_hrefs =  get_href_list(writers)

        # 해당 요일의 작가별 매거진
        for writer_href in writer_hrefs:
            writer = writer_href.split('/')[1]
            no = writer_href.split('/')[-1]

            writer_path = os.path.abspath(os.path.join(os.path.dirname(__file__), writer))

            # 기존 생성된 작가 디렉토리가 없으면
            # 새로 생성
            if writer not in writer_list:
                os.mkdir(writer_path)
                writer_list.append(writer)
            w_url = root_URL + writer_href
            article = requests.get(w_url)
            title = select_by(article, '.wrap_cover > .cover_item > .cover_cell > .cover_title')
            sub_title = select_by(article, '.wrap_cover > .cover_item > .cover_cell > .cover_sub_title')
            body_text = [x.get_text() for x in select_by(article, '.wrap_body')]

            # article 저장
            with open(writer_path+"/"+no+'.txt', mode='a', encoding='utf-8') as f:
                f.write(title[0].get_text()+"\n")
                f.write(sub_title[0].get_text()+"\n")
                for body in body_text:
                    f.write(body)