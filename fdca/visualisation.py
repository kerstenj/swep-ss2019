import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot(store):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    temp = store.df["cluster_center"]
    temp[store.df["cluster_center"] == store.df.index] = 1

    # Aggregation:
    #Axes3D.scatter(xs, ys, zs=0, zdir='z', s=20, c=None, depthshade=True, *args, **kwargs)
    ax.scatter(store.df["x"], store.df["y"], c=temp)

    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # Iris subtable:
    # ax.scatter(s.df["sepal length"],s.df["sepal width"],c=temp)
    # ax.set_xlabel('sepal length')
    # ax.set_ylabel('sepal width')

    ax.grid(True)
    fig.tight_layout()
    plt.show()
