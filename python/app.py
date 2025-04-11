import streamlit as st
import pandas as pd
import pickle
import requests
import os

# Function to fetch poster
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=621b9d742b7de7b7d798e91d78e1dfd7&language=en-US"
        )
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path'] if 'poster_path' in data else None
    except:
        return None

# Recommendation function
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        id = movies.iloc[i[0]].id # ✅ FIXED
        recommended_movies.append(movies.iloc[i[0]]['title'])  # ✅ Safe way
        recommended_posters.append(fetch_poster(id))

    return recommended_movies, recommended_posters


# File paths
movies_file_path = r"C:\Users\mypc\OneDrive\Desktop\asad\ml project\movie recommendation system\python\movies_dict.pkl"
similarity_file_path = r"C:\Users\mypc\OneDrive\Desktop\asad\ml project\movie recommendation system\python\similarity.pkl"

# Load data
if not os.path.exists(movies_file_path) or not os.path.exists(similarity_file_path):
    st.error("Required pickle files not found. Please check the file paths.")
else:
    movies_dict = pickle.load(open(movies_file_path, 'rb'))
    similarity = pickle.load(open(similarity_file_path, 'rb'))
    movies = pd.DataFrame(movies_dict)

    # Streamlit UI
    st.title("🎬 Movie Recommendation System")

    option = st.selectbox(
        '📽️ Select a movie to get recommendations:',
        movies["title"].values.tolist()
    )

    if st.button("🔎 Recommend"):
        with st.spinner("Fetching recommendations..."):
            recommended_movies, recommended_posters = recommend(option)
        
        st.subheader(f"🎥 Recommendations for: {option}")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.text(recommended_movies[0])
            st.image(recommended_posters[0])
        with col2:
            st.text(recommended_movies[1])
            st.image(recommended_posters[1])
        with col3:
            st.text(recommended_movies[2])
            st.image(recommended_posters[2])
        with col4:
            st.text(recommended_movies[3])
            st.image(recommended_posters[3])
        with col5:
            st.text(recommended_movies[4])
            st.image(recommended_posters[4])

        st.success("✅ Recommendations displayed successfully!")
    else:
        st.info("Please select a movie to get recommendations.")
        st.warning("Click the '🔎 Recommend' button to see the results.")
        st.success("Ready to recommend movies!")
