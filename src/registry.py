import argparse
import base64
import json
from datetime import datetime, timezone

from algosdk import account, mnemonic
from algosdk.transaction import PaymentTxn, wait_for_confirmation

from .config import ACCOUNT_MNEMONIC, get_algod_client

PREFIX = "LFR1"


def build_note(item_type: str, item: str, description: str, location: str) -> bytes:
    payload = {
        "v": 1,
        "app": PREFIX,
        "type": item_type,
        "item": item,
        "description": description,
        "location": location,
        "reported_at": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(payload, separators=(",", ":")).encode("utf-8")


def register_item(item_type: str, item: str, description: str, location: str) -> str:
    if not ACCOUNT_MNEMONIC:
        raise RuntimeError("ACCOUNT_MNEMONIC is not configured. Copy .env.example to .env and add a TestNet mnemonic.")

    private_key = mnemonic.to_private_key(ACCOUNT_MNEMONIC)
    sender = account.address_from_private_key(private_key)
    client = get_algod_client()

    params = client.suggested_params()
    note = build_note(item_type, item, description, location)

    # A self-transfer is used for the MVP so no second account is required.
    txn = PaymentTxn(
        sender=sender,
        sp=params,
        receiver=sender,
        amt=0,
        note=note,
    )
    signed = txn.sign(private_key)
    txid = client.send_transaction(signed)
    wait_for_confirmation(client, txid, 4)
    return txid


def verify_transaction(txid: str):
    client = get_algod_client()
    info = client.pending_transaction_info(txid)
    confirmed_round = info.get("confirmed-round", 0)
    if not confirmed_round:
        return {"verified": False, "reason": "Transaction is not confirmed or could not be found."}

    txn = info.get("txn", {})
    note_b64 = txn.get("txn", {}).get("note")
    if not note_b64:
        return {"verified": False, "reason": "Confirmed transaction has no registry note."}

    note = json.loads(base64.b64decode(note_b64).decode("utf-8"))
    return {"verified": note.get("app") == PREFIX, "confirmed_round": confirmed_round, "record": note}


def main():
    parser = argparse.ArgumentParser(description="Algorand Lost & Found Registry")
    sub = parser.add_subparsers(dest="command", required=True)

    register = sub.add_parser("register")
    register.add_argument("--type", choices=["lost", "found"], required=True)
    register.add_argument("--item", required=True)
    register.add_argument("--description", required=True)
    register.add_argument("--location", required=True)

    verify = sub.add_parser("verify")
    verify.add_argument("--txid", required=True)

    args = parser.parse_args()
    if args.command == "register":
        print(register_item(args.type, args.item, args.description, args.location))
    else:
        print(json.dumps(verify_transaction(args.txid), indent=2))


if __name__ == "__main__":
    main()
