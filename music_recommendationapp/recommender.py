import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('music_app/tracks.csv')

# Features to use for recommendation
features = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']

# Normalize
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[features])
df['features'] = list(df_scaled)

def get_recommendations(track_name, top_n=5):
    if track_name not in df['track_name'].values:
        return []

    idx = df[df['track_name'] == track_name].index[0]
    similarities = cosine_similarity([df.iloc[idx]['features']], df['features'].tolist())[0]
    indices = similarities.argsort()[::-1][1:top_n+1]
    return df.iloc[indices][['track_name', 'artist_name', 'language', 'popularity', 'track_url', 'artwork_url']]
