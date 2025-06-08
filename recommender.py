# recommender.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

class SpotifyRecommender:
    def __init__(self, dataset_path):
        self.df = pd.read_csv(dataset_path)

        # Map 'key' from string to int
        self.key_mapping = {
            'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
            'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11
        }
        if self.df['key'].dtype == 'object':
            self.df['key'] = self.df['key'].map(self.key_mapping)

        # Map 'mode' from string to int
        self.mode_mapping = {'Minor': 0, 'Major': 1}
        if self.df['mode'].dtype == 'object':
            self.df['mode'] = self.df['mode'].map(self.mode_mapping)

        # Numeric features used for recommendations
        self.features = ['danceability', 'energy', 'key', 'loudness', 'mode',
                         'speechiness', 'acousticness', 'instrumentalness',
                         'liveness', 'valence', 'tempo']

        self._prepare_model()

    def _prepare_model(self):
        self.scaler = StandardScaler()
        self.df_scaled = self.scaler.fit_transform(self.df[self.features])
        self.model = NearestNeighbors(n_neighbors=6, algorithm='auto')
        self.model.fit(self.df_scaled)

    def recommend(self, track_name):
        if track_name not in self.df['track_name'].values:
            return f"Track '{track_name}' not found in dataset.", []
        idx = self.df[self.df['track_name'] == track_name].index[0]
        track_vector = self.df_scaled[idx].reshape(1, -1)
        distances, indices = self.model.kneighbors(track_vector)
        recommended_indices = indices[0][1:]  # skip the input song itself
        recommendations = self.df.iloc[recommended_indices][['track_name', 'artists', 'genre']]
        return f"Recommendations for '{track_name}':", recommendations
