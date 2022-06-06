from http.client import ImproperConnectionState
import requests  # for using API
import pickle
import streamlit as st
import numpy as np
import pandas as pd

df = pickle.load(open('Movies.pkl', 'rb'))
Similarity = pickle.load(open('Similarity_matrix.pkl', 'rb'))

st.title("Movie Recommendation System")

movie_titles = df['title'].values

movie_name = st.selectbox('Tell me, what is your favorite Movie, I will show you more according to that',
                          movie_titles)

# st.write('You selected:', movie_name)

############################# Functions ##############################


def fetch_poster(movie_id):
    # I got it from TMDB, key=api address and movie/id must be required
    respond = requests.get(
        'https://api.themoviedb.org/3/movie/{}%7Bmovie_id%7D?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))

    # this will have json of this url,we will get poster path from this api
    url_of_img = respond.json()
    # https://image.tmdb.org/t/p/w500/kqjL17yufvn9OVLyXYpvtyrFfak.jpg this is the path where I will get Pictures from
    return 'https://image.tmdb.org/t/p/w500/' + url_of_img['poster_path']


def recommend(movie):
    movie_index = df[df.title == movie].index[0]
    distance = sorted(
        list(enumerate(Similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]

    L = []
    recommended_movies_posters = []

    for i in distance:
        # this will get the original movie_id
        movie_id = df.iloc[i[0]].movie_id
        recommended_movies_posters.append(
            fetch_poster(movie_id))  # call upper, find image
        L.append(df.iloc[i[0]].title)
    return L, recommended_movies_posters


if st.button('Recommend me movie'):
    name, poster = recommend(movie_name)
    # for i in name:
    #     st.write(i)
    # A = list(st.columns(5))
    st.snow()

    col0, col1, col2, col3, col4 = st.columns(5)

    for i in range(5):
        with globals()['col%s' % i]:  # for getting the variable by looping
            st.text(name[i])
            st.image(poster[i])

        # with col2:
        #     st.header(name[1])
        #     st.image(poster[1])

        # with col3:
        #     st.header(name[2])
        #     st.image(poster[2])
# st.balloons()
