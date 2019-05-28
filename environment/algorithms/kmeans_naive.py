import pandas as pd
import numpy as np
import random

def euclidean_distance(a, b):
    result = 0
    for i in range(len(a)):
        result = result + (a.iloc[i] - b.iloc[i])**2

    return np.sqrt(result)


def get_random_centroids(df, k):
    centroids = []

    while len(centroids) < k:
        idx = random.randint(0, len(df.index)-1)
        row = df.iloc[idx]

        if row in centroids: continue
        else: centroids.append( (idx,row) )

    return centroids


def assign_to_centroids(df, centroids):
    assigned = pd.Series([-1 for _ in range(len(df.index))], index=df.index)

    for index, row in df.iterrows():
        # Calculate nearest center
        min_index = -1
        min_dist = np.inf
        for centroid_index, centroid in centroids:
            dist = euclidean_distance(row, centroid)

            if dist < min_dist:
                min_dist = dist
                min_index = centroid_index

        assigned[index] = min_index

    return assigned


def columns_equal(a, b):
    for i in range(len(a)):
        if a.iloc[i] != b.iloc[i]: return False
    return True


def find_new_centroids(df, centroids):
    new_centroids = []

    for centroid_index, centroid in centroids:
        new_centroid = Series([0 for _ in range(len(df.index))], index=df.index)

    return new_centroids


def execute(df, k):
    # Algorithm Step-by-Step explanation
    # https://mubaris.com/posts/kmeans-clustering/

    # Initial iteration
    centroids = get_random_centroids(df, k)
    df['center_index_old'] = pd.Series([-1 for _ in range(len(df.index))], index=df.index)
    df['center_index'] = assign_to_centroids(df, centroids)

    i = 0
    while not columns_equal(df['center_index'], df['center_index_old']):
        centroids = find_new_centroids(df, centroids)
        df['center_index_old'] =  df['center_index']
        df['center_index'] = assign_to_centroids(df, centroids)

        print(f'Iteration #{i}')
        i += 1

    df.drop('center_index_old', axis=1, inplace=True)
    print(df.to_string())