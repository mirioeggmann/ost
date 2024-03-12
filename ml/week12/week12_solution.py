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
    # gamma appropriately scaled
    mdl = SVC(kernel='linear', C=10, gamma='scale').fit(x, y)
    
    # Display result
    fig, ax = plt.subplots(1,1, figsize=(8,8))
    ax.scatter(x[:, 0], x[:, 1], c=y, s=50, cmap='autumn')
    plot_svc_decision_function(mdl, ax)
    
    plt.pause(0.01)
    plt.show()


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
    # Evaluate svm for different C values
    c_values = np.array([10, 1, 0.1, 0.001])
    fig, axes = plt.subplots(2,2, figsize=(8,8))
    
    for i, c in enumerate(c_values):
        mdl = SVC(kernel='linear', C=c, gamma='scale').fit(x, y)
        axes[i//2,i%2].scatter(x[:, 0], x[:, 1], c=y, s=50, cmap='autumn')
        plot_svc_decision_function(mdl, axes[i//2,i%2])
        axes[i//2,i%2].set_title('Linear SVM, C={:.2f}'.format(c))
    
    plt.pause(0.01)
    plt.show()


def exercise_3(x, y):
    """
    Function for exercise 3

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
    # 1. Exponential function centered in the middle
    z_1 = np.exp(-x[:, 0]**2 - x[:, 1]**2)

    # 2. polynomial mapping with degree 2
    z_2 = x[:,0]**2 + x[:,1]**2
    
    # Display result
    fig = plt.figure(figsize=(8,8))
    ax1 = fig.add_subplot(211, projection='3d')
    ax1.scatter(x[:, 0], x[:, 1], z_1, c=y, s=50, cmap='autumn')
    ax1.set_title('Exp function')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('z')
    
    ax2 = fig.add_subplot(212, projection='3d')
    ax2.scatter(x[:, 0], x[:, 1], z_2, c=y, s=50, cmap='autumn')
    ax2.set_title('Poly function')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_zlabel('z')
    
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
    # Radial basis function as kernel
    mdl_1 = SVC(kernel='rbf', C=100000, gamma='scale', degree=2)
    mdl_1.fit(x, y)
    
    # Polynomial kernel of degree 2
    mdl_2 = SVC(kernel='poly', C=100000, gamma='scale', degree=2)
    mdl_2.fit(x, y)
    
    # Display result
    fig, axes = plt.subplots(2,1, figsize=(8,8))
    axes[0].scatter(x[:, 0], x[:, 1], c=y, s=50, cmap='autumn')
    plot_svc_decision_function(mdl_1, axes[0])
    axes[0].set_title('RBF kernel')
    
    axes[1].scatter(x[:, 0], x[:, 1], c=y, s=50, cmap='autumn')
    plot_svc_decision_function(mdl_2, axes[1])
    axes[1].set_title('Poly kernel')
    
    plt.pause(0.01)
    plt.show()
    


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
