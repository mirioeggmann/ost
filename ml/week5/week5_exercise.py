# -*- coding: utf-8 -*-
# @Author: Simon Walser
# @Date:   2021-09-29 09:24:21
# @Last Modified by:   Simon Walser
# @Last Modified time: 2021-10-01 11:50:03

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from utilities.plotting_stuff import plot_logistic_regression


################################################################################
#
# Class / Function definitions
#
################################################################################


def read_data(path):
    df = pd.read_csv(path, delimiter=';')
    return df


def preprocess_data(df):
    # Select subset
    df_subset = df.loc[:,['Gemessen am', 'Passanten in Richtung Neumarkt','Passanten in Richtung Multergasse']].copy()
    df_subset.rename({'Gemessen am':'date',
                      'Passanten in Richtung Neumarkt':'x1',
                      'Passanten in Richtung Multergasse':'x2'}, inplace=True, axis=1)

    # Sort values by time and drop duplicates
    df_subset.sort_values('date', ascending=True, inplace=True)
    df_subset = df_subset.drop_duplicates('date')
    df_subset.date = pd.to_datetime(df_subset.date, yearfirst=True, utc=True).dt.tz_localize(None)
    df_subset.reset_index(drop=True, inplace=True)

    # Create classification dataframe
    df_predict = pd.DataFrame({'y':['day']*len(df_subset),
                               'x1':df_subset.x1,
                               'x2':df_subset.x2,
                               'date':df_subset.date})
    mask = (df_subset.date.dt.hour <= 3) | (df_subset.date.dt.hour >= 19)
    df_predict.loc[mask, 'y'] = 'night'

    return df_predict


def plot_data(df):
    fig1 ,axes = plt.subplots(2,1, figsize=(10,5))
    sns.histplot(data=df, x='x1', hue='y', kde=True, palette=sns.color_palette('bright')[:2], ax=axes[0], bins=100)
    sns.histplot(data=df, x='x2', hue='y', kde=True, palette=sns.color_palette('bright')[:2], ax=axes[1], bins=100)
    axes[0].set_title('Neumarkt')
    axes[1].set_title('Multergasse')

    fig2, ax = plt.subplots(1,1, figsize=(10,5))
    ax.plot(df.date, df.x1, c='b', alpha=0.5, label='Neumarkt')
    ax.plot(df.date, df.x2, c='r', alpha=0.5, label='Multergasse')
    ax.set_title('Datetime vs. Pedestrian')
    ax.set_xlabel('Datetime')
    ax.set_ylabel('Number of Pedestrian')
    ax.legend(loc='best')

    plt.show()


def fit_logistic_regression(X, y):
    # TODO: Implement logistic regression model, fit it to the training data (X,y)
    # and return it

    return model


def evaluate_logistic_regression(model, X, y):
    # TODO: Calculate the Mean Accuracy based on the test data (X,y)
    # and print the result

    print('Model: {:100s} | Mean Accuracy: {:6.4f}'.format(re.sub('\n\s+','',str(model)),score))


def main(src_path):
    # Load, prepare and visualize data
    df = read_data(src_path)
    df = preprocess_data(df)
    plot_data(df)

    # TODO: Create train-test split
    # df_train, df_test = ...

    # TODO: Invoke function fit_logistic_regression with the appropriate data

    # TODO: Invoke function evaluate_logistic_regression with the appropriate data

    # Plot result
    plot_logistic_regression(model, df_test[['x1','x2']], df_test.y)


################################################################################
#
# Main functions
#
################################################################################


if __name__ == "__main__":
    src_path = 'fussganger_vadianstrasse.csv'

    main(src_path)
