# Algorand Lost & Found Registry

A simple blockchain-based Lost & Found registry built on the Algorand TestNet.

## Problem
Campus lost-and-found records are usually maintained in centralized forms or spreadsheets. Records can be changed or deleted, making it difficult to prove when an item was reported.

## Proposed Solution
This project records a compact lost/found item report in an Algorand transaction's note field. The blockchain transaction provides a tamper-evident timestamp and transaction ID that can be used to verify the report.

## MVP Features
- Register a lost/found item on Algorand TestNet.
- Store item metadata as a JSON note in a blockchain transaction.
- Return the transaction ID after successful confirmation.
- Verify a previously submitted record using its transaction ID.
- Keep private contact information off-chain; only a safe public description is stored.

## Technology Stack
- Python 3.10+
- `algosdk` (Algorand Python SDK)
- Algorand TestNet
- Algod API

## Project Structure

```text
algorand-lost-found/
├── src/
│   ├── config.py
│   └── registry.py
├── tests/
│   └── test_registry.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add a funded Algorand TestNet account mnemonic.
4. Run the CLI:

```bash
python -m src.registry register --type lost --item "Black backpack" --description "Black backpack found near library" --location "Campus Library"
```

The program will submit a 0-ALGO self-transaction with the item report in the note field and print the transaction ID.

To verify a transaction:

```bash
python -m src.registry verify --txid YOUR_TRANSACTION_ID
```

## Important Security Note
Never commit `.env` or a real mnemonic/private key to GitHub. Use a dedicated TestNet account only.

## Future Scope
- Web dashboard for students and administrators.
- Algorand smart contract for structured registry records.
- Search/filter using an indexer.
- Optional cryptographic proof for handover of an item.
- Role-based verification for campus administrators.

## First Milestone
The first implementation milestone is a working TestNet transaction that stores and verifies a lost/found item record.
