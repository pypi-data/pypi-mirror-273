# pylint: disable=E0401,R0914,C0103
"""This module contains the DataProcessor class for processing data for the model."""

import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import joblib


class DataProcessor:
    """
    Class to process data for the model

    """
    def __init__(self, token_path=None, enc_path=None, sequence_length=200):
        self.sequence_length = sequence_length

        if enc_path:
            self.encoder = joblib.load(enc_path)
        else:
            self.encoder = LabelEncoder()

        if token_path:
            self.tokenizer = joblib.load(token_path)
        else:
            self.tokenizer = Tokenizer(char_level=True,lower=True, oov_token = '-n-')


    @staticmethod
    def raw_to_df(content):
        """
        Convert raw content to a pandas DataFrame.

        Args:
            content (str): The raw content to be processed.

        Returns:
            pandas.DataFrame: A DataFrame containing the processed data
            with columns 'label' and 'url'.
        """
        content_lines = content.split("\n")
        raw_data = [line.strip() for line in content_lines]
        raw_urls = [line.split("\t")[1] for line in raw_data]
        raw_labels = [line.split("\t")[0] for line in raw_data]
        df = pd.DataFrame({"label": raw_labels, "url": raw_urls})
        return df

    def tokenize_pad_data(self, data):
        """
        Tokenize and pad data sequences
        """
        return pad_sequences(
            self.tokenizer.texts_to_sequences(data),
            maxlen=self.sequence_length
        )

    def tokenize_pad_encode_data(self, train, val, test):
        """
        Tokenizes, pads, and encodes the data for training, validation, and testing.

        Args:
            train (DataFrame): The training data.
            val (DataFrame): The validation data.
            test (DataFrame): The testing data.

        Returns:
            dict: A dictionary containing the following:
                - "tokenizer": The tokenizer used for tokenization.
                - "char_index": The word index of the tokenizer.
                - "url_train": The tokenized and padded training data.
                - "url_val": The tokenized and padded validation data.
                - "url_test": The tokenized and padded testing data.
                - "label_train": The encoded training labels.
                - "label_val": The encoded validation labels.
                - "label_test": The encoded testing labels.
        """
        raw_x_train, raw_y_train = (train["url"].values, train["label"].values)
        raw_x_test, raw_y_test = (val["url"].values, val["label"].values)
        raw_x_val, raw_y_val = (test["url"].values, test["label"].values)

        self.tokenizer.fit_on_texts(
            raw_x_train.tolist() + raw_x_val.tolist() + raw_x_test.tolist()
        )

        x_train = self.tokenize_pad_data(raw_x_train)
        x_val = self.tokenize_pad_data(raw_x_val)
        x_test = self.tokenize_pad_data(raw_x_test)

        y_train = self.encoder.fit_transform(raw_y_train)
        y_val = self.encoder.transform(raw_y_val)
        y_test = self.encoder.transform(raw_y_test)

        return {
            "tokenizer": self.tokenizer,
            "char_index": self.tokenizer.word_index,
            "url_train": x_train,
            "url_val": x_val,
            "url_test": x_test,
            "label_train": y_train,
            "label_val": y_val,
            "label_test": y_test,
        }


    @staticmethod
    def dump_data(data, path):
        """
        Save data to given path into joblib format
        """
        joblib.dump(data, path)

    def dump_tokenizer(self, path):
        """
        Save tokenizer to given path into joblib format
        """
        joblib.dump(self.tokenizer, path)

    def dump_encoder(self, path):
        """
        Save encoder to given path into joblib format
        """
        joblib.dump(self.encoder, path)

    @staticmethod
    def save_csv(df, file_path, index=False):
        """
        Save a pandas DataFrame to a CSV file for a given path
        """
        df.to_csv(file_path, index=index)
