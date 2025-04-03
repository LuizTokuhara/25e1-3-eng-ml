"""
This is a boilerplate pipeline 'treinamento'
generated using Kedro 0.19.12
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            nodes.train_reg_log,
            inputs=['base_train', 'base_test'],
            outputs=["log_reg_model", "log_reg_metrics"],
            tags=['Treinamento']
        ),
        node(
            nodes.train_dec_tree,
            inputs=['base_train', 'base_test'],
            outputs=["dt_model", "dt_metrics"],
            tags=['Treinamento']
        )
    ])
