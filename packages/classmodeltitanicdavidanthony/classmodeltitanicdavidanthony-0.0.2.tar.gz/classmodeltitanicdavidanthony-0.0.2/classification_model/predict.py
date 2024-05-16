import typing as t
import pandas as pd

#from processing.data_manager import load_dataset
from classification_model import __version__ as _version
from classification_model.config.core import config
from classification_model.processing.data_manager import load_pipeline
from classification_model.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_titanic_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(
    *,
    data_input: t.Union[pd.DataFrame, dict],
) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(data_input)
    validated_data, errors = validate_inputs(input_data=data)
    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        predictions = _titanic_pipe.predict(
            X=validated_data[config.model_config.features]
        )
        # predictions_prob_ = _titanic_pipe.predict_proba(
        #     X=validated_data[config.model_config.features]
        # )[:,1]
        results = {
            "predictions": predictions,
            "version": _version,
            "errors": errors,
        }

    return results
