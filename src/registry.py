import argparse
import base64
import json
from datetime import datetime, timezone

from algosdk import account, mnemonic
from algosdk.transaction import PaymentTxn, wait_for_confirmation

from .config import (
    ACCOUNT_MNEMONIC,
    get_algod_client,
    get_indexer_client,
)


PREFIX = "LFR1"

ALLOWED_ITEM_TYPES = {"lost", "found"}

MAX_ITEM_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500
MAX_LOCATION_LENGTH = 200


def validate_item(
    item_type: str,
    item: str,
    description: str,
    location: str,
) -> None:
    """Validate Lost & Found record data."""

    if item_type not in ALLOWED_ITEM_TYPES:
        raise ValueError(
            "Invalid item type. Use 'lost' or 'found'."
        )

    if not item or not item.strip():
        raise ValueError(
            "Item name cannot be empty."
        )

    if not description or not description.strip():
        raise ValueError(
            "Description cannot be empty."
        )

    if not location or not location.strip():
        raise ValueError(
            "Location cannot be empty."
        )

    if len(item.strip()) > MAX_ITEM_LENGTH:
        raise ValueError(
            f"Item name cannot exceed "
            f"{MAX_ITEM_LENGTH} characters."
        )

    if len(description.strip()) > MAX_DESCRIPTION_LENGTH:
        raise ValueError(
            f"Description cannot exceed "
            f"{MAX_DESCRIPTION_LENGTH} characters."
        )

    if len(location.strip()) > MAX_LOCATION_LENGTH:
        raise ValueError(
            f"Location cannot exceed "
            f"{MAX_LOCATION_LENGTH} characters."
        )


def build_note(
    item_type: str,
    item: str,
    description: str,
    location: str,
) -> bytes:
    """Build the JSON record stored in the Algorand transaction note."""

    validate_item(
        item_type,
        item,
        description,
        location,
    )

    payload = {
        "v": 1,
        "app": PREFIX,
        "type": item_type,
        "item": item.strip(),
        "description": description.strip(),
        "location": location.strip(),
        "reported_at": datetime.now(timezone.utc).isoformat(),
    }

    return json.dumps(
        payload,
        separators=(",", ":"),
    ).encode("utf-8")


def decode_registry_note(note_b64: str):
    """Decode a base64-encoded registry note."""

    try:
        note = json.loads(
            base64.b64decode(
                note_b64
            ).decode("utf-8")
        )
    except (
        ValueError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ):
        return None

    if note.get("app") != PREFIX:
        return None

    return note


def get_account_address() -> str:
    """Return the blockchain address derived from the configured mnemonic."""

    if not ACCOUNT_MNEMONIC:
        raise RuntimeError(
            "ACCOUNT_MNEMONIC is not configured. "
            "Copy .env.example to .env and add a TestNet mnemonic."
        )

    private_key = mnemonic.to_private_key(
        ACCOUNT_MNEMONIC
    )

    return account.address_from_private_key(
        private_key
    )


def register_item(
    item_type: str,
    item: str,
    description: str,
    location: str,
) -> str:
    """Register a lost/found item on Algorand TestNet."""

    validate_item(
        item_type,
        item,
        description,
        location,
    )

    sender = get_account_address()

    client = get_algod_client()

    params = client.suggested_params()

    note = build_note(
        item_type,
        item,
        description,
        location,
    )

    # A self-transfer is used for the MVP.
    # No ALGO is transferred to another account.
    txn = PaymentTxn(
        sender=sender,
        sp=params,
        receiver=sender,
        amt=0,
        note=note,
    )

    # Compatible with the installed
    # py-algorand-sdk version.
    signed = txn.sign(
        mnemonic.to_private_key(
            ACCOUNT_MNEMONIC
        )
    )

    txid = client.send_transaction(
        signed
    )

    wait_for_confirmation(
        client,
        txid,
        4,
    )

    return txid


