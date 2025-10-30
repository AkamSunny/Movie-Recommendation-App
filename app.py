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

# Custom CSS for cinematic background and styling
st.markdown("""
<style>
    /* Main background with cinema theme */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.6)), 
                    url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Header styling */
    h1 {
        color: #FFD700 !important;
        text-align: center;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.8);
        font-weight: bold;
        padding: 20px 0;
        font-size: 3rem !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        border: 2px solid #FFD700;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 15px 40px;
        border: none;
        border-radius: 25px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        transform: translateY(-2px);
    }
    
    /* Movie title text styling */
    .stText {
        color: #FFD700 !important;
        font-weight: bold;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9);
        margin-bottom: 10px;
    }
    
    /* Image container styling */
    img {
        border-radius: 10px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
        transition: transform 0.3s ease;
    }
    
    img:hover {
        transform: scale(1.05);
    }
    
    /* Column spacing */
    [data-testid="column"] {
        padding: 10px;
    }
    
    /* Label styling */
    label {
        color: #FFD700 !important;
        font-weight: bold;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit header
st.header("🎬 Movie Recommender System")

# Movie selection dropdown
selectvalue = st.selectbox("Select or type a movie from the list:", movies_list)


# Recommend function
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