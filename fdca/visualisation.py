'''
This module contains functions for plotting results of the FDCA.
'''

import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np


def plot_line(series):
    trace = go.Scatter(
        x=series.index.values.tolist(),
        y=series.values.tolist(),
        mode='lines'
    )

    layout = go.Layout(
        title='Z values with different dc values',
        xaxis={
            'title': 'dc'
        },
        yaxis={
            'title': 'Z'
        }
    )

    figure = go.Figure(data=[trace], layout=layout)
    py.plot(figure, filename='basic-line', auto_open=True)


def plot_2d(df, centers, x, y):
    traces = []

    for i in centers:
        temp_cluster_array = df[
            (df['cluster_center'] == i)
            & (df['cluster_center'] != df.index)
        ]

        traces.append(
            go.Scatter(
                x=temp_cluster_array[x],
                y=temp_cluster_array[y],
                name='Cluster ' + str(i),
                mode='markers',
                marker={
                    'size': 10
                }
            )
        )

    cluster_centers = df[df['cluster_center'] == df.index]

    traces.append(
        go.Scatter(
            x=cluster_centers[x],
            y=cluster_centers[y],
            name='Cluster Centers',
            mode='markers',
            marker={
                'color': 'rgb(0, 0, 0)',
                'size': 10
            }
        )
    )

    data = traces

    layout = go.Layout(
        # title='Clustering',
        xaxis={
            'title': x
        },
        yaxis={
            'title': y
        }
    )

    figure = go.Figure(data=data, layout=layout)
    py.plot(figure, filename='basic-scatter', auto_open=True)


# def plot_2d_circles(store, x, y, size):
#     trace = go.Scatter(
#         x = store.df[x],
#         y = store.df[y],
#         mode = 'markers',
#         marker = dict(
#             size = store.df[size],
#             opacity = 0.6,
#             colorscale = 'Viridis'
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
#     py.plot(figure, filename='basic-scatter', auto_open=True)


def plot_3d(df, centers, x, y, z):
    traces = []

    for i in centers:
        temp_cluster_array = df[
            (df['cluster_center'] == i)
            & (df['cluster_center'] != df.index)
        ]

        # Create a trace
        traces.append(
            go.Scatter3d(
                x=temp_cluster_array[x],
                y=temp_cluster_array[y],
                z=temp_cluster_array[z],
                name='Cluster ' + str(i),
                mode='markers',
                marker={
                    'opacity': 0.6,
                    'size': 5
                }
            )
        )

    cluster_centers = df[df['cluster_center'] == df.index]

    traces.append(
        go.Scatter3d(
            x=cluster_centers[x],
            y=cluster_centers[y],
            z=cluster_centers[z],
            name='Cluster Centers',
            mode='markers',
            marker={
                'color': 'rgb(0, 0, 0)',
                'opacity': 0.6,
                'size': 5
            }
        )
    )

    data = traces

    layout = go.Layout(
        # title='Clustering',
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
        scene={
            'xaxis': {'title': x},
            'yaxis': {'title': y},
            'zaxis': {'title': z},
        },
        legend={'orientation': 'h'}
    )

    figure = go.Figure(data=data, layout=layout)
    py.plot(figure, filename='basic-3d-scatter', auto_open=True)


def plot_x_y_date(df, centers, x, y, date, steps=200):
    points = {}

    date_min = df[date].min()
    date_max = df[date].max()
    date_step = (date_max - date_min) / steps

    # print(date_min, date_max, date_step)

    i = date_min
    while i <= date_max:
        for index, item in df[(df.date >= i) & (df.date <= i+date_step)].iterrows():
            if item['cluster_center'] in points:
                if str(i) in points[item['cluster_center']]['dates']:
                    points[item['cluster_center']]['dates'][str(i)] += 1
                else:
                    points[item['cluster_center']]['dates'][str(i)] = 1
            else:
                points[item['cluster_center']] = {
                    'x': str(item[x]),
                    'y': str(item[y]),
                    'dates': {str(i): 1}
                }

        i += date_step

    x_values = []
    y_values = []
    times = []
    sizes = []

    for item in points:
        x_values += [points[item]['x']] * len(points[item]['dates'])
        y_values += [points[item]['y']] * len(points[item]['dates'])
        times += list(points[item]['dates'].keys())
        sizes += list(points[item]['dates'].values())

    trace = go.Scatter3d(
        x=x_values,
        y=y_values,
        z=times,
        mode='markers',
        marker={
            'size': sizes,
            'opacity': 0.5,
            'color': sizes,
            'colorscale': 'Viridis',
            'colorbar': {
                'title': 'Number of Tweets',
                'titleside': 'bottom'
            }
        }
    )

    layout = go.Layout(
        # title= 'Clustering',
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
        scene={
            'xaxis': {'title': x},
            'yaxis': {'title': y},
            'zaxis': {'title': date},
        },
    )

    figure = go.Figure(data=[trace], layout=layout)
    py.plot(figure, filename='3d-scatter-test', auto_open=True)


def plot_class_bars(df, centers, class_column):
    classes = {}
    for index, item in df.iterrows():
        if item[class_column] in classes:
            if f"Cluster {item['cluster_center']}" in classes[item[class_column]]:
                classes[item[class_column]]['Cluster ' + str(item['cluster_center'])] += 1
            else:
                classes[item[class_column]]['Cluster ' + str(item['cluster_center'])] = 1
        else:
            classes[item[class_column]] = {
                'Cluster ' + str(item['cluster_center']): 1
            }

    traces = []
    for key in classes:
        traces.append(
            go.Bar(
                x=list(classes[key].keys()),
                y=list(classes[key].values()),
                name=key
            )
        )

    layout = go.Layout(
        barmode='stack',
        xaxis={'title': 'Cluster'},
        yaxis={'title': 'Number of Tweets'}
    )

    figure = go.Figure(data=traces, layout=layout)
    py.plot(figure, filename='grouped-bar')


def plot_2d_geo(df, centers, longitude, latitude, scale=200, scope='usa'):
    clusters = []

    for index, item in df[df['cluster_center'] == df.index].iterrows():
        size = df[df['cluster_center'] == index].shape[0]

        cluster = go.Scattergeo(
            locationmode='USA-states',
            lon=[item[longitude]],
            lat=[item[latitude]],
            name='Cluster ' + str(item['cluster_center']),
            text='Number of Tweets: ' + str(size),
            marker=go.scattergeo.Marker(
                size=size / scale,
                opacity=0.5,
                line=go.scattergeo.marker.Line(
                    width=0.5, color='rgb(40,40,40)'
                ),
                sizemode='area'
            )
        )

        clusters.append(cluster)

    layout = go.Layout(
            title=go.layout.Title(
                text='Clusters on Map'
            ),
            showlegend=True,
            geo=go.layout.Geo(
                scope=scope,
                projection=go.layout.geo.Projection(
                    type='albers usa'
                ),
                showland=True,
                landcolor='rgb(217, 217, 217)',
                subunitwidth=1,
                countrywidth=1,
                subunitcolor='rgb(255, 255, 255)',
                countrycolor='rgb(255, 255, 255)'
            )
        )

    fig = go.Figure(data=clusters, layout=layout)
    py.plot(fig, filename='cluster_geo_bubble_map')
