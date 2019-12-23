### 거룩한 크롤링
### written by Lee, Taeyoon. 2019.07.03
import os
import sys
import requests 
import re
from bs4 import BeautifulSoup
from crawlingtools import *
url_head = 'http://maria.catholic.or.kr/bible/read/bible_read.asp'
url_tail = '?m={promise}&n={book}&p={chapter}'
url_pattern = url_head + url_tail

m= [1,2]              ### 구약,신약
n_1 = range(101, 147) ### 창세기부터 즈카르야서
n_2 = range(147, 174) ### 마태오부터 요한묵시록까지
total_bible = [n_1, n_2] # 구/ 신약

###############################################################
SAVE_ROOT = "/mnt/data2/sunkist/projects/crawling/static/data"
###############################################################
# 성경 문장수
num_bible_sen = 0
###############################################################
# 주소 패턴
mp3_pattern = r"(?<=mp3:\")http://archive[.]catholic[.]or[.]kr/agent/read[.]asp[?]book=bible&oldnew=soriold&kwon=[\d]+&jang=[\d]+&filenm=[\d]+_[\d]+_[\d]+\.mp3"
mp3_pattern_new = r"(?<=mp3:\")http://archive[.]catholic[.]or[.]kr/agent/read[.]asp[?]book=bible&oldnew=sorinew&kwon=[\d]+&jang=[\d]+&filenm=[\d]+_[\d]+_[\d]+\.mp3"
filename_pattern = r"(?<=filenm=).*"
###############################################################

# get sentence list
def get_sentence_list(response):
    td_list = select_by(response, '.al')
    chap_sentences = []
    for td in td_list:
    	if td.get("id") != "j":
    		chap_sentences.extend(td.select('.lineheight_chg'))
    raw_sentences = [sen.text.replace("\r","").replace("\n","").replace("\t","").strip() for sen in chap_sentences]
    return raw_sentences

###############################################################

# get mp3 list
def get_mp3_list(response):
    raw_mp3_list = re.findall(mp3_pattern, str(response.content))
    mp3_list = [mp3.replace("\\r","").replace("\\n","").replace("\\t","").strip() for mp3 in raw_mp3_list]
    file_mp3_list = [re.findall(filename_pattern,mp3)[0] for mp3 in mp3_list]
    return mp3_list, file_mp3_list

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

# write mp3
def write_mp3(path, url_list, name_list):
    for mp3_index, mp3_url in enumerate(url_list):
        r = requests.get(mp3_url, stream=True)
        if r.status_code == 200:
            book_mp3_path = os.path.join(promise_path, "mp3s", name_list[mp3_index])
            with open(book_mp3_path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
    return

###############################################################

# 총 문장수
total_num_sentence = 0

def count_up():
	global total_num_sentence
	total_num_sentence += 1
	return total_num_sentence

for i, prom in enumerate(total_bible):
    # 구약 신약 디렉토리 생성
    promise_path = os.path.join(SAVE_ROOT,"{}".format(i))
    readme_path = os.path.join(promise_path ,"README.md")
    os.makedirs(promise_path, exist_ok=True)

    for j in prom:
        # 창세기 ~ 즈카르야 생성

        # 책 총 장수 구하기
        response = requests.get(url_pattern.format(promise=i+1,book=j,chapter=1))
        my_titles = select_by(response, '.audio_tt > span')
        page_list = select_by(response, '.page_list')[0].select('span > a')
        print(my_titles)

        # 책 절별 문장 txt
        book_text_path = os.path.join(promise_path, "{}.txt".format(j))
        with open(readme_path, 'a') as f:
            f.write("{} : ".format(j) + my_titles[0].text + "\n")


        ### 각 성경별 장
        for chap in get_href_list(page_list):
            print("### {} 장 ###".format(chap.split("=")[-1]))
            chap_url = url_head + chap
            chap_response = requests.get(chap_url)    # ~기 ~장

            # 문장 리스트
            raw_sentences = get_sentence_list(chap_response)

            # mp3 리스트
            mp3_list, file_mp3_list = get_mp3_list(chap_response)

            num_sen = len(raw_sentences)
            num_prom_sen += num_sen

            # 문장 쓰기
            write_text(book_text_path, raw_sentences, count_up)

            # mp3 쓰기
            # write_mp3(promise_path, mp3_list, file_mp3_list)


    print("총 문장수 : ", total_num_sentence)