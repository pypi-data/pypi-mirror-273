import logging
from typing import Any, Type

from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk
from pandas import DataFrame
from pydantic import BaseModel

logger = logging.getLogger(__name__)


def create_index_with_mapping_if_not_exists(client: Elasticsearch, index: str, mappings) -> None:
    if not client.indices.exists(index=index):
        logger.info(f"Creating index: {index}")
        client.indices.create(index=index, mappings=mappings)
    else:
        logger.info(f"Tried to create index `{index}` but it already exists. Continuing.")


def delete_index_if_exists(client: Elasticsearch, index: str) -> None:
    if client.indices.exists(index=index):
        logger.info(f"Deleting index: {index}")
        client.indices.delete(index=index, ignore_unavailable=True)
    else:
        logger.info(f"Tried to delete index `{index}` but it does not exist. Continuing.")


def _records_to_actions(df: DataFrame, index: str, *, id_column="id", doctype="doc"):
    for record in df.to_dict(orient="records"):
        yield {
            "_op_type": "index",  # defaults to index, just being explicit
            "_index": index,
            "_id": record[id_column],
            "_source": record,
        }


def validate_basemodel_to_mapping(
    model: Type[BaseModel], mappings: dict[str, dict[str, Any]]
) -> bool:
    if "properties" not in mappings:
        logger.error("No 'properties' key found in mappings")
        return False

    # each field in basemodel should be present in mappings
    for field in model.model_fields.keys():
        if field not in mappings["properties"]:
            logger.error(f"Field '{field}' not found in mappings")
            return False

    # each field in mappings should be present in basemodel
    for field in mappings["properties"].keys():
        if field not in model.model_fields.keys():
            logger.error(f"Field '{field}' not found in pydantic model")
            return False

    return True


def upload_to_elastic(
    client: Elasticsearch,
    df: DataFrame,
    *,
    index: str,
):
    logger.info(f"Uploading {len(df)} records to index: {index}")
    for success, info in parallel_bulk(
        client=client,
        actions=_records_to_actions(df, index),
    ):
        logger.info(f"Indexing record: {info}")
        if not success:
            logger.error(
                f"""Failed to index record: {info}.
                Checklist:
                - Did you convert dates using pd.to_datetime?
                - Did you replace all NaN values with None?
                """
            )
        else:
            logger.info(f"Successfully indexed record: {info}")
