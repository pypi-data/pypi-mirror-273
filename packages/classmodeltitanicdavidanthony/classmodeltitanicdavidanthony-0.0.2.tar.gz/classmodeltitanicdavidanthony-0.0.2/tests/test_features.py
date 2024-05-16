from classification_model.config.core import config
from classification_model.processing.features import ExtractLetterTransformer


def test_extractletter_variable_transformer(sample_input_data):
    # Given
    #print(sample_input_data.loc[5,'cabin'])
    transformer = ExtractLetterTransformer(
        variable=config.model_config.CABIN,  # cabin
    )
    assert sample_input_data[config.model_config.CABIN].iat[5] == 'G6'

    # When
    subject = transformer.fit_transform(sample_input_data)

    # Then
    assert subject[config.model_config.CABIN].iat[5] == 'G'
