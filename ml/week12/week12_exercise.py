"""
Week12: Support Vector Machine

03.12.2019 / Sascha Jecklin

"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.datasets.samples_generator import make_blobs
from sklearn.datasets.samples_generator import make_circles
from sklearn.model_selection import GridSearchCV
from mpl_toolkits.mplot3d import Axes3D
sns.set()

###############################################################################
##
## Functions
##
###############################################################################

def exercise_1(x, y):
    """
    Function for exercise 1

    Parameters
    ----------
    x : ndarray
        Predictor variables of dataset
    y : ndarray
        Response variables of dataset

    Returns
    -------
    None.

    """
    # TODO: Create and fit a linear SVC model using sklearn objects
    
    # TODO: Make a scatter plot of the training data
    
    # TODO: Display the decision boundary of the SVC model using the function
    # plot_svc_decision_function

    pass


def exercise_2(x, y):
    """
    Function for exercise 2

    Parameters
    ----------
    x : ndarray
        Predictor variables of dataset
    y : ndarray
        Response variables of dataset

    Returns
    -------
    None.

    """
    # TODO: Create and fit a linear SVC model with different values for the 
    # hyperparameter C
    
    # TODO: Make a scatter plot of the training data
    
    # TODO: Display all decision boundaries of the SVC model using the function
    # plot_svc_decision_function multiple times
    
    # Evaluate svm for different C values
    c_values = np.array([10, 1, 0.1, 0.001])

def exercise_3(x, y):
    """
    An RBF Kernel maps into an infinite dimensional space -> bad for
    plotting. To get an idea of what happens we expand our 2D data into 3D
    and make it linearly separable.

    Parameters
    ----------
    x : ndarray
        Predictor variables of dataset
    y : ndarray
        Response variables of dataset

    Returns
    -------
    None.

    """
    # TODO: Try to make the classes separable by a plane by adding a third 
    # dimension to the provided two dimensions.
    
    # TODO: Use the following functions as third dimension:
        # -> z = exp(-x^2 - y^2)
        # -> z = x^2 + y^2
        
    # TODO: Display a 3D scatter plot of the training data expanded to three
    # dimensions.
    
    # Display result
    fig = plt.figure(figsize=(8,8))
    ax1 = fig.add_subplot(211, projection='3d')
    
    ax2 = fig.add_subplot(212, projection='3d')
    
    plt.pause(0.01)
    plt.show()


def exercise_4(x, y):
    """
    Function for exercise 4

    Parameters
    ----------
    x : ndarray
        Predictor variables of dataset
    y : ndarray
        Response variables of dataset

    Returns
    -------
    None.

    """

    # TODO: Create and fit a SVC model with RBF kernel
    
    # TODO: Create and fit a SVC model with polynomial kernel of degree 2
    
    # TODO: Make a scatter plot of the training data
    
    # TODO: Display the decision boundary of both SVC model using the function
    # plot_svc_decision_function
        
    pass


def plot_svc_decision_function(mdl, ax=None):
    """ Plot the decision boundary for a 2D support vector Machine

    Parameters:
    -----------
    mdl : object
          trained model
    ax : object
         optional figure handle

    """

    # take given axis or create new one
    if ax is None:
        ax = plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Create grid data to determine decision boundary
    x = np.linspace(xlim[0], xlim[1], 30)
    y = np.linspace(ylim[0], ylim[1], 30)
    y, x = np.meshgrid(y, x)
    x_and_y_stacked = np.vstack([x.ravel(), y.ravel()]).T
    P = mdl.decision_function(x_and_y_stacked).reshape(x.shape)

    # Display result
    ax.contour(x, y, P, colors='k',
               levels=[-1, 0, 1], alpha=0.5,
               linestyles=['--', '-', '--'])

    ax.scatter(mdl.support_vectors_[:, 0],
               mdl.support_vectors_[:, 1],
               s=200, facecolors='none', edgecolors='black')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

###############################################################################
##
## Main
##
###############################################################################

def main():
    # Linearly separable data
    x1, y1 = make_blobs(n_samples=50, centers=2, random_state=0,
                      cluster_std=0.60)
    # Almost linearly separable data
    x2, y2 = make_blobs(n_samples=150, centers=2, random_state=3,
                        cluster_std=1.5)
    # Not linear separable data
    x3, y3 = make_circles(100, factor=.1, noise=.1)
    
    
    # Apply linear SVM to linearly separable data
    exercise_1(x1, y1)
    
    # Apply linear SVM with different values for hyperparameter C
    exercise_2(x2, y2)
    
    # Apply linear SVM to highly nonlinear data
    exercise_1(x3, y3)
    
    # Find mapping function which makes dataset linearly separable
    exercise_3(x3, y3)
    
    # Apply kernel SVM
    exercise_4(x3, y3)

if __name__ == '__main__':
    main()