def verify_transaction(txid: str):
    """Verify and decode a Lost & Found registry transaction."""

    if not txid or not txid.strip():
        return {
            "verified": False,
            "reason": "Transaction ID cannot be empty.",
        }

    client = get_algod_client()

    try:
        info = client.pending_transaction_info(
            txid.strip()
        )
    except Exception as exc:
        return {
            "verified": False,
            "reason": (
                f"Could not retrieve transaction: {exc}"
            ),
        }

    confirmed_round = info.get(
        "confirmed-round",
        0,
    )

    if not confirmed_round:
        return {
            "verified": False,
            "reason": (
                "Transaction is not confirmed "
                "or could not be found."
            ),
        }

    txn = info.get(
        "txn",
        {},
    )

    note_b64 = txn.get(
        "txn",
        {},
    ).get("note")

    if not note_b64:
        return {
            "verified": False,
            "reason": (
                "Confirmed transaction has "
                "no registry note."
            ),
        }

    note = decode_registry_note(
        note_b64
    )

    if note is None:
        return {
            "verified": False,
            "reason": (
                "Transaction does not contain "
                "a valid Lost & Found registry note."
            ),
        }

    return {
        "verified": True,
        "confirmed_round": confirmed_round,
        "record": note,
    }


def list_records(limit: int = 50):
    """Return Lost & Found records registered by this account."""

    if limit < 1 or limit > 1000:
        raise ValueError(
            "Limit must be between 1 and 1000."
        )

    sender = get_account_address()

    client = get_indexer_client()

    # We intentionally do not use note_prefix here.
    #
    # The registry note is JSON and starts with "{",
    # while "LFR1" appears inside the JSON as the
    # value of the "app" field.
    #
    # Therefore, we retrieve payment transactions
    # for this account and filter valid registry
    # records after decoding their notes.
    response = client.search_transactions_by_address(
        address=sender,
        limit=limit,
        txn_type="pay",
    )

    transactions = response.get(
        "transactions",
        [],
    )

    records = []

    for transaction in transactions:
        note_b64 = transaction.get(
            "note"
        )

        if not note_b64:
            continue

        record = decode_registry_note(
            note_b64
        )

        if record is None:
            continue

        records.append(
            {
                "txid": transaction.get(
                    "id"
                ),
                "confirmed_round": transaction.get(
                    "confirmed-round"
                ),
                "record": record,
            }
        )

    return records


def main():
    parser = argparse.ArgumentParser(
        description="Algorand Lost & Found Registry"
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    register = sub.add_parser(
        "register",
        help="Register a lost or found item",
    )

    register.add_argument(
        "--type",
        choices=["lost", "found"],
        required=True,
    )

    register.add_argument(
        "--item",
        required=True,
    )

    register.add_argument(
        "--description",
        required=True,
    )

    register.add_argument(
        "--location",
        required=True,
    )

    verify = sub.add_parser(
        "verify",
        help="Verify a transaction",
    )

    verify.add_argument(
        "--txid",
        required=True,
    )

    list_parser = sub.add_parser(
        "list",
        help="List registered Lost & Found records",
    )

    list_parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of records to display",
    )

    args = parser.parse_args()

    try:
        if args.command == "register":
            txid = register_item(
                args.type,
                args.item,
                args.description,
                args.location,
            )

            print(
                f"Registration successful.\n"
                f"Transaction ID: {txid}"
            )

        elif args.command == "verify":
            result = verify_transaction(
                args.txid
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                )
            )

        elif args.command == "list":
            records = list_records(
                args.limit
            )

            if not records:
                print(
                    "No Lost & Found records found."
                )
                return

            print(
                f"Found {len(records)} "
                f"Lost & Found record(s):\n"
            )

            print(
                json.dumps(
                    records,
                    indent=2,
                )
            )

    except ValueError as exc:
        parser.error(
            str(exc)
        )

    except RuntimeError as exc:
        parser.error(
            str(exc)
        )


if __name__ == "__main__":
    main()
