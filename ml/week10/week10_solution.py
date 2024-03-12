"""
SOLUTION

19.11.2019 / Sascha Jecklin

"""

import numpy as np
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline

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
    # Generate polynomial features
    d = 15
    poly = PolynomialFeatures(degree=d)
    x_poly = poly.fit_transform(x[:,np.newaxis])

    # Prepare linear model
    mdl = linear_model.LinearRegression(fit_intercept=False)
    mdl.fit(x_poly, y)

    # Create smoothing spline model
    spl = UnivariateSpline(x, y, s=3)

    # Display result
    x_test      = np.linspace(-1.05, 2.05, 500)
    y_poly_test = mdl.predict(poly.fit_transform(x_test[:,np.newaxis]))
    y_spl_test  = spl(x_test)

    fig = plt.figure(figsize=(8,7))
    ax = fig.add_subplot(111)

    ax.plot(x, f(x), label='function')
    ax.plot(x, y, ls='', marker='.', label='f+noise')
    ax.plot(x_test, y_poly_test, label='Poly. reg. d={}'.format(d))
    ax.plot(x_test, y_spl_test, label='Smoothing spline s=10')

    ax.legend()
    ax.set_title('Arbitrary model flexibility')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_ylim([-2, 2])

    plt.show()


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
    # Perform grid search cross validation for polynomial regression
    parameters = {'polynomialfeatures__degree':np.arange(1,31)}

    polyreg = make_pipeline(PolynomialFeatures(), \
                            linear_model.LinearRegression(fit_intercept=False))
    kFoldCV = sklearn.model_selection.KFold(10, shuffle=True, random_state=0)
    clf = GridSearchCV(polyreg, parameters, cv=kFoldCV, scoring='neg_mean_squared_error')
    clf.fit(x[:,np.newaxis], y)

    print(pd.DataFrame(clf.cv_results_, \
                       index=parameters['polynomialfeatures__degree']))
    print("Poly. reg. best d is {}".format(clf.best_params_['polynomialfeatures__degree']))

    best_poly = clf.best_estimator_

    # Perform grid search cross validation for smoothing splines
    list_of_s   = np.arange(1,31)
    list_of_mse = []
    for s in list_of_s:
        cv_results = spline_cross_validation(x, y, s=s, fold=10)
        list_of_mse.append(np.mean(cv_results))
        print("Smoothing spline with smoother s: {:4d} own CV: {:4.4f}".format(s, list_of_mse[-1]))

    # Determine best value for s
    best_s = list_of_s[np.argmin(list_of_mse)]
    print("Smoothing spline best s is {}".format(best_s))
    best_spl = UnivariateSpline(x, y, s=best_s)

    # Plot result
    x_test      = np.linspace(-1.05, 2.05, 500)
    y_poly_test = best_poly.predict(x_test[:,np.newaxis])
    y_spl_test  = best_spl(x_test)

    fig = plt.figure(figsize=(8,7))
    ax = fig.add_subplot(111)

    ax.plot(x, f(x), label='function')
    ax.plot(x, y, ls='', marker='.', label='f+noise')
    ax.plot(x_test, y_poly_test, label='Best poly. reg.')
    ax.plot(x_test, y_spl_test, label='Best smoothing spline')

    ax.legend()
    ax.set_title('Best model flexibility')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_ylim([-2, 2])

    plt.show()


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
