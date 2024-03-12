# -*- coding: utf-8 -*-
# @Author: Simon Walser
# @Date:   2021-09-23 11:07:57
# @Last Modified by:   Simon Walser
# @Last Modified time: 2021-09-23 11:41:08
import string, unicodedata
import nltk
import contractions
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tag.perceptron import PerceptronTagger
from nltk.corpus import wordnet
from nltk.tag import pos_tag_sents
from nltk.tag.mapping import map_tag

import numpy as np
import pandas as pd
import multiprocessing as mp

from sklearn.base import TransformerMixin, BaseEstimator

# inspired by:
# https://towardsdatascience.com/text-preprocessing-steps-and-universal-pipeline-94233cb6725a
# https://www.kdnuggets.com/2018/03/text-data-preprocessing-walkthrough-python.html
class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self,
                 language = "english",
                 unicodedata = True,
                 clean_html = False,
                 replace_contractions = True,
                 remove_numbers = True,
                 punctuations = None,
                 stopwords = None,
                 pos_tags = None,
                 lemmantize = True,
                 stem = False,
                 alpha_only = False,
                 min_length = 1,
                 max_length = 15,
                 n_jobs = 1):
        """
        Text preprocessing transformer includes steps:
            1. Text normalization and cleanup
            2. POS tag retention
            3. Lemmatization
            4. Stemming

        language - the language
        unicodedata - makes sure characters which look identical are identical (é -> e)
        clean_html - cleans up HTLM tags
        replace_contractions - Replaces e.g. "I'm" with "I am"
        remove_numbers - Removes numbers
        punctuations - An user defined punctuation set
        stopwords - An user defined stop word set (None for default)
        pos_tags - An user defined POS tag set that should be kept
        lemmantize - Defines if lemmantization should be applied
        stem - Defines if stemming should be applied
        min_length - Defines the min length of a string
        max_length - Defines the max length of a string
        n_jobs - parallel jobs to run
        """
        self.language = language
        self.unicodedata = unicodedata
        self.clean_html = clean_html
        self.replace_contractions = replace_contractions
        self.remove_numbers = remove_numbers
        self.punctuations = punctuations
        self.stopwords = stopwords
        self.pos_tags = pos_tags
        self.lemmantize = lemmantize
        self.stem = stem
        self.min_length = min_length
        self.max_length = max_length
        self.n_jobs = n_jobs
        self.alpha_only = alpha_only

    def fit(self, X, y=None):
        return self

    def transform(self, X, *_):
        X_copy = X.copy()

        partitions = 1
        cores = mp.cpu_count()
        if self.n_jobs <= -1:
            partitions = cores
        elif self.n_jobs <= 0:
            return X_copy.apply(self.preprocess_text)
        else:
            partitions = min(self.n_jobs, cores)

        data_split = np.array_split(X_copy, partitions)
        pool = mp.Pool(cores)
        data = pd.concat(pool.map(self._preprocess_part, data_split))
        pool.close()
        pool.join()

        return data

    def _preprocess_part(self, part):
        return part.apply(self.preprocess_text)

    def preprocess_text(self, text):
        return ' '.join(self.normalize(text))

    def _get_wordnet_pos(self, tag):
        """Map POS tag to first character lemmatize() accepts"""
        tag = tag.upper()

        if tag == "J":
            return wordnet.ADJ
        elif tag == "N":
            return wordnet.NOUN
        elif tag == "V":
            return wordnet.VERB
        elif tag == "R":
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def _tag(self, text):
        tags = [self._get_wordnet_pos(nltk.pos_tag([w])[0][1][0]) for w in text]

        #tagger = PerceptronTagger()
        #tags = tagger.tag(text)
        #tags = [self._get_wordnet_pos(tag[1]) for tag in tags]
        #tags = [self._get_wordnet_pos(map_tag('en-ptb', None, tag[1])) for tag in tags]

        #tags = pos_tag_sents(text)
        #tags = [self._get_wordnet_pos(tag[1][0]) for tag in tags[0]]

        return tags

    def normalize(self, text):
        # START: Your code goes here
        #return [word_tokenize(text.lower())]
        # END: Dummy code

        if self.clean_html:
            soup  = BeautifulSoup(text, 'html.parser')
            text = soup.get_text()
            '''
            text = soup.find_all(text=True)
            output = []
            blacklist = ['[document]','noscript','header','html','meta','head','input','script','style']

            for t in text:
                if t.parent.name not in blacklist:
                    output.append('{}'.format(t))

            text = ' '.join(output)
            '''

        if self.unicodedata:
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

        if self.replace_contractions:
            text = contractions.fix(text)

        stop_words = None
        if self.stopwords is None:
            # use default (use none -> user provides empty set)
            stop_words=set(stopwords.words(self.language))
        else:
            stop_words=self.stopwords

        punct_words = None
        if self.punctuations is None:
            # use default (use none -> user provides empty set)
            punct_words = set(string.punctuation)
        else:
            punct_words = self.punctuations

        normalized = [w for w in word_tokenize(text.lower())
                  if
                     (not w in punct_words)
                  and
                     (not w in stop_words)
                  and
                     ((not self.remove_numbers) or (not w.isdigit()))
                  and
                     ((self.min_length < len(w)) and (len(w) < self.max_length))
                  ]

        if self.alpha_only:
            normalized = [w for w in normalized if w.isalpha()]

        tagged = None
        if self.pos_tags is not None:
            tagged = self._tag(normalized)

            normalized = [w for (w, tag) in zip(normalized, tagged) if tag in self.pos_tags]
            tagged = [tag for tag in tagged if tag in self.pos_tags]
            #normalized = [w for w in normalized if self._get_wordnet_pos(w) in self.pos_tags]

        if self.lemmantize:
            if tagged is None:
                tagged = self._tag(normalized)

            lemmatizer = WordNetLemmatizer()
            normalized = [lemmatizer.lemmatize(w, tag) for (w, tag) in zip(normalized, tagged)]
            #normalized = [lemmatizer.lemmatize(w, self._get_wordnet_pos(w)) for w in normalized]

        if self.stem:
            stemmer = SnowballStemmer(self.language)
            normalized = [stemmer.stem(w) for w in normalized]

        return normalized
        # END: Your code goes here

