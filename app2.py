import streamlit as st
import pickle
import requests

# ==================== CONFIG & PAGE STYLING ====================

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

st.markdown("""
    <style>
    /* Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1c1c1c 0%, #111 100%);
        color: white;
    }

    /* Header */
    h1 {
        color: #FFD700;
        text-align: center;
        font-size: 3em;
        font-family: 'Trebuchet MS', sans-serif;
        margin-bottom: 0.2em;
    }

    h3 {
        color: #FFDD00;
    }

    /* Dropdown + Buttons */
    .stSelectbox label, .stButton button {
        font-size: 1.1em !important;
    }

    .stButton>button {
        background-color: #FFD700;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #ffcc00;
        transform: scale(1.05);
    }

    /* Movie Poster Styling */
    .movie-card {
        text-align: center;
        margin: 10px;
    }
    .movie-poster {
        border-radius: 12px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .movie-poster:hover {
        transform: scale(1.08);
        box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================

def fetch_poster(movie_id):
    """Fetch poster image from TMDB API"""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get("poster_path")
        if not poster_path:
            return "https://via.placeholder.com/500x750?text=No+Poster"
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

# ==================== LOAD DATA ====================

movie = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
top_indices = pickle.load(open("indices.pkl", "rb"))

movies_list = movie["title"].values

# ==================== HEADER ====================

st.markdown("<h1>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.write("<p style='text-align:center; font-size:1.2em;'>Find your next favorite movie — powered by AI magic 🍿</p>", unsafe_allow_html=True)

# ==================== MOVIE SELECTOR ====================

selectvalue = st.selectbox("🎞️ Select a Movie", movies_list)

# ==================== RECOMMENDATION FUNCTION ====================

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


# ==================== BUTTON & DISPLAY ====================

if st.button("✨ Recommend Movies"):
    with st.spinner("Finding the best recommendations for you... 🎥"):
        recommend_movie, recommend_poster = recommend(selectvalue)

        st.write("")  # spacing

        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"<div class='movie-card'><img class='movie-poster' src='{recommend_poster[i]}' width='200'><br><b>{recommend_movie[i]}</b></div>", unsafe_allow_html=True)
