# crawlingtools
from bs4 import BeautifulSoup


# BeautifulSoup으로 html소스를 python객체로 변환하기
# 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시.
# 이 글에서는 Python 내장 html.parser를 이용했다.
def select_by(res, selector):
    soup = BeautifulSoup(res.text, 'html.parser')
    sobj = soup.select(selector)
    return sobj

def find_by(res, string):
    soup = BeautifulSoup(res.text, 'html.parser')
    sobj = soup.find_all('a', string)
    return sobj

def find_by_re(res, string):
    soup = BeautifulSoup(res.text, 'html.parser')
    sobj = soup.find_all(string)
    return sobj


def get_href_list(sobj_list):
    href_list = [x.get('href') for x in sobj_list ]
    return href_list

def get_text_list(sobj_list):
    href_list = [x.get('href') for x in sobj_list ]
    return href_list