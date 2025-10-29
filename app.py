import streamlit as st
import pickle
import requests


# Function to fetch movie poster using TMDB API
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get("poster_path")
        if not poster_path:
            return "https://via.placeholder.com/500x750?text=No+Poster"
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception as e:
        print("Poster fetch failed:", e)
        return "https://via.placeholder.com/500x750?text=Error"


# Load movie data and similarity matrices
movie = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
top_indices = pickle.load(open("indices.pkl", "rb"))

movies_list = movie["title"].values

# Streamlit header
st.header("🎬 Movie Recommender System")

# Movie selection dropdown
selectvalue = st.selectbox("Select or type a movie from the list:", movies_list)


# Recommend function (fixed indentation + correct logic)
def recommend(movie_title):
    index = movie[movie["title"] == movie_title].index[0]
    distance = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda vector: vector[1]
    )

    recommend_movie = []
    recommend_poster = []

    for i in distance[:5]:
        actual_idx = top_indices[index][i[0]]
        recommend_movie.append(movie.iloc[actual_idx].title)
        recommend_poster.append(fetch_poster(actual_idx))

    return recommend_movie, recommend_poster


# Button action
if st.button("Recommend"):
    recommend_movie, recommend_poster = recommend(selectvalue)

    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(recommend_movie[i])
            st.image(recommend_poster[i], width=140)
