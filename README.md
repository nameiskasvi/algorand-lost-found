# Algorand Lost & Found Registry

A blockchain-backed Lost & Found management system built using **Python, Flask, and the Algorand TestNet**.

The application allows users to register lost or found items, store their records on the Algorand blockchain, view previously registered records, search and filter records, and verify individual records using their Algorand transaction ID.

This project is intended for **academic, educational, and demonstration purposes**.

---

## Project Overview

Traditional Lost & Found systems commonly use forms, spreadsheets, or centralized databases.

Such systems may make it difficult to independently verify when a record was created or whether the original record has been modified.

This project uses the **Algorand blockchain** to create a verifiable record for each Lost & Found report.

When a user registers an item, the application creates a compact JSON record and stores it in the note field of an Algorand transaction.

Each registered record receives a unique **Algorand Transaction ID (TXID)**.

The TXID can later be used to retrieve and verify the record from the Algorand TestNet.

---

## Problem Statement

Campus Lost & Found records are often maintained using centralized systems such as spreadsheets, forms, or databases.

These systems can have limitations such as:

- Difficulty proving when a report was originally created.
- Centralized record management.
- Limited independent verification.
- Difficulty tracing the original record.
- Lack of a simple blockchain-based verification mechanism.

---

## Proposed Solution

The proposed system uses Algorand TestNet transactions as blockchain-backed Lost & Found records.

The basic workflow is:

```text
User
  |
  v
Enter Lost/Found Item
  |
  v
Input Validation
  |
  v
Create JSON Record
  |
  v
Create Algorand Transaction
  |
  v
Store Record in Transaction Note
  |
  v
Submit Transaction to Algorand TestNet
  |
  v
Transaction Confirmation
  |
  v
Transaction ID Returned
  |
  +-------------------------+
  |                         |
  v                         v
View/Search Records         Verify Transaction
  |                         |
  v                         v
Retrieve Blockchain         Retrieve Transaction
Record                       |
                             v
                       Decode Transaction Note
                             |
                             v
                       Verify Registry Record
```

---

## Key Features

### Blockchain Registration

Users can:

- Register lost items.
- Register found items.
- Store structured item information in an Algorand transaction note.
- Use Algorand TestNet for development and demonstration.
- Receive the confirmed transaction ID.

### Record Verification

Users can:

- Verify a record using its transaction ID.
- Retrieve the confirmed transaction.
- Decode the transaction note.
- Validate the Lost & Found Registry identifier.
- View the confirmed blockchain round.
- View the original record information.

### Transaction History

The application can:

- Retrieve previously registered records.
- Display transaction IDs.
- Display confirmed rounds.
- Decode stored Lost & Found registry information.

### Search and Filtering

Records can be:

- Viewed together.
- Filtered by Lost.
- Filtered by Found.
- Searched by item name.
- Searched by location.
- Searched case-insensitively.

### Interactive CLI

The project provides an interactive command-line menu containing:

```text
1. Register Lost Item
2. Register Found Item
3. View All Records
4. Verify Transaction
5. Search & Filter Records
6. Exit
```

### Web Dashboard

The Flask web interface provides:

- Dashboard statistics.
- Lost item registration.
- Found item registration.
- Record search.
- Record filtering.
- Blockchain record listing.
- Transaction verification.
- Algorand TestNet status indication.
- Transaction IDs and confirmed rounds.

### Input Validation

The application validates:

- Record type.
- Empty item names.
- Empty descriptions.
- Empty locations.
- Maximum item name length.
- Maximum description length.
- Maximum location length.
- Empty search queries.
- Invalid search and filter types.

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application |
| py-algorand-sdk | Algorand blockchain interaction |
| Algorand TestNet | Blockchain network |
| Algod API | Submit and retrieve transactions |
| Indexer API | Retrieve transaction history |
| python-dotenv | Environment configuration |
| pytest | Automated testing |
| HTML/CSS | Web interface |

---

# Project Structure

```text
algorand-lost-found/
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   └── registry.py
│
├── tests/
│   ├── test_registry.py
│   └── test_web.py
│
└── web/
    ├── app.py
    ├── static/
    │   └── style.css
    └── templates/
        ├── index.html
        └── verify.html
```

### Important Files

**`src/config.py`**

Contains the Algorand connection and environment configuration.

**`src/registry.py`**

Contains the main Lost & Found registry functionality, including:

- Input validation
- Blockchain registration
- Transaction verification
- Transaction history
- Searching
- Filtering
- Interactive CLI

**`web/app.py`**

Contains the Flask web application.

**`tests/`**

Contains automated tests for the registry and web application.

---

# Requirements

Before running the project, make sure you have:

- Python 3.10 or later
- Git
- An Algorand TestNet account
- TestNet ALGO for transaction fees

The project uses the **Algorand TestNet** for development and demonstration.

---

# Installation

