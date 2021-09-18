import requests
from bs4 import BeautifulSoup

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'user-agent:': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
               }

def get_newest_movies():
    url = 'https://dy.dytt8.net'
    re = requests.get(url, headers)
    re.encoding = re.apparent_encoding
    html = BeautifulSoup(re.text, 'html.parser')
    trs = html.select('#header > div > div.bd2 > div.bd3 > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(2) > div.co_content8 > ul > table > tr')
    movies = {}
    for tr in trs:
        tds = tr('td')
        td = tds[0]
        ass = td('a')
        if len(ass)>1:
           # print(ass[1]['href'])
            href = ass[1]['href']
            value = ass[1].string
            newest_movie_url = url+href
            newest_movie_name = value
            print('The chosen movie is {0}\n and the download url is {1}'.format(newest_movie_name,newest_movie_url))
            movies.setdefault(newest_movie_name, newest_movie_url)
    print(str(movies))
    return movies

def get_like_movies(movies):
    import json
    delete_movies = []
    for movie, url in movies.items():
        req = requests.get(url, headers)
        req.encoding = req.apparent_encoding
        html = BeautifulSoup(req.text, 'html.parser')
        span = html.select('#Zoom > span')
        text = span[0].text
        if 'IMDb评分' in text:
            IMDB_score = str(text.split('IMDb评分')[1].split('from')[0]).strip().split('/')[0]
        else:
            IMDB_score = 0
        if '豆瓣评分' in text:
            DouBan_score = str(text.split('豆瓣评分')[1].split('from')[0]).strip().split('/')[0]
        else:
            DouBan_score = 0
        du = str(span).split('<a href="')[1].split('"')[0]
        img = str(span).split('img alt="" border="0" src="')[1].split('"')[0]
        print(IMDB_score, DouBan_score, du, img)
        if float(IMDB_score) < 7 and float(DouBan_score) < 7.5:
            delete_movies.append(movie)
        else:
            movies[movie] = {'url': url, 'durl': du, 'IMDB_score': IMDB_score, 'DouBan_score': DouBan_score}
    for movie in delete_movies:
        movies.pop(movie)
    print('今天有喜欢的电影{0}部：{1}'.format(len(movies), json.dumps(movies, ensure_ascii=False)))
    return movies


def notice_people(chosen_movies):
    import send_sms as send
    text = '主人今天有你非常喜欢的电影哦，快来看看吧！\n'+str(chosen_movies)
    phone = '13487082762'
    send.ihuyi_send(text, phone)

def main():
    print('开始进入电影天堂......')
    print('开始获取最新电影......')
    newest_movies = get_newest_movies()
    print('最新电影获取完成......')
    print('选择喜欢的电影中......')
    chosen_movies = get_like_movies(newest_movies)
    print('喜欢的电影已获取......')
    print('发信息通知主人中......')
    #notice_people(chosen_movies)
    print('主人以查收新电影......')
    print('拜拜拜拜拜拜拜拜......')




if __name__ == '__main__':
    main()