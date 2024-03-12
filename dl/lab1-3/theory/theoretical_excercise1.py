import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
import seaborn as sns


def plotVectors(vecs, cols, alpha=1):
    """
    Plot set of vectors.

    Parameters
    ----------
    vecs : array-like
        Coordinates of the vectors to plot. Each vectors is in an array. For
        instance: [[1, 3], [2, 2]] can be used to plot 2 vectors.
    cols : array-like
        Colors of the vectors. For instance: ['red', 'blue'] will display the
        first vector in red and the second in blue.
    alpha : float
        Opacity of vectors

    Returns:

    fig : instance of matplotlib.figure.Figure
        The figure of the vectors
    """
    plt.figure()
    plt.axvline(x=0, color='#A9A9A9', zorder=0)
    plt.axhline(y=0, color='#A9A9A9', zorder=0)

    for i in range(len(vecs)):
        x = np.concatenate([[0, 0], vecs[i]])
        plt.quiver([x[0]],
                   [x[1]],
                   [x[2]],
                   [x[3]],
                   angles='xy', scale_units='xy', scale=1, color=cols[i],
                   alpha=alpha)

if __name__ == "__main__":

    # 4a)
    A = np.array([[1, 2], [1, 4], [1, 6]])
    print(A)
    b = np.array([[1.8], [3.3], [4.1]])
    print(b)

    B = A.T.dot(A)
    print(B)
    print("eigenvalues for 4a")
    eigenvalues = LA.linalg.eig(B)[0]
    print(eigenvalues)
    print("eigenvectors for 4c")
    eigenvectors = LA.linalg.eig(B)[1]
    print(eigenvectors)

    D = np.array([[np.sqrt(eigenvalues[1]), 0], [0, np.sqrt(eigenvalues[0])], [0, 0]])
    print(D)

    print("check c -------------------------------------")
    v1 = np.array([eigenvectors[0][1], eigenvectors[1][1]])
    v2 = np.array([eigenvectors[0][0], eigenvectors[1][0]])
    V = np.array([v1.T, v2.T])
    print(v1)
    print(v2)
    print(V)

    print("check d -------------------------------------")
    C = A.dot(A.T)
    print(C)

    U_eigenvalues = LA.linalg.eig(C)[0]
    U = LA.linalg.eig(C)[1] # eigenvectors of C
    print(U_eigenvalues)
    print(U)

    print("check e -------------------------------------")
    U_identity_matrix_check = (U.T).dot(U).round(0) # or U.dot(U.T) the same
    print(U_identity_matrix_check)
    V_identity_matrix_check = (V).dot(V.T).round(0)
    print(V_identity_matrix_check)

    A_test = (U.dot(D)).dot(V.T)
    print("{0} equals to {1}".format(A_test, A))

    orange = '#FF9A13'
    blue = '#1190FF'

    #plotVectors([Ab.flatten(), b.flatten()], cols=[blue, orange])
    plt.ylim(-1, 40)
    plt.xlim(-1, 40)
    plt.show()
