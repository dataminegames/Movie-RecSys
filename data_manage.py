import os
import logging
import argparse
import json
from tqdm import tqdm
from datetime import datetime

import django

import requests
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from recsys.models import *


def get_table(table):
    if table == 'movieinfo':
        return MovieInfo
    elif table == 'moviechoice':
        return MovieChoice
    elif table == 'userprofile':
        return UserProfile
    elif table == 'userlike':
        return UserLike

def count(table):
    print(table.objects.all().count())

def delete(table, table_name, year):
    print('start deleting...')
    for i in range(3):
        user_input = input(f'Delete data from {year}? [y/n]: ')
        if user_input.lower() in ['n', 'no']:
            return
        elif user_input.lower() in  ['y', 'yes']:
            break
    dt = datetime(year, 1, 1)
    if table_name == 'movieinfo':
        data = table.objects.filter(open_date__gte=year).delete()
    elif table_name == 'moviechoice':
        data = table.objects.filter(movie__open_date__gte=year).delete()
    elif table_name == 'userprofile':
        data = table.objects.filter(vote_date__gte=dt).delete()
    elif table_name == 'userlike':
        data = table.objects.filter(user__vote_date__gte=dt).delete()
    print('successfully done.')

def drop_duplicates(table):
    print('start updating...')
    for row in tqdm(table.objects.all().reverse()):
        if table.objects.filter(title=row.title).count() > 1:
            row.delete()
    print('successfully done.')

def crawl(table, year):
    FLAG = False
    # KEY0 = '33c7f7950fd16de47c3bac55eae8ae3c'
    KEY0 = '58bad83915361d537ea6be2d08e7cabc'
    # KEY1 = 'Jbum6L5q5_8xTmPfAKxP:HR89_EvzD2'
    # KEY1 = 'LnhJeaFGnxynnOOAXl4L:yPDFu5nXlK'
    KEY1 = 'N6XWa1VyIDua7NkQXgWl:AVOILEc8E4'
    URL0 = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=' + KEY0
    URL1 = 'https://openapi.naver.com/v1/search/movie.json'

    headers = {
        'Host': 'openapi.naver.com',
        'User-Agent': 'curl/7.49.1',
        'Accept': '*/*',
        'X-Naver-Client-Id': KEY1.split(':')[0],
        'X-Naver-Client-Secret': KEY1.split(':')[1]
    }

    logger = logging.getLogger(__name__)
    formatter = logging.Formatter( '%(asctime)s [%(levelname)s] %(name)s - %(message)s')
    streamHandler = logging.StreamHandler()
    fileHandler = logging.FileHandler('./log/crawler_error.log')
    streamHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    logger.setLevel(level=logging.DEBUG)

    print('start crawling...')
    # 영화진흥원 전체 영화 데이터 조회
    pbar = tqdm(range(year, 2023))
    for y in pbar:
        page = 1
        while True:
            url_0 = URL0 + '&openStartDt={}&curPage={}&itemPerPage=100'.format(y, page)
            res_0 = requests.get(url_0)
            data_0_list = json.loads(res_0.text)['movieListResult']['movieList']
            if not data_0_list:
                break
            for data_0 in data_0_list:
                try:
                    if '성인물(에로)' in data_0['genreAlt'].split(',') \
                        or not data_0['directors'] or data_0['prdtStatNm'] != '개봉':
                        continue
                    # data_0 : 영화진흥원 데이터(제목, 장르, 감독 데이터)
                    title = data_0['movieNm']

                    if title == '엔칸토: 마법의 세계':
                        FLAG = True
                    if FLAG:
                        genres = data_0['genreAlt']
                        companys = '|'.join(map(lambda x: x['companyNm'], data_0['companys']))
                        nation = data_0['repNationNm']
                        open_date = data_0['openDt']
                        
                        # data_1 : 네이버영화 데이터(포스터, 평점, 배우 데이터)
                        res_1 = requests.get(URL1, headers=headers, params={'query': title})
                        # print(json.loads(res_1.text))
                        data_1_list = json.loads(res_1.text)['items']
                        data_1_list = list(filter(lambda x: x['title'][:3] == '<b>' and x['title'][-4:] == '</b>', data_1_list))
                        if not data_1_list:
                            continue
                        data_1 = data_1_list[0]
                        actors = data_1['actor'][:-1]
                        directors = data_1['director'][:-1]
                        poster = data_1['image']
                        link = data_1['link']

                        # data_2 : 네이버영화 데이터(평점, 누적관객수)
                        res_2 = requests.get(link.replace('basic', 'detail'))
                        soup = BeautifulSoup(res_2.text, 'html.parser')
                        genre_tags = soup.select('dl.info_spec dd > p a')
                        if not genre_tags or genre_tags[0].text == '에로':
                            continue
                        rating_audi_tags = soup.select('#actualPointPersentBasic > div > em')[:4]
                        rating_audi = float(''.join([tag.text for tag in rating_audi_tags])) if rating_audi_tags else 0
                        rating_critic_tags = soup.select('a.spc > div > em')[:4]
                        rating_critic = float(''.join([tag.text for tag in rating_critic_tags])) if rating_critic_tags else 0
                        rating_netizen_tags = soup.select('#pointNetizenPersentBasic > em')[:4]
                        rating_netizen = float(''.join([tag.text for tag in rating_netizen_tags])) if rating_netizen_tags else 0
                        audi_acc_tag = soup.select('dl.info_spec > dd:last-child > div > p')
                        audi_acc = int(audi_acc_tag[0].text.split('명')[0].replace(',', '')) if audi_acc_tag else 0
                        
                        pbar.set_description(f'{y} | {title}')
                        

                        # save data
                        m = table(
                            # data_0
                            title=title,
                            genres=genres,
                            nation=nation,
                            open_date=open_date,
                            companys=companys,
                            # data_1
                            actors=actors,
                            directors=directors,
                            poster=poster,
                            link=link,
                            # data_2
                            rating_audi=rating_audi,
                            rating_critic=rating_critic,
                            rating_netizen=rating_netizen,
                            audi_acc=audi_acc
                        )
                        m.save()
                except Exception as e:
                    logger.info(title)
                    logger.debug(e, exc_info=True)
                    return
            page += 1
    print('successfully done.')

def update_top30(table):
    delete(table, 'moviechoice', 2000)
    drop_duplicates(MovieInfo)

    movie_list = MovieInfo.objects.order_by('-audi_acc')[:30]
    for i, movie in enumerate(movie_list):
        m = table(movie=movie, order=i+1)
        m.save()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--do', choices=['count', 'delete', 'drop_dup', 'crawl', 'update_choice'])
    parser.add_argument('-t', '--table', choices=['movieinfo', 'moviechoice', 'userprofile', 'userlike'])
    parser.add_argument('-y', '--year', default="2021", help='Data will be processed from the given year')
    args = parser.parse_args()

    do = args.do
    table = get_table(args.table)
    table_name = args.table
    year = int(args.year)

    if do == 'count':
        count(table)
    elif do == 'delete':
        delete(table, table_name, year)
    elif do == 'drop_dup' and table_name == 'movieinfo':
        drop_duplicates(table)
    elif do == 'crawl' and table_name == 'movieinfo':
        crawl(table, year)
    elif do == 'update_choice' and table_name == 'moviechoice':
        update_top30(table)

if __name__ == "__main__":
    main()