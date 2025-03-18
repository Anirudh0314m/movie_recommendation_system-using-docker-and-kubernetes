from fastapi import FastAPI, HTTPException
import pickle
import os

app = FastAPI()

# Load models at startup
movies = pickle.load(open('../movie_list.pkl', 'rb'))
similarity = pickle.load(open('../similarity.pkl', 'rb'))

@app.get("/api/recommend/{movie_title}")
async def get_recommendations(movie_title: str, count: int = 5):
    if movie_title not in movies['title'].values:
        raise HTTPException(status_code=404, detail="Movie not found")
        
    # Your recommendation logic here
    # ...
    
    return {"recommendations": recommended_movies}