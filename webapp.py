import pickle
import streamlit as st
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4023e8c1b9a949050dbcf42eb1d9d4fc&language=en-US"
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path', '')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return "https://via.placeholder.com/500"  # Placeholder image if poster is not found
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500"

# Function to recommend movies
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters
    except IndexError:
        st.error("Movie not found in the database.")
        return [], []

# Streamlit application
st.set_page_config(page_title='Movie Recommender System', page_icon=':movie_camera:')
st.title('Movie Recommender System')

# Load data
try:
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except (FileNotFoundError, pickle.UnpicklingError) as e:
    st.error(f"Error loading data: {e}")

# Sidebar selection
st.sidebar.title('Select a Movie')
selected_movie = st.sidebar.selectbox(
    "Choose a movie",
    movies['title'].values
)

# Recommendation button
if st.sidebar.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    if recommended_movie_names:
        st.subheader('Recommended Movies')
        row = st.columns(5)
        for i, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
            with row[i % 5]:
                st.write(f"### {name}")
                st.image(poster, use_column_width=True)

# Footer
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f8f9fa;
    padding: 10px 0;
    text-align: center;
    font-size: 14px;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="footer">Built with ❤️ using Streamlit | Deployed on Heroku</p>', unsafe_allow_html=True)
