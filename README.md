# Algorand Lost & Found Registry

A blockchain-backed Lost & Found management system built using Python, Flask, and the Algorand TestNet.

The application allows users to register lost or found items, retrieve blockchain-backed records, search and filter records, and verify individual records using their Algorand transaction ID.

---

## 1. Project Overview

Traditional Lost & Found systems commonly use spreadsheets, forms, or centralized databases. Such systems may make it difficult to independently verify when a record was created or whether the original record has been modified.

This project uses the Algorand blockchain to create a verifiable record for each Lost & Found report.

Instead of storing sensitive personal information on-chain, the application stores a compact JSON record inside an Algorand transaction note.

Each registered record receives a unique blockchain transaction ID (TXID), which can later be used to verify the record.

---

## 2. Problem Statement

Campus Lost & Found records are often maintained using centralized systems such as spreadsheets or web forms.

These systems can have limitations including:

- Difficulty proving when a report was originally created.
- Centralized record management.
- Limited independent verification.
- Difficulty tracing the original blockchain-backed record.
- Lack of a simple public verification mechanism.

---

## 3. Proposed Solution

The proposed system uses Algorand TestNet transactions as tamper-evident records.

The workflow is:

1. A user submits a Lost or Found item.
2. The application validates the input.
3. The item information is converted into a JSON record.
4. The JSON record is stored in the Algorand transaction note field.
5. A 0-ALGO self-transfer transaction is submitted.
6. Algorand confirms the transaction.
7. The transaction ID is returned to the user.
8. The transaction can later be retrieved and verified.
9. The web dashboard provides searching, filtering, and verification.

---

## 4. Key Features

### Blockchain Registration

- Register lost items.
- Register found items.
- Store structured item information in an Algorand transaction note.
- Use Algorand TestNet for development and demonstration.
- Return the confirmed transaction ID.

### Record Verification

- Verify a record using its transaction ID.
- Retrieve the confirmed transaction.
- Decode the transaction note.
- Validate the Lost & Found registry identifier.
- Display the confirmed blockchain round.
- Display the original record information.

### Transaction History

- Retrieve previously registered records.
- Display transaction IDs.
- Display confirmed rounds.
- Decode stored registry information.

### Search & Filtering

Records can be:

- Viewed together.
- Filtered by `Lost`.
- Filtered by `Found`.
- Searched by item name.
- Searched by location.
- Searched case-insensitively.

### Interactive CLI

The project provides an interactive command-line menu with:

1. Register Lost Item
2. Register Found Item
3. View All Records
4. Verify Transaction
5. Search & Filter Records
6. Exit

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
- Invalid search/filter types.

---

## 5. Blockchain Record Format

Each transaction contains a JSON object in the Algorand transaction note field.

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
