import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

def plot_2D(store, x="x", y="y"):
    fig, ax = plt.subplots()

    temp = store.df["cluster_center"]
    temp[store.df["cluster_center"] == store.df.index] = 1

    ax.scatter(store.df[x], store.df[y], c=temp)
    ax.set_xlabel(x)
    ax.set_ylabel(y)

    ax.grid(True)
    fig.tight_layout()
    plt.show()


def plot_2D_circles(store, x="x", y="y", radius="z"):
    fig, ax = plt.subplots()

    temp = store.df["cluster_center"]
    temp[store.df["cluster_center"] == store.df.index] = 1

    ax.scatter(store.df[x], store.df[y], s=store.df[radius], c=temp)
    ax.set_xlabel(x)
    ax.set_ylabel(y)

    ax.grid(True)
    fig.tight_layout()
    plt.show()


def plot_3D(store, x="x", y="y", z="z"):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    temp = store.df["cluster_center"]
    temp[store.df["cluster_center"] == store.df.index] = 1

    ax.scatter(store.df[x], store.df[y], store.df[z], c=store.df["class"], cmap='viridis', linewidth=0.5)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_zlabel(z)

    ax.grid(True)
    fig.tight_layout()
    plt.show()
