import streamlit as st
import pandas as pd
import pickle
import requests
import os

# Function to fetch poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=621b9d742b7de7b7d798e91d78e1dfd7&language=en-US"
        response = requests.get(url)
        if response.status_code != 200:
            return None
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path'] if 'poster_path' in data else None
    except:
        return None

# Recommendation function
def recommend(movie):
    try:
        movie_index = movies[movies["title"] == movie].index[0]
    except IndexError:
        st.error("Selected movie not found in the dataset.")
        return [], []

    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]]['title'])
        poster_url = fetch_poster(movie_id)
        recommended_posters.append(poster_url)

    return recommended_movies, recommended_posters


# File paths
movies_file_path = r"C:\Users\mypc\OneDrive\Desktop\asad\ml project\movie recommendation system\movies_dict.pkl"
similarity_file_path = r"C:\Users\mypc\OneDrive\Desktop\asad\ml project\movie recommendation system\similarity.pkl"

# Load data
if not os.path.exists(movies_file_path) or not os.path.exists(similarity_file_path):
    st.error("Required pickle files not found. Please check the file paths.")
else:
    movies_dict = pickle.load(open(movies_file_path, 'rb'))
    similarity = pickle.load(open(similarity_file_path, 'rb'))
    movies = pd.DataFrame(movies_dict)

    # Streamlit UI
    st.title("🎬 Movie Recommendation System")

    option = st.selectbox('📽️ Select a movie to get recommendations:', movies["title"].values)

    if st.button("🔎 Recommend"):
        with st.spinner("Fetching recommendations..."):
            recommended_movies, recommended_posters = recommend(option)

        if recommended_movies:
            st.subheader(f"🎥 Recommendations for: {option}")
            cols = st.columns(5)

            for i in range(5):
                with cols[i]:
                    st.text(recommended_movies[i])
                    if recommended_posters[i]:
                        st.image(recommended_posters[i])
                    else:
                        st.warning("Poster not available")
            st.success("✅ Recommendations displayed successfully!")
        else:
            st.error("Could not generate recommendations.")
    else:
        st.info("Please select a movie to get recommendations.")
        st.warning("Click the '🔎 Recommend' button to see the results.")
        st.success("Ready to recommend movies!")