## 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/nameiskasvi/algorand-lost-found.git
```

Move into the project directory:

```bash
cd algorand-lost-found
```

---

## 2. Create a Virtual Environment

A virtual environment is recommended so that the project's Python packages remain separate from other projects.

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### Linux, macOS, or WSL

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

## 3. Install Required Packages

Install all required dependencies using:

```bash
pip install -r requirements.txt
```

---

# Algorand TestNet Configuration

The application requires an Algorand TestNet account to submit transactions.

A configuration template is provided in:

```text
.env.example
```

Create your own `.env` file from this template.

### Linux, macOS, or WSL

```bash
cp .env.example .env
```

### Windows Command Prompt

```cmd
copy .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

---

# Configure the `.env` File

Open the newly created `.env` file.

The configuration should contain values similar to:

```env
ALGOD_ADDRESS=https://testnet-api.algonode.cloud
ALGOD_TOKEN=

INDEXER_ADDRESS=https://testnet-idx.algonode.cloud
INDEXER_TOKEN=

ACCOUNT_MNEMONIC=your_testnet_account_mnemonic
```

The variables are:

| Variable | Purpose |
|---|---|
| `ALGOD_ADDRESS` | Algorand TestNet Algod endpoint |
| `ALGOD_TOKEN` | Algod API token, if required |
| `INDEXER_ADDRESS` | Algorand TestNet Indexer endpoint |
| `INDEXER_TOKEN` | Indexer API token, if required |
| `ACCOUNT_MNEMONIC` | Mnemonic of the Algorand TestNet account used by the application |

The default TestNet endpoints are already provided in the project configuration.

---

# Security Warning

The `.env` file may contain sensitive account information.

**Never commit `.env` to GitHub.**

Do not publish:

- Account mnemonics.
- Private keys.
- Wallet seed phrases.
- Passwords.
- Secret API credentials.

The repository contains `.env.example` as a safe configuration template.

Only the template should be shared publicly.

For this project, use an **Algorand TestNet account**.

Do not use a production/MainNet account for testing.

---

# Running the Application

The project provides two ways to use the application:

1. Command-Line Interface (CLI)
2. Flask Web Dashboard

---

# Using the Command-Line Interface

From the project root, run:

```bash
python -m src.registry menu
```

The application will display an interactive menu:

```text
1. Register Lost Item
2. Register Found Item
3. View All Records
4. Verify Transaction
5. Search & Filter Records
6. Exit
```

Choose an option by entering its corresponding number.

---

## Register a Lost Item

Select:

```text
1
```

The application will ask for the item information.

For example:

```text
Item name: Black Backpack
Description: Black backpack containing notebooks
Location: University Library
```

The application validates the information and submits the record to the Algorand TestNet.

After successful confirmation, a transaction ID is returned.

Example:

```text
Transaction ID: <TRANSACTION_ID>
```

Save the transaction ID if you want to verify the record later.

---

## Register a Found Item

Select:

```text
2
```

For example:

```text
Item name: Red Umbrella
Description: Red umbrella found near the entrance
Location: University Main Gate
```

The application submits the record to the Algorand TestNet and returns the transaction ID.

---

## View All Records

Select:

```text
3
```

The application retrieves previously registered Lost & Found records.

The displayed information can include:

- Record type.
- Item name.
- Description.
- Location.
- Reported timestamp.
- Transaction ID.
- Confirmed blockchain round.

---

## Verify a Transaction

Select:

```text
4
```

Enter the transaction ID:

```text
Enter Transaction ID: <TRANSACTION_ID>
```

The application retrieves the transaction from the Algorand TestNet and checks whether it contains a valid Lost & Found Registry record.

The verification result includes information such as:

- Verification status.
- Transaction ID.
- Confirmed round.
- Original record information.

---

## Search and Filter Records

Select:

```text
5
```

The search and filtering functionality allows users to:

- View all records.
- View Lost records.
- View Found records.
- Search by item name.
- Search by location.

Searches are case-insensitive.

For example:

```text
Search by item: backpack
```

can find a record containing:

```text
Black Backpack
```

Similarly:

```text
Search by location: library
```

can find:

```text
University Library
```

---

# Direct CLI Commands

The application also supports direct command-line operations.

## Register a Lost Item

```bash
python -m src.registry register --type lost --item "Black Backpack" --description "Black backpack containing notebooks" --location "University Library"
```

## Register a Found Item

```bash
python -m src.registry register --type found --item "Red Umbrella" --description "Red umbrella found near the entrance" --location "University Main Gate"
```

## List Records

```bash
python -m src.registry list
```

To specify the number of records:

```bash
python -m src.registry list --limit 20
```

## Verify a Transaction

```bash
python -m src.registry verify --txid "<TRANSACTION_ID>"
```

Replace `<TRANSACTION_ID>` with the actual Algorand transaction ID.

## Open the Interactive Menu

```bash
python -m src.registry menu
```

---

# Running the Web Dashboard

The project also provides a Flask web interface.

From the project root, run:

```bash
python -m web.app
```

After the application starts, open a web browser and go to:

```text
http://127.0.0.1:5000
```

---

# Using the Web Dashboard

The web dashboard provides a graphical interface for the Lost & Found Registry.

