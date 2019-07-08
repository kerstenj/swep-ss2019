import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np


def plot_line(series):
    trace = go.Scatter(
        x = series.index.values.tolist(),
        y = series.values.tolist(),
        mode = "lines"
    )

    data = [trace]

    py.plot(data, filename="basic-line", auto_open=True)

def plot_2d(store, x, y):
    traces = []

    for i in store.centers:
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

# def plot_2d_circles(store, x, y, size):
#     trace = go.Scatter(
#         x = store.df[x],
#         y = store.df[y],
#         mode = "markers",
#         marker = dict(
#             size = store.df[size],
#             opacity = 0.6,
#             colorscale = "Viridis"
#         )
#     )
#
#     data = [trace]
#
#     layout= go.Layout(
#         # title= 'Clustering',
#         xaxis= dict(
#             title= x
#         ),
#         yaxis=dict(
#             title= y
#         )
#     )
#
#     figure = go.Figure(data=data, layout=layout)
#
#     # Plot
#     py.plot(figure, filename='basic-scatter', auto_open=True)

def plot_3d(store, x, y, z):
    traces = []

    for i in store.centers:
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

def plot_3d_test(store, x, y, z, size):
    clusters = {}

    for index, item in store.df.iterrows():
        if item["cluster_center"] in clusters:
            clusters[item["cluster_center"]] += item[size]
        else:
            clusters[item["cluster_center"]] = item[size]

    traces = []

    for item in clusters:
        traces.append(
            go.Scatter3d(
                x = store.df[store.df.index == item][x],
                y = store.df[store.df.index == item][y],
                z = store.df[store.df.index == item][z],
                name = "Cluster " + str(item),
                mode = "markers",
                marker = dict(
                    size = clusters[item]
                )
            )
        )

    layout= go.Layout(
        # title= 'Clustering',
        margin = dict(
            l = 0,
            r = 0,
            b = 0,
            t = 0
        )
    )

    figure = go.Figure(data=traces, layout=layout)

    # Plot
    py.plot(figure, filename='3d-scatter-test', auto_open=True)
