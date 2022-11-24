
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

title_list = [
    '명량',
    '극한직업',
    '신과함께-죄와 벌',
    '국제시장',
    '어벤져스: 엔드게임',
    '겨울왕국 2',
    '베테랑',
    '도둑들',
    '7번방의 선물',
    '범죄도시 2',
    '알라딘',
    '광해, 왕이 된 남자',
    '택시운전사',
    '부산행',
    '변호인',
    '인터스텔라',
    '보헤미안 랩소디',
    '검사외전',
    '관상',
    '해적: 바다로 간 산적',
    '스파이더맨: 파 프롬 홈',
    '최종병기 활',
    '한산: 용의 출현',
    '럭키',
    '곡성',
    '숨바꼭질',
    '더 테러 라이브',
    '검은 사제들',
    '완벽한 타인',
    '쿵푸팬더 2',
    '인사이드 아웃',
    '봉오동 전투',
    '남산의 부장들',
    '내 아내의 모든 것',
    '다만 악에서 구하소서',
    '건축학개론',
    '너의 이름은.',
    '라라랜드',
    '어바웃 타임',
    '마녀',
    '가장 보통의 연애',
    '곤지암',
    '히트맨',
    '사바하',
    '미니언즈2'
]

for ord, title in enumerate(title_list):
    movie = MovieInfo.objects.filter(title=title).order_by('audiAcc')[0]
    print(movie)
    m = MovieChoice(movie=movie, order=ord)
    m.save()