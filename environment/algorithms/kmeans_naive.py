import random

import pandas as pd
import numpy as np


def euclidean_distance(vec_a, vec_b):
    result = 0
    for i in range(len(vec_a)):
        result = result + (vec_a.iloc[i] - vec_b.iloc[i])**2

    return np.sqrt(result)


def get_random_centroids(dataframe, count):
    centroids = []

    while len(centroids) < count:
        idx = random.randint(0, len(dataframe.index)-1)
        row = dataframe.iloc[idx]

        if row in centroids:
            continue
        else:
            centroids.append((idx, row))

    return centroids


def assign_to_centroids(dataframe, centroids):
    assigned = pd.Series(
        [-1 for _ in range(len(dataframe.index))],
        index=dataframe.index
    )

    for index, row in dataframe.iterrows():
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


def columns_equal(column_a, column_b):
    for i in range(len(column_a)):
        if column_a.iloc[i] != column_b.iloc[i]:
            return False
    return True


def find_new_centroids(dataframe, centroids):
    new_centroids = []

    for _, centroid in centroids:
        new_centroid = pd.Series(
            [0 for _ in range(len(dataframe.index))],
            index=dataframe.index
        )

    return new_centroids


def execute(dataframe, count):
    # Algorithm Step-by-Step explanation
    # https://mubaris.com/posts/kmeans-clustering/

    # Initial iteration
    centroids = get_random_centroids(dataframe, count)
    dataframe['center_index_old'] = pd.Series(
        [-1 for _ in range(len(dataframe.index))],
        index=dataframe.index
    )
    dataframe['center_index'] = assign_to_centroids(dataframe, centroids)

    i = 0
    while not columns_equal(dataframe['center_index'], dataframe['center_index_old']):
        centroids = find_new_centroids(dataframe, centroids)
        dataframe['center_index_old'] = dataframe['center_index']
        dataframe['center_index'] = assign_to_centroids(dataframe, centroids)

        print(f'Iteration #{i}')
        i += 1

    dataframe.drop('center_index_old', axis=1, inplace=True)
    print(dataframe.to_string())
