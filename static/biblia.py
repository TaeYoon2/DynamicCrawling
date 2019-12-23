### 거룩한 크롤링
### written by Lee, Taeyoon. 2019.07.03
import os
import sys
import requests 
import re
from bs4 import BeautifulSoup
from crawlingtools import *
url_head = 'https://www.bibliatodo.com/la-biblia/Reina-valera-2000/'
# url_head = 'view-source:http://maria.catholic.or.kr/bible/read/bible_read.asp'
url_tail = '{libro}-{capitulos}'
url_pattern = url_head + url_tail

##################
# 성경 전체 인덱스 얻기
##################
response = requests.get(url_pattern.format(libro='genesis',capitulos=1))
libros = select_by(response, '#libros > option')

books = [libro.get('id') for libro in libros]


### per book basic
num_capitulos = select_by(response, '#num_capitulos > option')
chapters = [num.get('id') if num.get('id') is not None else '1' for num in num_capitulos]
print(url_pattern.format(libro='genesis',capitulos=1))
print(chapters)

###############################################################
SAVE_ROOT = "/mnt/data2/sunkist/projects/crawling/static/data"
###############################################################
# 성경 문장수
num_bible_sen = 0
###############################################################
# mp3_pattern = r"(?<=mp3:\")http://archive[.]catholic[.]or[.]kr/agent/read[.]asp[?]book=bible&oldnew=soriold&kwon=[\d]+&jang=[\d]+&filenm=[\d]+_[\d]+_[\d]+\.mp3"
# mp3_pattern_new = r"(?<=mp3:\")http://archive[.]catholic[.]or[.]kr/agent/read[.]asp[?]book=bible&oldnew=sorinew&kwon=[\d]+&jang=[\d]+&filenm=[\d]+_[\d]+_[\d]+\.mp3"
# filename_pattern = r"(?<=filenm=).*"
###############################################################
# write text
def write_text(path, sentences, meta_func=None):
    with open(path, 'a') as f:
        for line in sentences:
            f.write(line+"\n")
            # meta (문장수 카운트 업)
            if meta_func is not None:
                meta_func()
    return
###############################################################
# 총 문장수
total_num_sentence = 0

def count_up():
	global total_num_sentence
	total_num_sentence += 1
	return total_num_sentence

###############################################################
for libro in books:
    print(libro)
    book_text_path = os.path.join(SAVE_ROOT, "{}.txt".format(libro))
    readme_path = os.path.join(SAVE_ROOT, "README.md")
    # 창세기 ~ 요한계시록 생성
    response = requests.get(url_pattern.format(libro=libro,capitulos=1))
    ### per book basic
    num_capitulos = select_by(response, '#num_capitulos > option')
    chapters = [num.get('id') if num.get('id') is not None else '1' for num in num_capitulos]

    # 장 정리
    for chapter in chapters:
        # 절 정리
        chap_response = requests.get(url_pattern.format(libro=libro,capitulos=chapter))
        numeros = [numero.parent.text.replace("\r","").replace("\n","").replace("\t","").strip() for numero in select_by(chap_response, 'p > #numeros')]

        # 문장 쓰기
        write_text(book_text_path, numeros, count_up)