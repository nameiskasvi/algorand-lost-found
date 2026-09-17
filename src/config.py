import os

from dotenv import load_dotenv
from algosdk.v2client import algod, indexer


load_dotenv()


ALGOD_ADDRESS = os.getenv(
    "ALGOD_ADDRESS",
    "https://testnet-api.algonode.cloud",
)

ALGOD_TOKEN = os.getenv(
    "ALGOD_TOKEN",
    "",
)

INDEXER_ADDRESS = os.getenv(
    "INDEXER_ADDRESS",
    "https://testnet-idx.algonode.cloud",
)

INDEXER_TOKEN = os.getenv(
    "INDEXER_TOKEN",
    "",
)

ACCOUNT_MNEMONIC = os.getenv(
    "ACCOUNT_MNEMONIC",
    "",
)


def get_algod_client() -> algod.AlgodClient:
    """Return an Algod client for Algorand TestNet."""

    return algod.AlgodClient(
        ALGOD_TOKEN,
        ALGOD_ADDRESS,
    )


def get_indexer_client() -> indexer.IndexerClient:
    """Return an Indexer client for Algorand TestNet."""

    return indexer.IndexerClient(
        INDEXER_TOKEN,
        INDEXER_ADDRESS,
    )
