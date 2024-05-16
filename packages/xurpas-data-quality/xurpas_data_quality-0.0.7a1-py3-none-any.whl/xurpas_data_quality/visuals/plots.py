import io
import base64

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from xurpas_data_quality.data.algorithms import sturges, rice,freedman_diaconis

def create_tiny_histogram(data: pd.Series):
    data = data.dropna()
    fig= plt.figure()
    plt.hist(data, edgecolor="white")
    plt.box(False)

    return fig

def create_histogram(data: pd.Series):
    data = data.dropna()
    fig= plt.figure(figsize=(8,4))
    plt.hist(data, edgecolor="white")
    plt.box(False)

    return fig

def create_heatmap(df: pd.DataFrame):
    # Create a figure and a set of subplots
    fig, ax = plt.subplots()
    plt.box(False)
    # Create the heatmap
    heatmap = ax.imshow(df, cmap='RdYlBu', interpolation='nearest', vmin=-1.0, vmax=1.0)

    # Set the column names as x-axis labels
    ax.set_xticks(np.arange(len(df.columns)))
    ax.set_xticklabels(df.columns)

    # Set the column names as y-axis labels
    ax.set_yticks(np.arange(len(df.columns)))
    ax.set_yticklabels(df.columns)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Create a colorbar
    cbar = plt.colorbar(heatmap)
    cbar.outline.set_visible(False)

    return fig

def create_distribution_plot(column: pd.Series, subplot_size=5):
    fig, axs = plt.subplots(ncols=2, figsize=(2*subplot_size, subplot_size))

    axs[0].boxplot(column)

    axs[1].violinplot(column)

    fig.suptitle(f'{column.name} distribution')

    return fig

def create_interaction_plot(x: pd.Series, y: pd.Series):
    fig = plt.figure(figsize=(8,4))
    plt.scatter(x,y,edgecolor="white")

    return fig
    

def create_distribution_from_dataframe(df: pd.DataFrame):
    if 'employee_code' in df.columns:
        df = df.drop('employee_code', axis=1)

    fig = plt.figure()
    boxplot = df.boxplot(figsize=(15,3))
    return fig

def plot_to_base64(fig: plt.figure):
    buf = io.BytesIO()
    fig.savefig(buf, format="svg", bbox_inches='tight')
    plt.close(fig)

    data = base64.b64encode(buf.getvalue()).decode("utf8")
    buf.close()
    return "data:image/svg+xml;base64,{}".format(data)