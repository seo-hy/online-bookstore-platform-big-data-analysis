from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import urllib.parse

## 책 카테고리 정보를 담은 book_category.csv 생성

# 동적으로 생성되는 값이 있어 selenium 이용
chrome_options = webdriver.ChromeOptions()

# 크롬창 숨기기 옵션 추가
chrome_options.add_argument("headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 네이버 책 사이트 주소
naver_book_url = "https://book.naver.com/"
driver.get(naver_book_url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

# 메인 카테고리 가져오기
category_a_list= soup.select("#left_category > ul > li > a ")

category_file_name = 'book_category.csv'

# 카테고리 csv 파일 생성
with open(category_file_name, "w", encoding="UTF-8") as f:
    f.write("main_category,sub_category,url\n")

    for a in category_a_list:

        # 중분류 가져오기
        sub_li_list = a.next_sibling.next_sibling.select("li > a")
        tmp_dict = dict()
        for e in sub_li_list:
            f.write(a.string+","+e.string+","+urllib.parse.urljoin(naver_book_url,e.attrs['href'])+"&tab=top100&list_type=list&sort_type=salecount\n")

