import requests
from bs4 import BeautifulSoup
import lxml.etree
import pandas
import time

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
DOMAIN = "https://maoyan.com"
URL = DOMAIN + "/films?showType=3"



def get_and_save_top10(url):
    response = requests.get(url, headers=HEADER)
    bs = BeautifulSoup(response.text, "html.parser")
    movies = []
    count = 0
    for title_div in bs.find_all("div", attrs={"class": "channel-detail movie-item-title"}):
        if count < 10:
            movie = {}
            count = count+1
            title_a = title_div.find("a")
            movie_title = title_a.text
            movie["title"] = movie_title
            movie_detail_href = DOMAIN + title_a.get("href")
            get_detail(movie_detail_href, movie=movie)
    save(movies)


def get_detail(url, movie={}):
    time.sleep(2)
    # 电影类型
    movie_types = []
    # 上映日期
    movie_date = ""
    response = requests.get(url, headers=HEADER)
    bs = BeautifulSoup(response.text, "html.parser")
    base_div = bs.find("div", attrs={"class": "movie-brief-container"})
    li_info = base_div.find_all("li", attrs={"class": "ellipsis"})
    index = 0
    for base_li in li_info:
        if index == 0:
            for movie_type in base_li.find_all("a"):
                movie_types.append(movie_type.text)
        elif index == len(li_info):
            movie_date = base_li.text
    movie["movie_types"] = movie_types
    movie["movie_date"] = movie_date


def save(movies=[]):
    pand = pandas.DataFrame(movies)
    pand.to_csv("./movie.csv", mode="a+", sep="\n", encoding="utf8")

get_and_save_top10(URL)