import numpy as np
from config.core import config
from pipeline import titanic_pipe
from processing.data_manager import load_dataset, save_pipeline,save_feature_importance
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance # feature importance



def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.app_config.titanic_data)

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  # predictors
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.model_config.random_state,
    )
    # fit model
    titanic_pipe.fit(X_train, y_train)

    # compute importances and save it
    model_fi = permutation_importance(titanic_pipe, X_train, y_train, n_repeats=30,
                                       random_state=config.model_config.random_state, n_jobs=2)
    perm_sorted_idx = model_fi.importances_mean.argsort()
    labels_idx = X_train.columns[perm_sorted_idx].tolist() 
    importance_val = model_fi.importances[perm_sorted_idx].T
    importance_dict = {}
    for i in range(len(labels_idx)):
        importance_dict[labels_idx[i]] = importance_val[:,i].tolist()
    # persist trained model
    save_pipeline(pipeline_to_persist=titanic_pipe)

    # Save feature importance
    save_feature_importance(features_imp=importance_dict)


if __name__ == "__main__":
    run_training()
