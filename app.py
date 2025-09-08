import streamlit as st
import pickle
import pandas as pd
import os

# -------------------- Paths --------------------
BASE_DIR = os.path.dirname(__file__)

# Load preprocessed data and models safely
df = pd.read_pickle(os.path.join(BASE_DIR, "songs_df.pkl"))
tfidf_vectorizer = pickle.load(open(os.path.join(BASE_DIR, "tfidf_vectorizer.pkl"), "rb"))
cosine_sim = pickle.load(open(os.path.join(BASE_DIR, "cosine_sim.pkl"), "rb"))

# -------------------- Recommendation Function --------------------
def recommend(song_title):
    # Clean song names for matching
    df['song_clean'] = df['song'].str.strip().str.lower()
    song_title_clean = song_title.strip().lower()

    # Check if song exists
    if song_title_clean not in df['song_clean'].values:
        return ["❌ Song not found in database"]

    # Get index
    idx = df[df['song_clean'] == song_title_clean].index[0]

    # Compute similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # top 5

    # Return recommended songs
    song_indices = [i[0] for i in sim_scores]
    return df['song'].iloc[song_indices].tolist()

# -------------------- Streamlit UI --------------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-family: 'Trebuchet MS', sans-serif;
    }
    h1 {
        text-align: center;
        color: #ffdd59;
        font-size: 40px;
        margin-bottom: 10px;
    }
    .recommendation {
        background: #ffffff;
        color: #2c3e50;
        padding: 12px;
        margin: 8px 0;
        border-radius: 12px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        font-size: 18px;
        font-weight: 500;
    }
    .subtitle {
        text-align: center;
        font-size: 20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🎵 Music Recommendation System")
st.markdown("<p class='subtitle'>Discover new songs based on your favorite tracks</p>", unsafe_allow_html=True)

# Song selection
song_list = df['song'].values
selected_song = st.selectbox("🎶 Select a song you like:", song_list)

# Recommend button
if st.button("✨ Recommend"):
    recommendations = recommend(selected_song)
    st.write("## 🎧 Recommended Songs:")
    for i, rec in enumerate(recommendations, start=1):
        st.markdown(f"<div class='recommendation'>{i}. 🎶 {rec}</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;'>Made with ❤️ by <b>Chetna</b></p>", unsafe_allow_html=True)
