"""
This module contains functions for plotting results of the FDCA.
"""

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

def plot_2d(df, centers, x, y):
    traces = []

    for i in centers:
        temp_cluster_array = df[(df["cluster_center"] == i) & (df["cluster_center"] != df.index)]

        traces.append(
            go.Scatter(
                x = temp_cluster_array[x],
                y = temp_cluster_array[y],
                name = "Cluster " + str(i),
                mode = 'markers'
            )
        )

    cluster_centers = df[df["cluster_center"] == df.index]

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

def plot_3d(df, centers, x, y, z):
    traces = []

    for i in centers:
        temp_cluster_array = df[(df["cluster_center"] == i) & (df["cluster_center"] != df.index)]

        # Create a trace
        traces.append(
            go.Scatter3d(
                x = temp_cluster_array[x],
                y = temp_cluster_array[y],
                z = temp_cluster_array[z],
                name = "Cluster " + str(i),
                mode = 'markers',
                marker = dict(
                    opacity = 0.6,
                    size = 5
                )
            )
        )

    cluster_centers = df[df["cluster_center"] == df.index]

    traces.append(
        go.Scatter3d(
            x = cluster_centers[x],
            y = cluster_centers[y],
            z = cluster_centers[z],
            name = "Cluster Centers",
            mode = "markers",
            marker = dict(
                color = "rgb(0, 0, 0)",
                opacity = 0.6,
                size = 5

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
        ),
        scene=dict(
            xaxis= dict(
                title= x
            ),
            yaxis=dict(
                title= y
            ),
            zaxis = {
                'title': z
            }
        ),
        legend = {'orientation': 'h'}
    )

    figure = go.Figure(data=data, layout=layout)

    # Plot
    py.plot(figure, filename='basic-3d-scatter', auto_open=True)

def plot_x_y_date(df, centers, x, y, date, steps=100):
    points = {}

    date_min = df[date].min()
    date_max = df[date].max()
    date_step = (date_max - date_min) / steps

    # print(date_min, date_max, date_step)

    i = date_min
    while i <= date_max:
        for index, item in df[(df.date >= i) & (df.date <= i+date_step)].iterrows():
            if item["cluster_center"] in points:
                if str(i) in points[item["cluster_center"]]["dates"]:
                    points[item["cluster_center"]]["dates"][str(i)] += 1
                else:
                    points[item["cluster_center"]]["dates"][str(i)] = 1
            else:
                points[item["cluster_center"]] = {
                    "x": str(item[x]),
                    "y": str(item[y]),
                    "dates": {
                        str(i): 1
                    }
                }

        i += date_step

    x_values = []
    y_values = []
    times = []
    sizes = []

    for item in points:
        x_values += [points[item]["x"]] * len(points[item]["dates"])
        y_values += [points[item]["y"]] * len(points[item]["dates"])
        times += list(points[item]["dates"].keys())
        sizes += list(points[item]["dates"].values())

    trace = go.Scatter3d(
        x = x_values,
        y = y_values,
        z = times,
        mode = "markers",
        marker = {
            "size": sizes,
            "opacity": 0.5,
            "color": sizes,
            "colorscale": "Viridis",
            "colorbar": {
                "title": "Number of Tweets",
                "titleside": "bottom"
            }
        }
    )

    layout= go.Layout(
        # title= 'Clustering',
        margin = dict(
            l = 0,
            r = 0,
            b = 0,
            t = 0
        ),
        scene=dict(
            xaxis= dict(
                title= x
            ),
            yaxis=dict(
                title= y
            ),
            zaxis = {
                'title': date
            }
        )
    )

    figure = go.Figure(data=[trace], layout=layout)

    # Plot
    py.plot(figure, filename='3d-scatter-test', auto_open=True)
