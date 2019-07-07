import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np


def plot_line(array):
    trace = go.Scatter(
        y = array,
        mode = "lines"
    )

    data = [trace]

    py.plot(data, filename="basic-line", auto_open=True)

def plot_2D(store, x="x", y="y"):
    traces = []

    for i in store.cz:
        temp_cluster_array = store.df[(store.df["cluster_center"] == i) & (store.df["cluster_center"] != store.df.index)]

        traces.append(
            go.Scatter(
                x = temp_cluster_array[x],
                y = temp_cluster_array[y],
                name = "Cluster " + str(i),
                mode = 'markers'
            )
        )

    cluster_centers = store.df[store.df["cluster_center"] == store.df.index]

    traces.append(
        go.Scatter(
            x = cluster_centers[x],
            y = cluster_centers[y],
            name = "Cluster Centers",
            mode = "markers",
            marker = dict(
                color = "rgb(0, 0, 0)"
            )
        )
    )

    data = traces

    layout= go.Layout(
        # title= 'Clustering',
        xaxis= dict(
            title= x
        ),
        yaxis=dict(
            title= y
        )
    )

    figure = go.Figure(data=data, layout=layout)

    # Plot
    py.plot(figure, filename='basic-scatter', auto_open=True)

def plot_3D(store, x="x", y="y", z="z"):
    traces = []

    for i in store.cz:
        temp_cluster_array = store.df[(store.df["cluster_center"] == i) & (store.df["cluster_center"] != store.df.index)]

        # Create a trace
        traces.append(
            go.Scatter3d(
                x = temp_cluster_array[x],
                y = temp_cluster_array[y],
                z = temp_cluster_array[z],
                name = "Cluster " + str(i),
                mode = 'markers'
            )
        )

    cluster_centers = store.df[store.df["cluster_center"] == store.df.index]

    traces.append(
        go.Scatter3d(
            x = cluster_centers[x],
            y = cluster_centers[y],
            z = cluster_centers[z],
            name = "Cluster Centers",
            mode = "markers",
            marker = dict(
                color = "rgb(0, 0, 0)"
            )
        )
    )

    data = traces

    layout= go.Layout(
        # title= 'Clustering',
        margin = dict(
            l = 0,
            r = 0,
            b = 0,
            t = 0
        )
    )

    figure = go.Figure(data=data, layout=layout)

    # Plot
    py.plot(figure, filename='basic-3d-scatter', auto_open=True)
