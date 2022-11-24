
# -*- coding: utf-8 -*-
import os
import logging
import argparse
import re
import json
import time
from tqdm import tqdm
from datetime import datetime, date, timedelta

import django
import pandas as pd

import requests
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from recsys.models import *


logger = logging.getLogger(__name__)
formatter = logging.Formatter( '%(asctime)s [%(levelname)s] %(name)s - %(message)s')
streamHandler = logging.StreamHandler()
fileHandler = logging.FileHandler('./log/crawler_error.log')
streamHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)
logger.setLevel(level=logging.DEBUG)

KEY0 = ['55ecc158fe343b87a908bc715b2b01e9', '606dfeaadb537f0ec49555952ce80435', '58bad83915361d537ea6be2d08e7cabc', 
        'Rf8TrWXhEkUQCRyjaqVj:ZzhoiEkqHm', '14f08e812b76f7e3ab6ab5282c7041af', 'd8e83471b7c2d23edf815b21d2c69d0c', 
        'a5e50f1780755aabef0e68307c276620']
KEY1 = ['Jbum6L5q5_8xTmPfAKxP:HR89_EvzD2', 'LnhJeaFGnxynnOOAXl4L:yPDFu5nXlK', 'N6XWa1VyIDua7NkQXgWl:AVOILEc8E4']
URL0 = 'https://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key='
URL1 = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key='
URL2 = 'https://openapi.naver.com/v1/search/movie.json'


def str2dt(s, format="%Y%m%d"):
    return datetime.strptime(s, format).date()

def dt2str(dt, format="%Y%m%d"):
    return dt.strftime(format)

def date_range(start_dt='20221120', end_dt=''):
    delta = timedelta(days=1)
    start_date = str2dt(start_dt)
    if end_dt:
        end_date = str2dt(end_dt)
    else:
        end_date = date.today() - delta * 14
    
    date_range = []
    while start_date <= end_date:
        date_range.append(dt2str(start_date))
        start_date += delta
        
    return date_range[::-1]

columns = ['movieNm', 'salesAmt', 'salesShare', 'salesInten', 'salesChange', 'salesAcc', 
           'audiCnt', 'audiInten', 'audiChange', 'audiAcc', 'scrnCnt', 'showCnt', 'datetime']
movie_info_list = []
i = 0
pbar = tqdm(date_range('20100101'))
for dt in pbar:
    pbar.set_description(dt)
    try:
        req_url = URL0 + KEY0[i] + '&targetDt=' + dt
        res = requests.get(req_url)
        movie_list = json.loads(res.text)['boxOfficeResult']['dailyBoxOfficeList']
    except:
        i += 1
        req_url = URL0 + KEY0[i] + '&targetDt=' + dt
        res = requests.get(req_url)
        movie_list = json.loads(res.text)['boxOfficeResult']['dailyBoxOfficeList']
    for idx, movie in enumerate(movie_list):
        movie_info_list.append([movie[col] for col in columns[:-1]] + [dt])

df = pd.DataFrame(movie_info_list, columns=columns)
df[columns[1:-1]] = df[columns[1:-1]].astype(float)
df = df.sort_values(by=['movieNm', 'audiAcc'], ascending=False)
df = df.drop_duplicates(subset='movieNm', keep='first').reset_index(drop=True)
df.to_excel('audiacc_temp.xlsx')

for i in range(len(df)):
    title = df.loc[i, 'movieNm']
    dt = str2dt(df.loc[i, 'datetime'])
    movie_list = MovieInfo.objects.filter(title=title)
    movie_list = sorted(movie_list, key=lambda x: dt - str2dt(x.openDate))
    if movie_list:
        movie = movie_list[0]
        movie.salesAmount = df.loc[i, 'salesAmt']
        movie.salesShare = df.loc[i, 'salesShare']
        movie.salesInten = df.loc[i, 'salesInten']
        movie.salesChange = df.loc[i, 'salesChange']
        movie.salesAcc = df.loc[i, 'salesAcc']
        movie.audiCnt = df.loc[i, 'audiCnt']
        movie.audiInten = df.loc[i, 'audiInten']
        movie.audiChange = df.loc[i, 'audiChange']
        movie.audiAcc = df.loc[i, 'audiAcc']
        movie.scrnCnt = df.loc[i, 'scrnCnt']
        movie.showCnt = df.loc[i, 'showCnt']
        movie.save()
    else:
        print(title)

