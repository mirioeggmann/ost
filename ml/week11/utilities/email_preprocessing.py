"""
Week11: Email preprocessor for SPAM classification

26.11.2019 / Sascha Jecklin

"""

import numpy as np
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer


class EmailPreprocessor():
    """ Preprocessr class for email. Has functions to tokenize email and return
    feature vectors

    Attributes
    ----------
    list : vocab_list
           list with vocables

    Methods
    -------
    email_preprocessing(email_content)
        Preprocesses an email. Returns tokens of the given mail.

    tokenize_email(email_content)
        Tokenizes an email.

    extract_features(word_indices, feature_count)
        Extracts features of an email.
    """

    def __init__(self, vocab_list):
        self.vocab_list = vocab_list

    def email_preprocessing(self, email_content):
        ''' Preprocesses an email. Returns tokens of the given mail.

        Parameters:
        ----------_
        email_content : list of string
                        each line of an email
        Returns:
        --------
        list : tokenized email
        '''
        # everything to lower case
        email_content = email_content.lower()
        # strip HTML stuff
        tag_pattern = re.compile('<[^<>]+>')
        email_content = tag_pattern.sub(' ', email_content)
        # replace numbers with the word 'number'
        number_pattern = re.compile('[0-9]+')
        email_content = number_pattern.sub('number', email_content)
        # replace URL with the word 'httpaddr'
        url_pattern = re.compile('(http|https)://[^\s]*')
        email_content = url_pattern.sub('httpaddr', email_content)
        # replace a mail adress with the word 'emailaddr'
        email_pattern = re.compile('[^\s]+@[^\s]+')
        email_content = email_pattern.sub('emailaddr', email_content)
        # replace dollar sign with the word 'dollar'
        dollar_pattern = re.compile('[$]+')
        email_content = dollar_pattern.sub('dollar', email_content)

        return self.tokenize_email(email_content)

    def tokenize_email(self, email_content):
        ''' Tokenizes an email
        Parameters:
        ----------_
        email_content : list of string
                        each line of an email
        Returns:
        --------
        list : tokenized email
        '''
        word_indices = []
        # remove punctuation and tokenize
        tokenizer = RegexpTokenizer('[a-zA-Z0-9]+[\']{0,1}[a-zA-Z0-9]+')
        tokens = tokenizer.tokenize(email_content)

        for token in tokens:
            # remove everything which is not number or letter
            non_alphanumeric_pattern = re.compile('[^a-zA-Z0-9]')
            token = non_alphanumeric_pattern.sub('', token)
            # word stemming
            stemmer = PorterStemmer()
            token = stemmer.stem(token.strip())
            # if word is in vocab_list append it
            if token in self.vocab_list:
                word_index = self.vocab_list.index(token)
                word_indices.append(word_index)
        return word_indices

    def extract_features(self, word_indices, feature_count):
        ''' Extracts features of an email.
        Parameters:
        -----------
        email_content : list of string
                        each line of an email
        Returns:
        --------
        list : tokenized email
        '''
        # create empty array for features
        email_features = np.zeros(feature_count)
        # mark feature as one
        email_features[word_indices] = email_features[word_indices] + 1
        return np.array(email_features)
