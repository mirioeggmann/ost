import skimage.io
import numpy as np
import matplotlib.pyplot as plt
from my_kmeans_ex import MyKMeans
from sklearn.datasets.samples_generator import make_blobs


###############################################################################
##
## Functions
##
###############################################################################

def exercise1():
    # create data
    x, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.60,
                      random_state=0)

    # show data
    fig, axes = plt.subplots(3,1, figsize=(6,12))
    axes[0].scatter(x[:, 0], x[:, 1], s=7)
    axes[0].set_title('Dataset')
    
    # TODO: Implement the class MyKMeans. Select a reasonable number of classes
    # based on the above scatter plot
    
    # create model and fit it
    mdl = MyKMeans(None).fit(x)

    # call predict method and indicate cluster assignments with different colors
    prediction = mdl.predict(x)
    axes[1].scatter(x[:, 0], x[:, 1], c=prediction, s=7)
    axes[1].scatter(mdl.cluster_centers_[:, 0], mdl.cluster_centers_[:, 1],
                marker='X', c='r', s=150)
    axes[1].set_title('Cluster assignment')
    
    # displaying the decision boundaries of the clusters
    x_min, x_max = x[:, 0].min() - 1, x[:, 0].max() + 1
    y_min, y_max = x[:, 1].min() - 1, x[:, 1].max() + 1
    plot_clusters(mdl, x_min, x_max, y_min, y_max, ax=axes[2])
    axes[2].scatter(x[:, 0], x[:, 1], c=prediction, s=7)
    axes[2].set_title('Voronoi diagram')
    plt.show()

def exercise2():
    # read image and plot it
    image = skimage.io.imread('hands.png')
    
    fig, axes = plt.figure(2,1,figsize=(6,12))
    axes[0].imshow(image)
    axes[0].axis('off')
    plt.show()
    
    # TODO:  Have a look at the loaded image. How many clusters would you
    # create to seperate the hands from the background

    # TODO: Fit a MyKMeans model with the image. You need to modify the images
    # shape first. Hint: Based on what would you like to segment the image?

    # TODO: Visualize the segmented image


def plot_clusters(mdl, x_min, x_max, y_min, y_max, ax=None):
    """ This is a helper function to plot the cluster boundaries

    Parameters:
    -----------
    model : obj
            fitted model
    x_min : float
            minimum x_value of plot
    x_max : float
            maximum x_value of plot
    y_min : float
            minimum y_value of plot
    y_min : float
            maximum y_value of plot
    ax : obj
         optional figure to plot on
    """
    if ax is None:
        plt.figure(figsize=(8, 8))
    ax = plt.gca()

    # creating a meshgrid to approximate a decision boundary
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200, endpoint=True),
                         np.linspace(y_min, y_max, 200, endpoint=True))
    # predicting on the flattened mesh
    prediction = mdl.predict(np.c_[xx.ravel(), yy.ravel()])
    # and bringing it back to its original shape
    prediction = prediction.reshape(xx.shape)
    # plotting the colormesh
    ax.pcolormesh(xx, yy, prediction, cmap="cool")


if __name__ == '__main__':
    exercise1()
    exercise2()
    plt.show()
