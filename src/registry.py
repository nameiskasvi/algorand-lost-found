import argparse
import base64
import json
from datetime import datetime, timezone

from algosdk import account, mnemonic
from algosdk.transaction import PaymentTxn, wait_for_confirmation

from .config import ACCOUNT_MNEMONIC, get_algod_client


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
            f"Item name cannot exceed {MAX_ITEM_LENGTH} characters."
        )

    if len(description.strip()) > MAX_DESCRIPTION_LENGTH:
        raise ValueError(
            f"Description cannot exceed "
            f"{MAX_DESCRIPTION_LENGTH} characters."
        )

    if len(location.strip()) > MAX_LOCATION_LENGTH:
        raise ValueError(
            f"Location cannot exceed {MAX_LOCATION_LENGTH} characters."
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

    if not ACCOUNT_MNEMONIC:
        raise RuntimeError(
            "ACCOUNT_MNEMONIC is not configured. "
            "Copy .env.example to .env and add a TestNet mnemonic."
        )

    private_key = mnemonic.to_private_key(
        ACCOUNT_MNEMONIC
    )

    sender = account.address_from_private_key(
        private_key
    )

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
    signed = txn.sign(private_key)

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
            "reason": f"Could not retrieve transaction: {exc}",
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
        return {
            "verified": False,
            "reason": (
                "Registry note could not "
                "be decoded as JSON."
            ),
        }

    return {
        "verified": note.get("app") == PREFIX,
        "confirmed_round": confirmed_round,
        "record": note,
    }


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

    except ValueError as exc:
        parser.error(str(exc))

    except RuntimeError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
