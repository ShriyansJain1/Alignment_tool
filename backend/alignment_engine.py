import numpy as np
from sklearn.cluster import KMeans

def optimize(df, n_territories):

    coords = df[['lat', 'lon']].values

    kmeans = KMeans(n_clusters=n_territories, random_state=42, n_init=10)
    labels = kmeans.fit_predict(coords)

    return dict(zip(df['zip'], labels))