"""
This is a boilerplate pipeline 'preparacao_dados'
generated using Kedro 0.19.11
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from . import nodes

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            nodes.preparacao_dados_dev,
            inputs=['download_data_dev'],
            outputs='filtered_data',
            tags=['PreparacaoDados']
        ),
        node(
            nodes.treino_teste,
            inputs=['filtered_data'],
            outputs=['base_train', 'base_test'],
            tags=['PreparacaoDados']
        )
    ])
