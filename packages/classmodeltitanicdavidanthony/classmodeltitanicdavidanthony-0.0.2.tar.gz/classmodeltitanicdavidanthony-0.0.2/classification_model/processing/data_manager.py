import logging
import typing as t
from typing import Any, Union
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
import numpy as np
from classification_model import __version__ as _version
from classification_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config
import re
import json

logger = logging.getLogger(__name__)


# retain only the first cabin if more than
# 1 are available per passenger
# float type for np.nan
def get_first_cabin(row: Any) -> Union[str, float]:
    try:
        return row.split()[0]
    except AttributeError:
        return np.nan

# extracts the title (Mr, Ms, etc) from the name variable
def get_title(passenger: str) -> str:
    line = passenger
    if re.search('Mrs', line):
        return 'Mrs'
    elif re.search('Mr', line):
        return 'Mr'
    elif re.search('Miss', line):
        return 'Miss'
    elif re.search('Master', line):
        return 'Master'
    else:
        return 'Other'

def pre_processing(*, dataframe:pd.DataFrame) -> pd.DataFrame:
    # replace interrogation marks by NaN values
    dataframe = dataframe.replace('?', np.nan)

    # retain only the first cabin if more than
    dataframe[config.model_config.CABIN] = dataframe[config.model_config.CABIN].apply(get_first_cabin)

    # extracts the title (Mr, Ms, etc) from the name variable
    dataframe['title'] = dataframe['name'].apply(get_title)

    # cast numerical variables as floats
    dataframe['fare'] = dataframe['fare'].astype('float')
    dataframe['age'] = dataframe['age'].astype('float')

    # drop unnecessary variables
    dataframe.drop(labels=config.model_config.unused_fields, axis=1, inplace=True)

    return dataframe


def _load_raw_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    return dataframe

def load_dataset(*, file_name: str) -> pd.DataFrame:
    input_data = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    transformed = pre_processing(dataframe=input_data)
    return transformed


def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    """Persist the pipeline.
    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)

def save_feature_importance(*, features_imp: dict) -> None:
    """Features importance saving.
    Saves the versioned  
    """
    # Prepare versioned save file name
    save_file_name = f"{config.app_config.feature_importance_save}{_version}.json"
    save_path = TRAINED_MODEL_DIR / save_file_name
    #print(save_path)

    # Write data to the JSON file
    with open(save_path, "w") as json_file:
        #print(json_file)
        #print(features_imp)
        json.dump(features_imp, json_file)
    #joblib.dump(features_imp, save_path)

def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model


def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
