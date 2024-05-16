from feature_engine.encoding import OneHotEncoder
from feature_engine.imputation import AddMissingIndicator, CategoricalImputer, MeanMedianImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# feature scaling
from sklearn.preprocessing import StandardScaler



from classification_model.config.core import config
from classification_model.processing import features as pp

# set up the pipeline
titanic_pipe = Pipeline([

    # ===== IMPUTATION =====
    # impute categorical variables with string missing
    ('categorical_imputation', CategoricalImputer(
        imputation_method='missing', variables=config.model_config.CATEGORICAL_VARIABLES
    )
    ),

    # add missing indicator to numerical variables
    ('missing_indicator', AddMissingIndicator(variables=config.model_config.NUMERICAL_VARIABLES)),

    # impute numerical variables with the median
    ('median_imputation', MeanMedianImputer(
        imputation_method='median', variables=config.model_config.NUMERICAL_VARIABLES)),


    # Extract letter from cabin
    ('extract_letter', pp.ExtractLetterTransformer(variable=config.model_config.CABIN)),
    
    # == CATEGORICAL ENCODING ======
    # remove categories present in less than 5% of the observations (0.05)
    # group them in one category called 'Rare'
    ('rare_label_encoder', pp.RareLabelCategoricalEncoder(variables=config.model_config.CATEGORICAL_VARIABLES,
                                         rare_perc=config.model_config.rare_perc)),

    # encode categorical variables using one hot encoding into k-1 variables
    ('categorical_encoder', OneHotEncoder(
        drop_last=True, variables=config.model_config.CATEGORICAL_VARIABLES)),

    # scale
    ('scaler', StandardScaler()),
    ('Logit', LogisticRegression(C=config.model_config.C, random_state=config.model_config.random_state)
),
]
)