##############################################################

# i = 0
# pbar = tqdm(range(2010, 2023))
# for y in pbar:
#     pbar.set_description(str(y))
#     while i < len(KEY0):
#         try:
#             req_url = URL1 + KEY0[i] + '&prdtStartYear={}'.format(y)
#             res = requests.get(req_url)
#             n_movie = json.loads(res.text)['movieListResult']['totCnt']
#             break
#         except:
#             i += 1
#     n_page = n_movie // 10 + bool(n_movie % 10)
#     for page in range(1, n_page + 1):
#         while i < len(KEY0):
#             try:
#                 url_0 = URL1 + KEY0[i] + '&openStartDt={}&itemPerPage=10&curPage={}'.format(y, page)
#                 res_0 = requests.get(url_0)
#                 data_0_list = json.loads(res_0.text)['movieListResult']['movieList']
#                 break
#             except:
#                 i += 1
#         for data_0 in data_0_list:
#             if '성인물(에로)' in data_0['genreAlt'].split(',') or \
#                 data_0['movieNm'][-3:] == '무삭제' or data_0['movieNm'][-4:] == '무삭제판' or \
#                 not data_0['directors'] or data_0['prdtStatNm'] != '개봉':
#                 continue
#             # data_0 : 영화진흥원 데이터(제목, 장르, 감독 데이터)
#             title = data_0['movieNm']
#             genres = data_0['genreAlt']
#             nation = data_0['repNationNm']
#             prod_date = data_0['prdtYear']
#             open_date = data_0['openDt']
#             companys = '|'.join(map(lambda x: x['companyNm'], data_0['companys']))
            
#             m = MovieInfo(
#                 # data_0
#                 title=title,
#                 genres=genres,
#                 nation=nation,
#                 prodDate=open_date,
#                 openDate=open_date,
#                 companys=companys,
                
#                 actors = '',
#                 directors = '',
#                 poster = '',
#                 link = '',

#                 ratingAudi = 0,
#                 ratingCritic = 0,
#                 ratingNetizen = 0,
#                 summaryContent = '',
#                 summaryNote = '',
#                 ratingNetizenM = 0,
#                 ratingNetizenF = 0,
#                 ratingNetizen10 = 0,
#                 ratingNetizen20 = 0,
#                 ratingNetizen30 = 0,
#                 ratingNetizen40 = 0,
#                 ratingNetizen50 = 0,
#                 ratingAudiM = 0,
#                 ratingAudiF = 0,
#                 ratingAudi10 = 0,
#                 ratingAudi20 = 0,
#                 ratingAudi30 = 0,
#                 ratingAudi40 = 0,
#                 ratingAudi50 = 0,
#                 ratingNetizenDir = 0,
#                 ratingNetizenAct = 0,
#                 ratingNetizenScn = 0,
#                 ratingNetizenMis = 0,
#                 ratingNetizenOst = 0,
#                 ratingAudiDir = 0,
#                 ratingAudiAct = 0,
#                 ratingAudiScn = 0,
#                 ratingAudiMis = 0,
#                 ratingAudiOst = 0,
                
#                 salesAmount = 0,
#                 salesShare = 0,
#                 salesInten = 0,
#                 salesChange = 0,
#                 salesAcc = 0,
#                 audiCnt = 0,
#                 audiInten = 0,
#                 audiChange = 0,
#                 audiAcc = 0,
#                 scrnCnt = 0,
#                 showCnt = 0,
#             )
#             m.save()

##############################################################

# def country_code(country):
#     if country == '프랑스': return 'FR'
#     elif country == '영국': return 'GB'
#     elif country == '홍콩': return 'HK'
#     elif country == '일본': return 'JP'
#     elif country == '한국': return 'KR'
#     elif country == '미국': return 'US'
#     else: return 'ETC'

