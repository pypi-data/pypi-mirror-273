import logging
import os
from typing import Literal

import coloredlogs
import torch
from chromadb.api import ClientAPI


def setup_logging(
    logger_name: str = "bilby_commodities", logfile_name: str | None = "events.log"
) -> None:
    coloredlogs.install()

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    if logfile_name is None:
        logfile_name = "events.log"

    file_handler = logging.FileHandler(logfile_name)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[file_handler, console_handler],
    )


def flatten[T](list_of_lists: list[list[T]]) -> list[T]:
    return [item for sublist in list_of_lists for item in sublist]


def get_torch_device_by_availability() -> Literal["cuda", "mps", "cpu"]:
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"


def delete_chroma_collection_if_exists(chroma_client: ClientAPI, collection_name: str) -> None:
    if collection_name in chroma_client.list_collections():
        logging.info(f"Deleting Chroma collection: {collection_name}")
        chroma_client.delete_collection(collection_name)
    else:
        logging.info(f"Chroma collection: {collection_name} not found, continuing...")


def is_capitalized(text: str) -> bool:
    # maybe use regex?
    for index, word in enumerate(text.split(" ")):
        if index != 0 and word in [
            "a",
            "an",
            "and",
            "as",
            "at",
            "but",
            "by",
            "for",
            "in",
            "nor",
            "of",
            "on",
            "or",
            "the",
            "to",
            "up",
            "yet",
        ]:
            continue
        if word[0].isalpha() and not word[0].isupper():
            return False
    return True


def assert_env_is_set(key: str) -> None:
    if key not in os.environ:
        error_msg = f"Environment variable {key} is not set"
        logging.error(error_msg)
        raise ValueError(error_msg)
