"""
SOLUTION

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
from my_lda_solution import LDA
from my_lda_solution import QDA


def main(data_path):
    # read data and convert it to kg and cm (from punds and inches)
    data = pd.read_csv(data_path)
    data.Weight = data.Weight*0.45359237
    data.Height = data.Height*2.54

    # shuffle and generate test and training split
    train_data, test_data = train_test_split(data, test_size=0.3, random_state=0)

    # plot data to get an idea of the data set
    plot_height_weight(train_data)

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

    # generate LDA and QDA models and fit them to the training data
    # lda = LinearDiscriminantAnalysis(store_covariance=True)
    lda = LDA()
    qda = QuadraticDiscriminantAnalysis()
    # qda = QDA()
    qda.fit(x_train, y_train)
    lda.fit(x_train, y_train)

    # calculate misclassification from LDA and QDA on train and test data
    # What do you notice?
    qda_misclassification_train = 1 - qda.score(x_train, y_train)
    lda_misclassification_train = 1 - lda.score(x_train, y_train)
    qda_misclassification_test = 1 - qda.score(x_test, y_test)
    lda_misclassification_test = 1 - lda.score(x_test, y_test)

    print("LDA Train: {:.4f}\nLDA Test: {:.4f}".format(lda_misclassification_train,
                                                       lda_misclassification_test))
    print("QDA Train: {:.4f}\nQDA Test: {:.4f}".format(qda_misclassification_train,
                                                       qda_misclassification_test))

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
