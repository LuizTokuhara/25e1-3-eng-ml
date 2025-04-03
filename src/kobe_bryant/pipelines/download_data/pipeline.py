"""
This is a boilerplate pipeline 'download_data'
generated using Kedro 0.19.11
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            nodes.download_data_dev,
            inputs=[],
            outputs='download_data_dev',
            tags=['DownloadData']
        ),
        node(
            nodes.download_data_prod,
            inputs=[],
            outputs='download_data_prod',
            tags=['DownloadData']
        )
    ])