## Dashboard

The main dashboard displays the registered records and statistics.

It can display:

- Total records.
- Lost records.
- Found records.
- Transaction IDs.
- Confirmed blockchain rounds.

---

## Register an Item

Use the registration form on the dashboard.

Enter:

- Item name.
- Description.
- Location.

Choose whether the item is:

```text
Lost
```

or:

```text
Found
```

Submit the form.

The application validates the information and creates an Algorand TestNet transaction.

---

## Search Records

The dashboard allows users to search records by:

- Item.
- Location.

Searches are case-insensitive.

---

## Filter Records

Records can be filtered by:

- Lost.
- Found.

---

## Verify a Transaction

Enter an Algorand transaction ID in the verification section.

The application retrieves the transaction from the Algorand TestNet and displays the verification result.

---

# Blockchain Record Format

Each Lost & Found record is stored as a JSON object in the Algorand transaction note field.

Example:

```json
{
  "v": 1,
  "app": "LFR1",
  "type": "lost",
  "item": "Black Backpack",
  "description": "Black backpack containing notebooks",
  "location": "University Library",
  "reported_at": "2026-09-17T13:58:08.589957+00:00"
}
```

### Fields

| Field | Description |
|---|---|
| `v` | Record format version |
| `app` | Lost & Found Registry identifier |
| `type` | `lost` or `found` |
| `item` | Name of the item |
| `description` | Description of the item |
| `location` | Location associated with the report |
| `reported_at` | UTC timestamp when the record was created |

Sensitive personal information should not be stored in the blockchain record.

---

# How Transaction Verification Works

When a transaction ID is provided, the application performs the following process:

```text
Transaction ID
      |
      v
Retrieve Transaction
      |
      v
Read Transaction Note
      |
      v
Decode JSON Record
      |
      v
Check Registry Identifier
      |
      v
Validate Record
      |
      v
Display Verification Result
```

This allows the application to verify whether the transaction contains a valid Lost & Found Registry record.

---

# Data Storage

The project does not use a traditional database for Lost & Found records.

Instead, each record is stored in an Algorand transaction note.

The Algorand Indexer is used to retrieve previously registered records.

Each registered blockchain record has a transaction ID that can be used to locate and verify the transaction.

---

# Running the Tests

The project contains automated tests for the registry functionality and Flask web application.

Run all tests with:

```bash
pytest -q
```

The tests cover functionality including:

- Input validation.
- Record creation.
- Record decoding.
- Record filtering.
- Item search.
- Location search.
- Transaction verification.
- Flask routes.
- Web registration.
- Web search.
- Web verification.
- Health endpoint.

A successful test run should show all tests passing.

---

# Troubleshooting

## `ACCOUNT_MNEMONIC` is not configured

Make sure the `.env` file exists in the project root.

Check that it contains:

```env
ACCOUNT_MNEMONIC=your_testnet_account_mnemonic
```

Make sure you are using an Algorand TestNet account.

---

## Transaction submission fails

Check the following:

1. The TestNet account is correctly configured.
2. The account has sufficient TestNet ALGO for transaction fees.
3. The Algorand TestNet endpoint is available.
4. The mnemonic belongs to the configured TestNet account.

---

## Records are not displayed

Check the following:

1. The `.env` file is configured correctly.
2. The application is using the account that registered the records.
3. The Indexer endpoint is available.
4. The transactions have been confirmed.

---

## Flask application does not start

First install the dependencies:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python -m web.app
```

---

## Tests fail because packages are missing

Run:

```bash
pip install -r requirements.txt
```

Then:

```bash
pytest -q
```

---

# Complete Quick Start

For a new user, the complete setup is:

```bash
git clone https://github.com/nameiskasvi/algorand-lost-found.git

cd algorand-lost-found

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
```

Configure the Algorand TestNet account in `.env`.

Then run the CLI:

```bash
python -m src.registry menu
```

Or run the web application:

```bash
python -m web.app
```

Then open:

```text
http://127.0.0.1:5000
```

---

# Project Status

The project currently provides:

- Algorand TestNet integration.
- Lost item registration.
- Found item registration.
- Blockchain transaction note storage.
- Transaction confirmation.
- Transaction verification.
- Transaction history.
- Record filtering.
- Item search.
- Location search.
- Input validation.
- Interactive CLI.
- Direct CLI commands.
- Flask web dashboard.
- Web registration.
- Web search.
- Web filtering.
- Web transaction verification.
- Automated tests.

---

# Repository

GitHub Repository:

https://github.com/nameiskasvi/algorand-lost-found

---

# Academic Purpose

This project was developed as an academic project to demonstrate the use of the **Algorand blockchain** for creating verifiable Lost & Found records.

The project demonstrates:

- Blockchain-based record storage.
- Algorand TestNet transactions.
- Transaction verification.
- Blockchain data retrieval.
- Python-based blockchain interaction.
- Flask web application development.
- Command-line application development.
- Automated software testing.

---

# License

This project is intended for academic, educational, and demonstration purposes.
