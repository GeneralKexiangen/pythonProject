import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import wordcloud
import jieba

st.set_page_config('My Movies!')


@st.cache_data
def get_user_ratings():
    df = pd.read_csv('/Users/zhiyue/Downloads/datasets/movies/archive/ratings.csv')
    return df


data = get_user_ratings()


@st.cache_data
def get_movie_names():
    df = pd.read_csv('/Users/zhiyue/Downloads/datasets/movies/imdb_data_csv/title.csv'
                     , header=None,
                     names=['id', 'title', 'kind_id', 'episode_nr', 'episode_of_id', 'imdb_id', 'imdb_index'
                         , 'md5sum', 'phonetic_code', 'production_year', 'season_nr', 'series_years']
                     , low_memory=False)
    # dt = df.set_index('id').to_dict()['title']
    return df


movie_names = get_movie_names()


@st.cache_data
def get_recommend_list():
    with open('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/moviesRecommend20220405/recommend_list.json', 'r',
              encoding='utf8') as fp:
        jsons = json.load(fp)
        # print(jsons.get('1'))
    return jsons


recommend_list = get_recommend_list()


def fig_movies(all_movies):
    movies_year = all_movies.groupby(['year'])['id'].agg('count').reset_index()
    df = movies_year[movies_year['year'] >= 1900]
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.bar(df['year'], df['id'])
    ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
    plt.title("movies-year")  # 给此图命名标签
    plt.xlabel("year")  # 给x轴命名标签
    plt.ylabel("movies number")  # 给y轴命名标签
    return fig


@st.cache_data
def get_cut_words():
    with open('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/moviesRecommend20220405/words.data', 'r',
              encoding='utf8') as fp:
        content = list(fp)
        # print(jsons.get('1'))
    return ' '.join(content)


content = get_cut_words()


def fig_wc():
    WC = wordcloud.WordCloud(max_words=200, height=600, width=800, background_color='white', repeat=False, mode='RGBA')
    con = WC.generate(content)
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.imshow(con)
    ax.axis("off")
    return fig


st.title("Movies Fields ☕ ")

# menu = ["login"]
if 'count' not in st.session_state:
    st.session_state.count = 0
# st.sidebar.selectbox("choices", menu)
st.sidebar.markdown(
    """
 <style>
 [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
     width: 250px;
 }
 [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
     width: 250px;
     margin-left: -250px;
 }
 </style>
 """,
    unsafe_allow_html=True, )

st.sidebar.subheader("Login Area")
userid = st.sidebar.text_input("UserID")
# password = st.sidebar.text_input("密码", type="password")

if st.sidebar.button("Logging"):
    if userid is not None:
        st.session_state.count += 1
        if st.session_state.count >= 1:
            st.sidebar.success("You have logged successfully，Your userId is {}".format(userid))
            st.balloons()
            # with st.expander("📘 - See More"):
            #     st.write('''''')
            c1, _, c2 = st.columns([16, 1, 8])
            with c1:
                st.header('Watched ')
                df_user = data[data['userId'] == int(userid)]
                # st.dataframe(df_user.style.highlight_max(axis=0))
                st.write('Movie', '&', 'WatchedTime')
                i = 1
                if len(df_user) > 0:
                    for index, row in df_user.iterrows():
                        st.write(str(i) + '. ',
                                 movie_names[movie_names['id'] == int(str(row['movieId']).split('.')[0])][
                                     'title'].values[0], ',',
                                 pd.to_datetime(row['timestamp'], unit='s'))
                        i += 1
                else:
                    st.write('You have not watched any more movies yet!')
                # st.image(None)
            with c2:
                st.header('Recommend ')
                st.text('Movies:')
                recoms = recommend_list.get(str(userid))
                i = 1
                if recoms is not None:
                    for key, value in recoms.items():
                        st.text(
                            str(i) + '. ' + movie_names[movie_names['id'] == int(key.split('.')[0])]['title'].values[0])
                        i += 1
                else:
                    st.text('No movies recommend!')
                # st.image(None)
else:
    all_movies = movie_names[['id', 'title', 'episode_of_id']]
    all_movies.columns = ['id', 'movie', 'year']
    all_movies['year'] = all_movies['year'].fillna(0).astype(int)
    all_movies = all_movies.sort_values(by=['id'])
    all_movies.reset_index(drop=True, inplace=True)
    c1, _, c2, _, c3 = st.columns([16, 1, 16, 1, 16])
    with c1:
        st.write('All movies from every year')
        st.dataframe(all_movies)
    with c2:
        st.write('Movies number every 2decade since 1900')
        st.pyplot(fig_movies(all_movies))
    with c3:
        st.write('Wordcloud about movies name from 2012')
        st.pyplot(fig_wc())