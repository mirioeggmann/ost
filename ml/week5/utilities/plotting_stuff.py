# -*- coding: utf-8 -*-
# @Author: Simon Walser
# @Date:   2021-10-01 11:18:12
# @Last Modified by:   Simon Walser
# @Last Modified time: 2021-10-01 11:21:11

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.cm import coolwarm

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


################################################################################
#
# Class / Function definitions
#
################################################################################


def plot_logistic_regression(model, X, y):

    if model.n_features_in_ == 2:
        xx, yy = np.meshgrid(np.linspace(-10, 60, 60),
                             np.linspace(-10, 60, 60))

        X_plot = np.hstack([xx.reshape([-1,1]), yy.reshape([-1,1])])
        zz = model.predict_proba(X_plot)[:,0].reshape(xx.shape)

        z_scatter = np.zeros(y.shape)
        z_scatter[y=='day'] = 1

        labels = model.predict(X)
        z_color = np.zeros(labels.shape)
        z_color[labels=='day'] = 1

        # Display result
        fig = plt.figure(figsize=(5,5))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(xx, yy, zz, cmap=coolwarm, alpha=0.5)
        ax.contour(xx, yy, zz, levels=10, zdir='z', cmap=coolwarm, offset=0)
        ax.contour(xx, yy, zz, levels=10, zdir='z', cmap=coolwarm, alpha=1)
        ax.scatter(X.x1, X.x2, z_scatter, s=5, c=z_color)

        ax.set_xlim(-10, 60)
        ax.set_ylim(-10, 60)
        ax.set_zlim(0, 1.1)

        ax.set_xlabel(X.columns[0])
        ax.set_ylabel(X.columns[1])
        ax.set_zlabel('P(day | pedestrian)')

        plt.show()

    elif model.n_features_in_ == 1:
        xx = np.linspace(-10, 60, 60)
        zz = model.predict_proba(xx[:,np.newaxis])[:,0]

        z_scatter = np.zeros(y.shape)
        z_scatter[y=='day'] = 1

        labels = model.predict(X)
        z_color = np.zeros(labels.shape)
        z_color[labels=='day'] = 1

        # Display result
        fig = plt.figure(figsize=(5,5))
        ax = fig.add_subplot(111)
        ax.plot(xx, zz)
        ax.scatter(X, z_scatter, s=5, c=z_color)

        ax.set_xlim(-10, 60)
        ax.set_ylim(0, 1.1)

        ax.set_xlabel(X.columns[0])
        ax.set_ylabel('P(day | pedestrian)')
        ax.grid('on')

        # Find and plot decision boundary
        if isinstance(model, Pipeline):
            d_boundary = -model['linreg'].intercept_/model['linreg'].coef_[0]*model['scaler'].scale_+model['scaler'].mean_
        elif isinstance(model, LogisticRegression):
            d_boundary = -model.intercept_/model.coef_[0]

        ax.axhline(0.5, c='k')
        ax.axvline(d_boundary, c='k')

        plt.show()
    else:
        raise ValueError('Invalid number of features for plot function')
