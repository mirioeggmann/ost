"""
Week10: polynomial regression vs smoothing splines

19.11.2019 / Sascha Jecklin

"""

import numpy as np
import sklearn
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn.model_selection import cross_val_score

###############################################################################
##
## Functions
##
###############################################################################

def exercise_1(x, y, f):
    """
    Function for first exercise. This function implements a polynomial
    regression model and a smoothing spline model and plots the result.

    Parameters
    ----------
    x : ndarray
        Dataset of predictor variable
    y : ndarray
        Dataset of response variable
    f : lambda function
        Function of underlying population regression function

    Returns
    -------
    None.

    """
    pass


def exercise_2(x, y, f):
    """
    Function for second exercise. This function determines the best parameter
    values by cross validation and plots the corresponding result.

    Parameters
    ----------
    x : ndarray
        Dataset of predictor variable
    y : ndarray
        Dataset of response variable
    f : lambda function
        Function of underlying population regression function

    Returns
    -------
    None.

    """
    pass



def spline_cross_validation(x, y, s, fold):
    """
    This function performs cross validation with a smoothing spline model and
    returns the MSE of each test run.

    Parameters
    ----------
    x : ndarray
        Dataset of predictor variable
    y : ndarray
        Dataset of response variable
    s : float
        Positive smoothing factor used to choose the number of knots.
        Number of knots will be increased until the smoothing condition is
        satisfied.
    fold : int
        Number of folds for cross validation.

    Returns
    -------
    ndarray
        Array which contains the validataion MSE of every fold.

    """
    # stacking togheter for shuffeling
    x_y = np.hstack((x[:,np.newaxis], y[:,np.newaxis]))
    np.random.seed(0)
    np.random.shuffle(x_y)
    
    fold_size = x_y.shape[0] // fold
    cross_val_loss = []
    for i in range(fold):
        # Split set into train and valid set
        x_y_train = np.concatenate((x_y[:i*fold_size,:], \
                                    x_y[(i+1)*fold_size:,:]), axis=0)
        x_y_test  = x_y[i*fold_size:(i+1)*fold_size,:].copy()
        
        # Sort subsets according to x value
        x_y_train = x_y_train[x_y_train[:,0].argsort(),:]
        x_y_test  = x_y_test[x_y_test[:,0].argsort(),:]
        
        # Train and evaluate model
        spl = UnivariateSpline(x_y_train[:, 0], x_y_train[:, 1], s=s)
        cross_val_loss.append(np.mean((spl(x_y_test[:, 0])-x_y_test[:, 1])**2))
        
    return np.array(cross_val_loss)


###############################################################################
##
## Main
##
###############################################################################


def main():
    # Define example data and population regression function
    f = lambda x : 1/(1+25*x**4)
    # f = lambda x : x**4
    # f = lambda x : np.sin(x*2*np.pi)/x
    
    x = np.linspace(-1, 2, 150)
    y = f(x) + np.random.normal(0, 0.2, len(x))
    
    # Call functions
    exercise_1(x, y, f)
    exercise_2(x, y, f)


if __name__ == '__main__':
    main()
    plt.show()
