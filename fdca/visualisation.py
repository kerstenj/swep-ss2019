import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

def plot(store):
    # 2d:
    # fig, ax = plt.subplots()

    # 3d:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    temp = store.df["cluster_center"]
    temp[store.df["cluster_center"] == store.df.index] = 1

    # Aggregation:
    # Axes3D.scatter(xs, ys, zs=0, zdir='z', s=20, c=None, depthshade=True, *args, **kwargs)
    # ax.scatter(store.df["x"], store.df["y"], c=temp)
    #
    # ax.set_xlabel('x')
    # ax.set_ylabel('y')

    # Iris subtable:
    ax.scatter(store.df["sepal length"],store.df["sepal width"],store.df["petal length"],c=store.df["class"])
    ax.set_xlabel('sepal length')
    ax.set_ylabel('sepal width')

    ax.grid(True)
    fig.tight_layout()
    plt.show()