# def char_filter(s):
#     return re.sub('[^A-Za-z0-9가-힣]', '', s)

# def search_title(movie, movie_res):
#     title = movie.title
#     title2 = movie_res['title']
#     title_res = ''.join(''.join(title2.split('<b>')[1:]).split('</b>')[:-1])
#     len_title = len(char_filter(title_res))
#     len_not_title = len(title2) - 7 * title2.count('<b>') - len_title
#     prodyear = int(str(movie.prodDate)[:4])
#     pub_date = 0 if not movie_res['pubDate'] else int(movie_res['pubDate'])
#     return abs(len(char_filter(title)) - len_title), len_not_title, prodyear-pub_date

# def get_text(tag, idx=-1, slice_to=None, type='str', para=False):
#     if tag and len(tag) > idx:
#         if idx == -1:
#             text = tag.text[:slice_to]
#         else:
#             text = tag[idx].text[:slice_to]
#         if para:
#             text = text.replace('\r', ' ').replace('\xa0', '').replace('  ', ' ')
#         if type == 'int':
#             return int(text)
#         elif type == 'float':
#             return float(text)
#         else:
#             return text
#     else:
#         if type == 'str':
#             return ''
#         else:
#             return 0

# headers = {
#     'Host': 'openapi.naver.com',
#     'User-Agent': 'curl/7.49.1',
#     'Accept': '*/*',
#     'X-Naver-Client-Id': KEY1[0].split(':')[0],
#     'X-Naver-Client-Secret': KEY1[0].split(':')[1]
# }

# i = 0
# pbar = tqdm(MovieInfo.objects.all())
# for movie in pbar:
#     pbar.set_description(movie.title)
#     # 영화 제목 기준으로 네이버 검색 api로 request
#     title = movie.title
#     country = country_code(movie.nation)
#     while i < len(KEY1) - 1:
#         try:
#             params = {'query': title, 'country': country, 'display':100}
#             res_1 = requests.get(URL2, headers=headers, params=params)
#             data_1_list = json.loads(res_1.text)['items']
#             data_1_list = list(filter(lambda x: '<b>' in x['title'], data_1_list))
#             if not data_1_list:
#                 params = {'query': title, 'display':100}
#                 res_1 = requests.get(URL2, headers=headers, params=params)
#                 data_1_list = json.loads(res_1.text)['items']
#             break
#         except:
#             i += 1
#             print(i)
#             print(KEY1[i].split(':'))
#             headers['X-Naver-Client-Id'] = KEY1[i].split(':')[0]
#             headers['X-Naver-Client-Secret'] = KEY1[i].split(':')[1]
#     data_1_list = list(filter(lambda x: '<b>' in x['title'], data_1_list))
#     if not data_1_list:
#         continue
#     movie_res = sorted(data_1_list, key=lambda x: search_title(movie, x))[0]
#     time.sleep(0.25)
#     # if title != movie_res['title'][3:-4]:
#     #     logger.info(f'{title}    {movie_res["title"]}')

#     actors = movie_res['actor'][:-1]
#     directors = movie_res['director'][:-1]
#     poster = movie_res['image']
#     link = movie_res['link']

#     # data_2 : 네이버영화 데이터(평점, 누적관객수)
#     res_2 = requests.get(link)
#     soup = BeautifulSoup(res_2.text, 'html.parser')
#     genre_tags = soup.select('dl.info_spec dd > p a')
#     if not genre_tags or genre_tags[0].text == '에로':
#         continue
#     rating_audi_tag = soup.select('#actualPointPersentBasic > div > em')[:4]
#     rating_audi = 0 if not rating_audi_tag else float(''.join([tag.text for tag in rating_audi_tag]))
#     rating_critic_tag = soup.select('a.spc > div > em')[:4]
#     rating_critic = 0 if not rating_critic_tag else float(''.join([tag.text for tag in rating_critic_tag]))
#     rating_netizen_tag = soup.select('#pointNetizenPersentBasic > em')[:4]
#     rating_netizen = 0 if not rating_netizen_tag else float(''.join([tag.text for tag in rating_netizen_tag]))
    
