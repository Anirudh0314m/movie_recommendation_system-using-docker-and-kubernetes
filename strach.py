import pickle
import streamlit as st
import requests

TMDB_API_KEY = 'b6cd9ca2e1212f1ec7d96aed3564ffe8'

def fetch_poster_and_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=3ea1a0325e4ab61f5692a12c4da2d55d".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "http://image.tmdb.org/t/p/w500/" + poster_path

    # Fetch movie details URL
    details_url = f"https://www.themoviedb.org/movie/{movie_id}"
    
    return full_path, details_url

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])) , reverse=True , key = lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    recommended_movies_accuracy = []
    recommended_movies_details = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster_url, details_url = fetch_poster_and_details(movie_id)
        recommended_movies_poster.append(poster_url)
        recommended_movies_details.append(details_url)
        recommended_movies_name.append(movies.iloc[i[0]].title)
        recommended_movies_accuracy.append(round(i[1] * 100, 2))
 
    
    return recommended_movies_name, recommended_movies_poster, recommended_movies_accuracy,recommended_movies_details

st.header("MOVIE RECOMMENDATION SYSTEM")
movies = pickle.load(open('movie_list.pkl' , 'rb'))
similarity = pickle.load(open('similarity.pkl','rb'))



movies_list = movies['title'].values
selected_movie = st.selectbox('Type a movie name',movies_list)


if st.button('Show recommendation'):
    recommended_movies_name, recommended_movies_poster, recommended_movies_accuracy,recommended_movies_details = recommend(selected_movie)

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