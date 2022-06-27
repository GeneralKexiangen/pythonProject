import jieba
import pandas as pd
import os


def stopwordslist(stopwords_path):
    stopwords = [line.strip() for line in open(stopwords_path, encoding='UTF-8').readlines()]
    return stopwords


# 常见停用词
chsw = stopwordslist('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/moviesRecommend20220405/stopword.txt')
ensw = stopwordslist('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/moviesRecommend20220405/stopworde.txt')


# 分词去掉停用词
def cut_words(words_list):
    cuts = []
    i = 1
    for word in words_list:
        if type(word) == type('1'):
            words = jieba.cut(word)
            ws = []
            #             print(i,word)
            i += 1
            for w in words:
                if w not in chsw and w not in ensw:
                    ws.append(w)
            cuts.extend(ws)
    return cuts


def get_movie_names():
    df = pd.read_csv('/Users/zhiyue/Downloads/imdb_data_csv/title.csv'
                     , header=None,
                     names=['id', 'title', 'kind_id', 'episode_nr', 'episode_of_id', 'imdb_id', 'imdb_index'
                         , 'md5sum', 'phonetic_code', 'production_year', 'season_nr', 'series_years']
                     , low_memory=False)
    # dt = df.set_index('id').to_dict()['title']
    return df


def get_all_movies():
    movie_names = get_movie_names()
    all_movies = movie_names[['id', 'title', 'episode_of_id']]
    all_movies.columns = ['id', 'movie', 'year']
    all_movies['year'] = all_movies['year'].fillna(0).astype(int)
    all_movies = all_movies.sort_values(by=['id'])
    all_movies.reset_index(drop=True, inplace=True)
    return all_movies


if __name__ == '__main__':
    all_movies = get_all_movies()
    cuts = cut_words(all_movies[all_movies['year'] == 2012]['movie'].to_list())
    if os.path.exists('words.data'):
        os.remove('words.data')
    fp = open('words.data', 'w+', encoding='utf-8');
    fp.write(str(cuts))
    fp.close()
