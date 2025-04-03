"""
This is a boilerplate pipeline 'pipeline_aplicacao'
generated using Kedro 0.19.12
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from . import nodes

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            nodes.application_pipeline,
            inputs=['download_data_prod'],
            outputs='aplicacao_artifact',
            tags=['AplicacaoPipeline']
        )
    ])
