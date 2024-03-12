"""
Week11: random forest spam classifier

26.11.2019 / Sascha Jecklin

"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from utilities.email_preprocessing import EmailPreprocessor
from my_random_forest import MyRandomForestClassifier

###############################################################################
##
## Functions
##
###############################################################################

def classify_mail(mdl):
    """ Reads an email from a .txt file, prepares it and classifies as HAM
    or SPAM

    parameters
    ----------
    mdl : opject
          model trained on spam/ham mails
    """
    message = 'Enter the path/filename of a.txt file or type "q" to abort: '
    while True:
        file_name = input(message)
        if file_name == 'q':
            break
        else:
            # read mail
            vocab_file = open('utilities/vocab_list.txt', 'r')
            vocab_list = vocab_file.read().splitlines()
            email_file = open(file_name, 'r')
            email = email_file.read()

            # preprocess mail
            ep = EmailPreprocessor(vocab_list=vocab_list)
            word_indices = ep.email_preprocessing(email)
            email_features = ep.extract_features(word_indices, len(vocab_list))

            # make prediction
            email_classification = mdl.predict([email_features])
            if email_classification == 0:
                print('\n\tEmail is HAM\n')
            if email_classification == 1:
                print('\n\tEmail is SPAM\n')


###############################################################################
##
## Main
##
###############################################################################

def main():
    # read data
    x_train = pd.read_csv("data/training_features_spam.csv",
                          header=None, sep=';').values
    y_train = pd.read_csv("data/training_labels_spam.csv",
                          header=None, sep=';').values.ravel()
    x_test = pd.read_csv("data/test_features_spam.csv",
                         header=None, sep=';').values
    y_test = pd.read_csv("data/test_labels_spam.csv",
                         header=None, sep=';').values.ravel()

    # TODO: Use sklearn's RandomForestClassifier and fit it to training data

    # TODO: implement your own MyRandomForestClassifier and fit it to training 
    # data. See my_random_forest.py

    # TODO : using trained model to classify some unseen data
    classify_mail(mdl)


if __name__ == '__main__':
    main()
