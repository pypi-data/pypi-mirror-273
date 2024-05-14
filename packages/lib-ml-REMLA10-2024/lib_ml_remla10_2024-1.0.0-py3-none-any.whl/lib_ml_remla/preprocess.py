"""
Provides functions to preprocess data.

"""
import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras._tf_keras.keras.preprocessing.text import Tokenizer
from keras._tf_keras.keras.preprocessing.sequence import pad_sequences


def split_data(train: list[str], test: list[str], val: list[str]) -> tuple[list[str], list[str],list[str], list[str],
                                                                           list[str], list[str]]:
    """
    Split the data into training, validation, and test sets.

    Args:
        train: List of strings containing the training data.
        test: List of strings containing the test data.
        val: List of strings containing the validation data.

    Returns:
        Tuple of the split data in the form (X_train, y_train, X_val, y_val, X_test, y_test).
    """
    raw_X_train = [line.split("\t")[1] for line in train]
    raw_y_train = [line.split("\t")[0] for line in train]

    raw_X_test = [line.split("\t")[1] for line in test]
    raw_y_test = [line.split("\t")[0] for line in test]
    
    raw_X_val = [line.split("\t")[1] for line in val]
    raw_y_val = [line.split("\t")[0] for line in val]

    return raw_X_train, raw_y_train, raw_X_val, raw_y_val, raw_X_test, raw_y_test


def preprocess_data(raw_X_train: list[str], raw_y_train: list[str],
                    raw_X_val: list[str], raw_y_val: list[str],
                    raw_X_test: list[str], raw_y_test: list[str], sequence_length: int = 200
                    ) -> tuple[np.ndarray, np.ndarray, np.ndarray,
                               np.ndarray, np.ndarray, np.ndarray, dict[str, int], Tokenizer, LabelEncoder]:
    """
    Preprocess the data for training the model.

    Args:
        raw_X_train: List of strings containing the training data.
        raw_y_train: List of strings containing the training labels.
        raw_X_val: List of strings containing the validation data.
        raw_y_val: List of strings containing the validation labels.
        raw_X_test: List of strings containing the test data.
        raw_y_test: List of strings containing the test labels.
        sequence_length: The length of the sequences to pad the data to.

    Returns:
        Tuple of preprocessed data in the form (X_train, y_train, X_val, y_val, X_test, y_test, char_index).

    """
    # Tokenize the dataset
    tokenizer = Tokenizer(lower=True, char_level=True, oov_token='-n-')
    tokenizer.fit_on_texts(raw_X_train + raw_X_val + raw_X_test)
    char_index = tokenizer.word_index

    X_train = pad_sequences(tokenizer.texts_to_sequences(raw_X_train), maxlen=sequence_length)
    X_val = pad_sequences(tokenizer.texts_to_sequences(raw_X_val), maxlen=sequence_length)
    X_test = pad_sequences(tokenizer.texts_to_sequences(raw_X_test), maxlen=sequence_length)
    encoder = LabelEncoder()

    y_train = encoder.fit_transform(raw_y_train)
    y_val = encoder.transform(raw_y_val)
    y_test = encoder.transform(raw_y_test)

    return X_train, y_train, X_val, y_val, X_test, y_test, char_index, tokenizer, encoder

def prepare(raw_X_test: np.ndarray, tokenizer: Tokenizer, sequence_length: int=200):
    """
    Preprocesses X_test given a tokenizer

    Args:
        raw_x_test: Unprocessed test data.
        tokenizer: Tokenizer used to process the data

    Returns:
        Processed X_test
    """
    X_test = pad_sequences(tokenizer.texts_to_sequences(raw_X_test), maxlen=sequence_length)
    return X_test
