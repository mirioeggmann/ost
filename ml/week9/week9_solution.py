"""
SOLUTION

12.11.2019 / Sascha Jecklin

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import itertools
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler


###############################################################################
##
## Functions
##
###############################################################################

def best_subset(x, y):
    """ Carries out a best subset selection of features for a
        LinearRegression model
    Parameters:
    -----------
    x: array_like
       predictors
    y: array_like
       labels
    """
    num_feat = x.shape[1]

    adj_r_squared_list = []
    feature_list = []
    n_features = []

    print('Best subset')
    # print formatted as table
    print('{:18} | {:>125} | {:>7}'.format("Number of features", "Features",
                                           "adj. R^2"))
    print('-'*157)  # print 157 dashes

    # iterate over the range from 1 to k features
    for k in range(1, num_feat+1):
        # iterate over all combinations with k features and store adj_r_squared
        for combination in itertools.combinations(x.columns, k):
            r_squared, adj_r_squared = fit_linear_reg(x[list(combination)], y)
            adj_r_squared_list.append(adj_r_squared)
            feature_list.append(combination)
            n_features.append(len(combination))

    # store in dataframe
    df = pd.DataFrame({'n_features': n_features,
                       'adj_r_squared': adj_r_squared_list,
                       'features': feature_list})
    # sort by biggest adj_r_squared
    df = df.sort_values(by=['adj_r_squared'], ascending=False)


    for i in range(1, num_feat+1):
        # picking the first entry with i predictors of a sorted list
        # --> max adj_r_squared for i
        best_with_i_pred = df[df.n_features == i].values[0]
        print("{:<18d} | {:>125} | {:1.6f}".format(i,
              ', '.join(best_with_i_pred[2]), best_with_i_pred[1]))
    print('\n'*3)

    # Display result
    fig, ax = plt.subplots(1,1)
    ax.plot(np.arange(1, num_feat+1), df.groupby(['n_features'])['adj_r_squared'].max())
    ax.set_title('Best subset selection')
    ax.set_xlabel('Number of predictors')
    ax.set_ylabel('Adjusted $R^2$')
    plt.show()



def forward_selection(x, y):
    """ Carries out a forward stepwise selection of features for a
        LinearRegression model
    Parameters:
    -----------
    x: array_like
       predictors
    y: array_like
       labels
    """

    num_feat = x.shape[1]
    # need to now with features are left to build all combinations of them
    remaining_features = list(x.columns.values)
    features           = []
    list_adj_R_squared = []

    print('Forward stepwise subset selection')
    # print formatted as table
    print('{:18} | {:>125} | {:>7}'.format("Number of features", "Features",
                                                                 "adj. R^2"))
    print('-'*157)  # print 157 dashes

    for i in range(1, num_feat+1):
        best_r_squared     = 0
        best_adj_r_squared = 0

        # Loop over possible additional features
        for add_feature in remaining_features:

            # Fit new set of features
            r_squared, adj_r_squared = fit_linear_reg(x[[add_feature]+features], y)

            if r_squared > best_r_squared:
                best_r_squared     = r_squared
                best_adj_r_squared = adj_r_squared
                best_feature       = add_feature

        # Updating variables for next loop
        features.append(best_feature)
        remaining_features.remove(best_feature)

        list_adj_R_squared.append(best_adj_r_squared)

        print("{:<18d} | {:>125} | {:1.6f}".format(i,
              ', '.join(features), best_adj_r_squared))

    # Display result
    fig, ax = plt.subplots(1,1)
    ax.plot(np.arange(1, num_feat+1), list_adj_R_squared)
    ax.set_title('Forward selection')
    ax.set_xlabel('Number of predictors')
    ax.set_ylabel('Adjusted $R^2$')
    plt.show()


def ridge_regression(x, y):
    """ Fits a linear regression model with different L2 regularization terms
        and plots the model coefficients depending on lambda (alpha)
    Parameters:
    -----------
    x: array_like
       predictors
    y: array_like
       labels
    """

    clf = Ridge()
    coefs = []
    alphas = np.logspace(-2, 5, 200)  # called lambda in the book
    labels = x.columns

    # scaling the data just like the book did it
    scaler = StandardScaler()
    x = scaler.fit_transform(x)

    # iterate over alphas and train models. store coefficients
    for a in alphas:
        clf.set_params(alpha=a)
        clf.fit(x, y)
        coefs.append(clf.coef_)


    # Display result
    plt.figure(figsize=(7, 7))
    ax = plt.gca()
    ax.plot(alphas, coefs)
    ax.set_xscale('log')
    ax.set_xlabel('lambda')
    ax.set_ylabel('weights')
    ax.set_title('Ridge coefficients as a function of the regularization')
    ax.axis('tight')
    ax.legend(labels)
    plt.show()


def lasso_regression(x, y):
    """ Fits a linear regression model with different L1 regularization terms
        and plots the model coefficients depending on lambda (alpha)
    Parameters:
    -----------
    x: array_like
       predictors
    y: array_like
       labels
    """
    clf = Lasso()
    coefs = []

    labels = x.columns
    alphas = np.logspace(0, 3, 200)

    # scaling the data just like the book did it
    scaler = StandardScaler()
    x = scaler.fit_transform(x)

    # iterate over alphas and train models. store coefficients
    for a in alphas:
        clf.set_params(alpha=a)
        clf.fit(x, y)
        coefs.append(clf.coef_)

    plt.figure(figsize=(7, 7))
    ax = plt.gca()
    ax.plot(alphas, coefs)
    ax.set_xscale('log')
    ax.set_xlabel('lambda')
    ax.set_ylabel('weights')
    ax.set_title('Lasso coefficients as a function of the regularization')
    ax.axis('tight')
    ax.legend(labels)

    plt.show()


def fit_linear_reg(x, y):
    """ Fits a linear regression model

    Parameters:
    -----------
    x: array_like
       predictors
    y: array_like
       labels

    Returns:
    --------
    r_squared: float
               r^2 values
    adj_r_squared: float
                   adjusted r^2 values
    """
    mdl = LinearRegression()
    mdl.fit(x, y)
    r_squared = mdl.score(x, y)
    adj_r_squared = 1 - (1 - r_squared) * (y.shape[0] - 1) / (y.shape[0] - x.shape[1] - 1)

    return r_squared, adj_r_squared

###############################################################################
##
## Main
##
###############################################################################

def main(data_path):
    # read data and remove NaN
    dataset = pd.read_csv(data_path).dropna()
    # convert categorical data into numbers
    dataset = pd.get_dummies(dataset, columns=['Gender', 'Student', 'Married',
                                               'Ethnicity'], drop_first=True)

    y = dataset.Balance
    x = dataset.drop(columns='Balance', axis=1)  # everything without balance

    # calling the four task functions
    best_subset(x, y)
    forward_selection(x, y)
    ridge_regression(x, y)
    lasso_regression(x, y)




if __name__ == '__main__':
    main(data_path='Credit.csv')
