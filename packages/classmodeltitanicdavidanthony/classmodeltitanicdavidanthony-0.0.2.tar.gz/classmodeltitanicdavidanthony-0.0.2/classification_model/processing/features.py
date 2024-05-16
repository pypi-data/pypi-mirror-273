from typing import List

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import re


class ExtractLetterTransformer(BaseEstimator, TransformerMixin):
    # Extract fist letter of variable

    def __init__(self, variable: str):
        self.variable = variable

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # so that we do not over-write the original dataframe
        X = X.copy()
        
        X[self.variable] = X[self.variable].str[0]

        return X

class RareLabelCategoricalEncoder(BaseEstimator, TransformerMixin):
    """Groups infrequent categories into a single string"""

    def __init__(self, variables, rare_perc):

        if not isinstance(variables, list):
            raise ValueError('variables should be a list')
        
        self.rare_perc = rare_perc
        self.variables = variables

    def fit(self, X:pd.DataFrame, y=None):
        # persist frequent labels in dictionary
        self.encoder_dict_ = {}

        for var in self.variables:
            # the encoder will learn the most frequent categories
            t = pd.Series(X[var].value_counts(normalize=True)) 
            # frequent labels:
            self.encoder_dict_[var] = list(t[t >= self.rare_perc].index)

        return self

    def transform(self, X):
        X = X.copy()
        for feature in self.variables:
            X[feature] = np.where(
                X[feature].isin(self.encoder_dict_[feature]),
                                X[feature], "Rare")
        return X