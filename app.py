import pickle
import streamlit as st
import requests
import os
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

TMDB_API_KEY = os.environ.get('TMDB_API_KEY', 'd43f04baefd4a1295e4cc1224b256818')  # Fallback for development

def create_requests_session():
    """Create a requests session with retry capabilities"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,  # Total number of retries
        backoff_factor=1,  # Time between retries (1, 2, 4 seconds)
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these HTTP status codes
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    return session

def fetch_poster_and_details(movie_id):
    session = create_requests_session()
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        response = session.get(url, timeout=10)  # Add timeout
        response.raise_for_status()
        data = response.json()
        
        # Handle case where poster might be None
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            full_path = "https://via.placeholder.com/500x750?text=No+Poster+Available"
            
        # Fetch movie details URL
        details_url = f"https://www.themoviedb.org/movie/{movie_id}"
        
        return full_path, details_url
    
    except (requests.RequestException, KeyError, ValueError) as e:
        st.warning(f"Error fetching movie data (ID: {movie_id}): {e}")
        return "https://via.placeholder.com/500x750?text=Error+Loading+Image", "#"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    recommended_movies_accuracy = []
    recommended_movies_details = []

    for i in distances[1:6]:
        try:
            movie_id = movies.iloc[i[0]].movie_id
            poster_url, details_url = fetch_poster_and_details(movie_id)
            recommended_movies_poster.append(poster_url)
            recommended_movies_details.append(details_url)
            recommended_movies_name.append(movies.iloc[i[0]].title)
            recommended_movies_accuracy.append(round(i[1] * 100, 2))
            # Small delay to avoid overwhelming the API
            time.sleep(0.1)
        except Exception as e:
            st.error(f"Error processing movie recommendation: {e}")
            # Add placeholder data when an error occurs
            recommended_movies_poster.append("https://via.placeholder.com/500x750?text=Error")
            recommended_movies_details.append("#")
            recommended_movies_name.append("Error loading movie")
            recommended_movies_accuracy.append(0)
    
    return recommended_movies_name, recommended_movies_poster, recommended_movies_accuracy, recommended_movies_details

st.header("MOVIE RECOMMENDATION SYSTEM")

@st.cache_resource
def load_data():
    """Cache the data loading to improve performance"""
    movies_data = pickle.load(open('movie_list.pkl', 'rb'))
    similarity_data = pickle.load(open('similarity.pkl', 'rb'))
    return movies_data, similarity_data

# Load data with caching
try:
    movies, similarity = load_data()
    movies_list = movies['title'].values
    selected_movie = st.selectbox('Type a movie name', movies_list)

    if st.button('Show recommendation'):
        with st.spinner('Getting recommendations...'):
            recommended_movies_name, recommended_movies_poster, recommended_movies_accuracy, recommended_movies_details = recommend(selected_movie)

        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]
        
        for i in range(5):
            with cols[i]:
                st.markdown(f"""
                <div style="text-align: center; word-wrap: break-word; width: 150px; white-space: pre-wrap;">
                    <p style="margin-bottom: 10px;">{recommended_movies_name[i]}</p>
                    <a href="{recommended_movies_details[i]}" target="_blank" style="text-decoration:none;">
                        <img src="{recommended_movies_poster[i]}" style="width: 100%; height: auto;">
                    </a>
                    <p style="margin-top: 10px;">Accuracy: {recommended_movies_accuracy[i]}%</p>
                </div>
                """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Failed to load application data: {e}")