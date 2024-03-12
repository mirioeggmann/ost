import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


def plot_height_weight_mesh(data, trained_model, x_min, x_max, y_min, y_max,
                            comment=None, ax=None):
    """ Plots a mesh witch visualizes the decision boundry of a given model

    Parameters:
    data : array_like
           input data
    trained_model : object
                    lda or qda model
    x_min : int
            minimum x value for figure
    x_max : int
            maximum x value for figure
    y_min : int
            minimum y value for figure
    y_max : int
            maximum y value for figure
    comment : string
              string for description
    ax : pyplot_axis
         axis from figure
    """
    plt.figure(figsize=(8, 8))
    cmap_light = ListedColormap(['#FFAAAA', '#AAAAFF'])
    if ax is None:
        ax = plt.gca()

    # make a meshgrid to predict class on every point in a plane
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, num=200, endpoint=True),
                         np.linspace(y_min, y_max, num=200, endpoint=True))
    # convert meshgrid to two flat vectors, make the prediction, and convert
    # the prediction back to a meshgrid
    prediction = trained_model.predict(np.c_[xx.ravel(), yy.ravel()])
    prediction = prediction.reshape(xx.shape)

    # print the prediction in a colored mesh
    ax.pcolormesh(xx, yy, prediction, cmap=cmap_light)
    plot_height_weight(data, ax=ax)
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    if comment is not None:
        ax.text(0.95, 0.05, comment, transform=ax.transAxes,
                verticalalignment="bottom", horizontalalignment="right",
                fontsize=14)


def decimal_to_percent(x, decimals=2):
    """ Convert decimal to percent

    Parameters:
    x : float
        input value
    decimals : int
               decimals

    Returns:
    int : float with decimals
    """
    return '{0:.2f}%'.format(np.round(100*x, decimals=2))


def plot_height_weight(data, ax=None):
    """ Plots height and weight from the data set

    Parameters:
    data : array_like
           input data
    ax : pyplot_axis
         axis from figure
    """
    if ax is None:
        plt.figure(figsize=(8, 8))
        ax = plt.gca()
    colors = {"Male": 'blue', "Female": 'red'}
    if ax is None:
        ax = plt.gca()
    for name, group in data.groupby('Gender'):
        ax.scatter(group.Height, group.Weight, color=colors[name], label=name)
    ax.set_title("Weight vs Height")
    ax.set_xlabel('height')
    ax.set_ylabel('weight')
    ax.legend(loc='upper left')
    ax.grid()
