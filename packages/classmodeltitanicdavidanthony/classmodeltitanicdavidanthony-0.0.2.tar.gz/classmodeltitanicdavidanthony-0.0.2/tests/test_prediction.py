import math

import numpy as np

from classification_model.predict import make_prediction
from sklearn.metrics import accuracy_score
from classification_model.config.core import config


def test_make_prediction(sample_input_data):
    y_true = sample_input_data[config.model_config.target]
    sample_input_data.drop(columns=[config.model_config.target],inplace=True)
    # Given
    expected_no_predictions = 262

    # When
    result = make_prediction(data_input=sample_input_data)
    #print(result.get("errors"))

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, np.ndarray)
    assert isinstance(predictions[0], np.int64)
    assert result.get("errors") is None
    assert len(predictions) == expected_no_predictions
    _predictions = list(predictions)
    accuracy = accuracy_score(_predictions, y_true)
    assert accuracy > 0.7 #accuracy = 0.7137
