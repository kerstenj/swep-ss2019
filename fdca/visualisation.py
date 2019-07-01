import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

def plot_2D(store, x, y):
    fig, ax = plt.subplots()

    temp = store.df["cluster_center"]
    temp[store.df["cluster_center"] == store.df.index] = 1

    ax.scatter(store.df[x],store.df[y],c=temp)
    ax.set_xlabel(x)
    ax.set_ylabel(y)

    ax.grid(True)
    fig.tight_layout()
    plt.show()


def plot_3D(store, x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    temp = store.df["cluster_center"]
    temp[store.df["cluster_center"] == store.df.index] = 1

    ax.scatter(store.df[x],store.df[y],store.df[z],c=temp)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_zlabel(z)

    ax.grid(True)
    fig.tight_layout()
    plt.show()
