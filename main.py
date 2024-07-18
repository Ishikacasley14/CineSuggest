import pandas as pd
import streamlit as st
import requests
import pickle
import bz2file as bz2

st.set_page_config(
    page_title="CineSuggest",
    page_icon="🎬"
)

def decompress_pickle(file):
    with bz2.BZ2File(file, 'rb') as f:
        data = pickle.load(f)
    return data

# Load data
movies_dict = decompress_pickle('models/movies_dict.pbz2')
movies_df = pd.DataFrame(movies_dict)
similarity = decompress_pickle('models/similarity.pbz2')

st.title('CineSuggest 🎬')

# Function to fetch poster and ratings from TMDB API
def fetch_poster_ratings(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"  # Replace with your TMDB API key
    response = requests.get(url)
    data = response.json()

    if 'vote_average' in data:
        ratings = data['vote_average']
    else:
        ratings = None

    poster_path = data.get('poster_path')
    if poster_path:
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        full_path = None

    return full_path, ratings

# Function to recommend movies based on similarity
def recommend_movies(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    movie_posters = []
    movie_ratings = []
    for i in distances[1:5]:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_df.iloc[i[0]].title)
        p, r = fetch_poster_ratings(movie_id)
        movie_posters.append(p)
        movie_ratings.append(r)

    return recommended_movies, movie_posters, movie_ratings

# Streamlit UI
option = st.selectbox(
    'Select your movie',
    movies_df['title'].values)

if st.button('Get Recommendations'):
    movie_names, movie_posters, movies_ratings = recommend_movies(option)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text(movie_names[0])
        if movie_posters[0]:
            st.image(movie_posters[0])
        if movies_ratings[0]:
            st.caption(f"Rating: {movies_ratings[0]}")
    with col2:
        st.text(movie_names[1])
        if movie_posters[1]:
            st.image(movie_posters[1])
        if movies_ratings[1]:
            st.caption(f"Rating: {movies_ratings[1]}")
    with col3:
        st.text(movie_names[2])
        if movie_posters[2]:
            st.image(movie_posters[2])
        if movies_ratings[2]:
            st.caption(f"Rating: {movies_ratings[2]}")
    with col4:
        st.text(movie_names[3])
        if movie_posters[3]:
            st.image(movie_posters[3])
        if movies_ratings[3]:
            st.caption(f"Rating: {movies_ratings[3]}")
