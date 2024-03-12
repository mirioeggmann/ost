"""
Week7: Using sklearn's LDA/QDA and own implementation

29.10.2019 / Sascha Jecklin

"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

from utilities.plotting_stuff import plot_height_weight
from utilities.plotting_stuff import plot_height_weight_mesh
from utilities.plotting_stuff import decimal_to_percent
from my_lda import LDA


def main(data_path):
    # read data and convert it to kg and cm (from pounds and inches)
    data = pd.read_csv(data_path)

    # TODO run the program despite the errors and study the data
    # plot data to get an idea of the data set
    plot_height_weight(data)
    plt.show()

    # TODO convert data from pounds and inches to kg and cm


    # shuffle and generate test and training split
    train_data, test_data = train_test_split(data, test_size=0.3)

    # extract predictors and labels
    x_train = train_data[['Height', 'Weight']].to_numpy()
    y_train = train_data['Gender'].to_numpy()
    x_test = test_data[['Height', 'Weight']].to_numpy()
    y_test = test_data['Gender'].to_numpy()

    # generate numerical classes from lables (Male and Female)
    le = preprocessing.LabelEncoder()
    le.fit(["Female", "Male"])
    y_train = le.transform(y_train)
    y_test = le.transform(y_test)

    # TODO generate LDA and QDA models using sklearn.discriminant_analysis and
    # fit them to the training data
    lda = 0
    qda = 0

    # TODO calculate misclassification from LDA and QDA on train and test data
    # and print it
    lda_misclassification_test = 0.0
    qda_misclassification_test = 0.0

    # TODO implement your own LDA model in the my_lda.py file and use this
    # instead of the one from sklearn.discriminant_analysis


    # TODO BONUS implement your own QDA model in the my_lda.py file and use
    # this instead of the one from sklearn.discriminant_analysis


    # plotting mesh to visualize LDA and QDA decision regions
    plot_height_weight_mesh(test_data, lda, 130, 210, 30, 130,
                            comment="Misclassification rate: " +
                            decimal_to_percent(lda_misclassification_test))
    plot_height_weight_mesh(test_data, qda, 130, 210, 30, 130,
                            comment="Misclassification rate: " +
                            decimal_to_percent(qda_misclassification_test))
    plt.show()


if __name__ == '__main__':
    main('weight-height.csv')
