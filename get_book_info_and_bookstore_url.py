import csv
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse


category_file_name = 'book_category.csv'
# 동적으로 생성되는 값이 있어 selenium 이용
chrome_options = webdriver.ChromeOptions()

# 크롬창 숨기기 옵션 추가
chrome_options.add_argument("headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

bookstore = ["알라딘","인터넷 교보문고","예스24","인터파크 도서"]
# 카테고리 정보 csv 읽어서 저장하기
category = list()
with open(category_file_name, "r",  encoding = "UTF-8") as f:
    rdr = csv.reader(f)
    for line in rdr:
        category.append(line)

book_info_file_name = "book_info_and_bookstore_url.csv"

with open(book_info_file_name, "w", encoding = "UTF-8") as f:
    f.write("main_category,sub_category,book_id,book_title,aladin,kyobo,yes24,interpark\n")
    for i in range(1, len(category)): # 첫 칸 헤더 제외
        main_category = category[i][0]
        sub_category = category[i][1]
        url = category[i][2]

        # 서브 카테고리별 top 100 & 플랫폼별 주소 가져오기
        # for i in range(1,6): # 20개씩 5페이지로 구성되어있다 ## DEMO 5개씩만 가져옴
        j = 1
        driver.get(url+"&page="+str(j))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        detail_a_list = soup.select("#category_section > ol > li > div > div > a")
        cnt = 0
        for detail_a in detail_a_list:
            if(cnt == 5):
                break
            try:
                cnt+=1
                # 네이버 책 도서 상세정보에서 책 정보와 서점 링크 가져오기
                bookstore_url_dict = dict()
                detail_url = detail_a.attrs['href']
                driver.get(detail_url)
                detail_soup = BeautifulSoup(driver.page_source, 'html.parser')

                book_id = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(detail_url).query))["bid"]
                book_cover = detail_soup.select_one("#container > div.spot > div.book_info > div.thumb.type_end > div > a > img").attrs['src']
                book_title = detail_soup.select_one("#container > div.spot > div.book_info > div.thumb.type_end > div > a > img").attrs['alt']
                book_title = book_title.replace(",","")
                img_file = urllib.request.urlopen(book_cover).read()
                print(book_id,book_title,book_cover)
                with open("./img/"+book_id+".jpg", mode="wb") as imgf:
                    imgf.write(img_file)

                buy_list = detail_soup.select("#productListLayer > ul > li > div > a:nth-child(1)")
                for a in buy_list:
                    if(len(bookstore_url_dict) ==4):
                        break
                    bookstore_name = a.string
                    if(bookstore_name in bookstore):
                        if(not (bookstore_name in bookstore_url_dict.keys())):
                            bookstore_url_dict[bookstore_name] = a.attrs['href']
                if(len(bookstore_url_dict) != 4):
                    print("[제외] " + bookstore_url_dict.keys())
                    continue

                # url이 redirect url로 되어있어서 고치기
                decode_val =dict(urllib.parse.parse_qsl(urllib.parse.urlparse(bookstore_url_dict[bookstore[0]]).query))["u"]
                bookstore_url_dict[bookstore[0]] = urllib.parse.urljoin("https://www.aladin.co.kr", urllib.parse.unquote(decode_val))
                bookstore_url_dict[bookstore[1]] =bookstore_url_dict[bookstore[1]][bookstore_url_dict[bookstore[1]].find("next_url")+9:]
                bookstore_url_dict[bookstore[2]] =dict(urllib.parse.parse_qsl(urllib.parse.urlparse(bookstore_url_dict[bookstore[2]]).query))["ReturnURL"]
                tmp_query = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(bookstore_url_dict[bookstore[3]]).query))
                bookstore_url_dict[bookstore[3]] =tmp_query["url"]+"&sc.prdNo="+tmp_query["sc.prdNo"]

                print(bookstore_url_dict)
                f.write(main_category+","+sub_category+","+str(book_id)+","+book_title+","+bookstore_url_dict[bookstore[0]]+","+bookstore_url_dict[bookstore[1]]+","+bookstore_url_dict[bookstore[2]]+","+bookstore_url_dict[bookstore[3]]+"\n")

            except Exception as e:
                print("[에러]",e)
                continue


