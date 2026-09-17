import os
from dotenv import load_dotenv
from algosdk.v2client import algod

load_dotenv()

ALGOD_ADDRESS = os.getenv("ALGOD_ADDRESS", "https://testnet-api.algonode.cloud")
ALGOD_TOKEN = os.getenv("ALGOD_TOKEN", "")
ACCOUNT_MNEMONIC = os.getenv("ACCOUNT_MNEMONIC", "")


def get_algod_client() -> algod.AlgodClient:
    return algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
