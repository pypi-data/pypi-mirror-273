import pandas as pd
import numpy as np

class Preprocessing:
    """
    A class for performing data preprocessing operations.
    
    Attributes:
    data (DataFrame): The input DataFrame to be preprocessed.
    """

    def __init__(self, data):
        """
        Initializes the Preprocessing class with input data.

        Args:
        data (DataFrame): The input DataFrame to be preprocessed.
        """
        self.data = data

    def remove_duplicates(self):
        """
        Removes duplicate rows from the DataFrame.
        """
        self.data = self.data.drop_duplicates()

    def remove_null_values(self):
        """
        Removes rows containing null values from the DataFrame.
        """
        self.data = self.data.dropna()

    def replace_null_values(self, value):
        """
        Replaces null values in the DataFrame with the specified value.

        Args:
        value: The value to replace null values with.
        """
        self.data = self.data.fillna(value)

    def remove_outliers(self, column, threshold=3):
        """
        Removes outliers from a specific column using z-score method.

        Args:
        column (str): The name of the column to remove outliers from.
        threshold (float, optional): The threshold value for outlier detection. Defaults to 3.
        """
        z_scores = np.abs((self.data[column] - self.data[column].mean()) / self.data[column].std())
        self.data = self.data[z_scores < threshold]

    def standardize_column_names(self):
        """
        Standardizes column names by converting them to lowercase and replacing spaces with underscores.
        """
        self.data.columns = [col.strip().lower().replace(' ', '_') for col in self.data.columns]

    def preprocess_data(self):
        """
        Performs all preprocessing steps: removing duplicates, null values, and standardizing column names.
        """
        self.remove_duplicates()
        self.remove_null_values()
        self.standardize_column_names()

