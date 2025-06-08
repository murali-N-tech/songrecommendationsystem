# main.py
import streamlit as st
from spotify_api import get_spotify_client
from recommender import SpotifyRecommender

st.set_page_config(page_title="Spotify Music Recommender", layout="centered")
st.title("🎧 Spotify Music Recommender")
st.markdown("Find similar songs based on your favorite track! Powered by Spotify and machine learning.")

# Load Spotify API and model
sp = get_spotify_client()
recommender = SpotifyRecommender("SpotifyFeatures.csv")

# Search and Select Song
query = st.text_input("🔎 Enter a song name:")
if query:
    results = sp.search(q=query, type='track', limit=5)
    track_options = [f"{item['name']} - {item['artists'][0]['name']}" for item in results['tracks']['items']]
    selected_track = st.selectbox("🎵 Select a song to base recommendations on:", track_options)

    if st.button("✨ Get Recommendations"):
        song_name = selected_track.split(" - ")[0]
        with st.spinner("Finding recommendations..."):
            status, recs = recommender.recommend(song_name)
        st.success(status)

        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("#### Recommended Songs")
            st.dataframe(recs, use_container_width=True)
        with col2:
            for item in results['tracks']['items']:
                if item['name'] == song_name:
                    st.markdown("#### Album Art")
                    st.image(item['album']['images'][0]['url'], width=250)
                    st.markdown(f"**{item['name']}**  \n{item['artists'][0]['name']}")
                    break

st.markdown("---")
st.caption("Made with ❤️ using Streamlit and Spotify API")
