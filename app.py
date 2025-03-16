import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
    """Fetch the movie poster URL using TMDB API."""
    url = (
        "https://api.themoviedb.org/3/movie/{}?api_key="
        "8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    ).format(movie_id)
    
    response = requests.get(url)
    
    if response.status_code != 200:
        st.error("Failed to fetch movie poster.")
        return ""
    
    data = response.json()
    poster_path = data.get('poster_path')
    
    if poster_path:
        return (
            f"https://image.tmdb.org/t/p/w500/{poster_path}"
        )
    else:
        st.warning("Poster not available.")
        return ""


def recommend(movie):
    """Recommend 5 similar movies based on similarity."""
    
    try:
        index = movies[
            movies['title'] == movie
        ].index[0]
    except IndexError:
        st.error("Movie not found.")
        return [], []

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True, key=lambda x: x[1]
    )
    
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(
            movies.iloc[i[0]].title
        )
        recommended_movie_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movie_names, recommended_movie_posters


st.header('Movie Recommender System')

try:
    movies = pickle.load(
        open('movies.pkl', 'rb')
    )
    similarity = pickle.load(
        open('similarity.pkl', 'rb')
    )
except FileNotFoundError:
    st.error(
        "Required data files not found. "
        "Please check 'movies.pkl' and 'similarity.pkl'."
    )

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown", 
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = (
        recommend(selected_movie)
    )

    if recommended_movie_names and recommended_movie_posters:
        cols = st.columns(5)
        
        for idx, col in enumerate(cols):
            with col:
                st.text(recommended_movie_names[idx])
                st.image(recommended_movie_posters[idx])
