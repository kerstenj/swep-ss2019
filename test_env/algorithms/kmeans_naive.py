import pandas as pd
import numpy as np
import random

def euclidean_distance(a, b):
    result = 0
    for i in len(a):
        result = result + (a[i] - b[i])**2

    return np.sqrt(result)


def get_random_centroids(df, k):
    centroids = []

    while len(centroids) < k:
        idx = random.randint(0, len(df.index)-1)

        if idx in centroids: continue
        else: centroids.append(idx)

    return centroids


def assign_to_centroids(df, centroids):
    assigned = pd.Series([-1 for _ in range(len(df.index))], index=df.index)

    for index, row in df.iterrows():
        # Calculate nearest center
        min_index = -1
        min_dist = np.inf
        for center in centroids:
            dist = euclidean_distance(row, df[center])

            if dist < min_dist:
                min_dist = dist
                min_index = center

        assigned[index] = min_index

    return assigned


def execute(df, k):
    # Algorithm Step-by-Step explanation
    # https://mubaris.com/posts/kmeans-clustering/

    centroids = get_random_centroids(df, k)
    assigned = assign_to_centroids(df, centroids)

    df['center_index'] = assigned

    print(df)
