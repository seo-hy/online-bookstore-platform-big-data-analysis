import csv
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def aladin(url):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)

    platform_soup = BeautifulSoup(driver.page_source, 'html.parser')

    price = platform_soup.select_one("#Ere_prod_allwrap > div.Ere_prod_bookwrap > div.Ere_prod_Binfowrap > div > div > ul > li > div.Ritem.Ere_ht11 > span.Ere_fs24").string
    price = int(price.replace(",",""))

    star = platform_soup.select_one("#wa_product_top1_wa_Top_Ranking_pnlRanking > div.info_list.Ere_fs15.Ere_ht18 > a.Ere_sub_pink.Ere_fs16.Ere_str").string
    star = float(star)

    rev_100 = platform_soup.select_one(
        "#wa_product_top1_wa_Top_Ranking_pnlRanking > div.info_list.Ere_fs15.Ere_ht18 > a:nth-child(5)").string
    rev = platform_soup.select_one(
        "#wa_product_top1_wa_Top_Ranking_pnlRanking > div.info_list.Ere_fs15.Ere_ht18 > a:nth-child(7)").string
    rev_100 = rev_100[6:-1]
    rev = rev[3:-1]
    num_of_review = int(rev_100)+int(rev)

    return price, star, num_of_review

def kyobo(url):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)

    platform_soup = BeautifulSoup(driver.page_source, 'html.parser')
    price = platform_soup.select_one("#container > div:nth-child(4) > form > div.box_detail_order > div.box_detail_price > ul > li:nth-child(1) > span.sell_price > strong").string
    price = int(price.replace(",",""))

    star = platform_soup.select_one("#container > div:nth-child(4) > form > div.box_detail_point > div.review > div > div > em").string
    star = float(star)
    num_of_review = platform_soup.select_one(
        "#book_info > li > a > span").string
    num_of_review=int(num_of_review[1:-1])
    return price, star, num_of_review
def yes24(url):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)

    platform_soup = BeautifulSoup(driver.page_source, 'html.parser')

    price = platform_soup.select_one("#yDetailTopWrap > div.topColRgt em.yes_m").string
    price = int(price[:-1].replace(",",""))

    star = platform_soup.select_one("#spanGdRating > a > em").string
    star = float(star)

    num_of_review = platform_soup.select_one(
        "#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_ratingArea > span.gd_reviewCount > a > em").string

    return price, star, int(num_of_review)

def interpark(url):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)

    platform_soup = BeautifulSoup(driver.page_source, 'html.parser')

    price = platform_soup.select_one("#inc_optionWrap > div.optionRight_wrap > div.lastTotalWrap > div.lastTotal_tab > ul > li > div > p.tt_price > span.price").string
    price = int(price.replace(",",""))

    star = platform_soup.select_one("#reviewGradeWrap > h3:nth-child(2) > div.titleSet1 > span.star_count").string
    star = float(star)

    num_of_review = platform_soup.select_one(
        "#reviewGradeWrap > h3:nth-child(2) > div.titleSet1 > span.total_count").string

    num_of_review = int(num_of_review[3:-2])
    return price, star, int(num_of_review)