#     summary_content_tag = soup.find('p','con_tx')
#     summary_content = get_text(summary_content_tag, para=True)
#     summary_note_tag = soup.find(id='makingnotePhase')
#     summary_note = get_text(summary_note_tag)
    
#     res_3 = requests.get(link.replace('basic', 'point'))
#     soup = BeautifulSoup(res_3.text, 'html.parser')
    
#     rating_group = soup.find_all('strong', 'graph_point')
#     rating_netizen_m = get_text(rating_group, 0, type='float')
#     rating_netizen_f = get_text(rating_group, 1, type='float')
#     rating_netizen_10 = get_text(rating_group, 2, type='float')
#     rating_netizen_20 = get_text(rating_group, 3, type='float')
#     rating_netizen_30 = get_text(rating_group, 4, type='float')
#     rating_netizen_40 = get_text(rating_group, 5, type='float')
#     rating_netizen_50 = get_text(rating_group, 6, type='float')
    
#     rating_audi_m = get_text(rating_group, 7, type='float')
#     rating_audi_f = get_text(rating_group, 8, type='float')
#     rating_audi_10 = get_text(rating_group, 9, type='float')
#     rating_audi_20 = get_text(rating_group, 10, type='float')
#     rating_audi_30 = get_text(rating_group, 11, type='float')
#     rating_audi_40 = get_text(rating_group, 12, type='float')
#     rating_audi_50 = get_text(rating_group, 13, type='float')
    
#     rating_film = soup.find_all('span', 'grp_score')
#     rating_netizen_dir = get_text(rating_film, 0, -1, type='int')
#     rating_netizen_act = get_text(rating_film, 1, -1, type='int')
#     rating_netizen_scn = get_text(rating_film, 2, -1, type='int')
#     rating_netizen_mis = get_text(rating_film, 3, -1, type='int')
#     rating_netizen_ost = get_text(rating_film, 4, -1, type='int')
    
#     rating_audi_dir = get_text(rating_film, 5, -1, type='int')
#     rating_audi_act = get_text(rating_film, 6, -1, type='int')
#     rating_audi_scn = get_text(rating_film, 7, -1, type='int')
#     rating_audi_mis = get_text(rating_film, 8, -1, type='int')
#     rating_audi_ost = get_text(rating_film, 9, -1, type='int')
    
#     movie.actors = actors
#     movie.directors = directors
#     movie.poster = poster
#     movie.link = link
#     movie.ratingAudi = rating_audi
#     movie.ratingCritic = rating_critic
#     movie.ratingNetizen = rating_netizen
#     movie.summaryContent = summary_content
#     movie.summaryNote = summary_note
#     movie.ratingNetizenM = rating_netizen_m
#     movie.ratingNetizenF = rating_netizen_f
#     movie.ratingNetizen10 = rating_netizen_10
#     movie.ratingNetizen20 = rating_netizen_20
#     movie.ratingNetizen30 = rating_netizen_30
#     movie.ratingNetizen40 = rating_netizen_40
#     movie.ratingNetizen50 = rating_netizen_50
#     movie.ratingAudiM = rating_audi_m
#     movie.ratingAudiF = rating_audi_f
#     movie.ratingAudi10 = rating_audi_10
#     movie.ratingAudi20 = rating_audi_20
#     movie.ratingAudi30 = rating_audi_30
#     movie.ratingAudi40 = rating_audi_40
#     movie.ratingAudi50 = rating_audi_50
    
#     movie.ratingNetizenDir = rating_netizen_dir
#     movie.ratingNetizenAct = rating_netizen_act
#     movie.ratingNetizenScn = rating_netizen_scn
#     movie.ratingNetizenMis = rating_netizen_mis
#     movie.ratingNetizenOst = rating_netizen_ost
#     movie.ratingAudiDir = rating_audi_dir
#     movie.ratingAudiAct = rating_audi_act
#     movie.ratingAudiScn = rating_audi_scn
#     movie.ratingAudiMis = rating_audi_mis
#     movie.ratingAudiOst = rating_audi_ost
#     movie.save()












