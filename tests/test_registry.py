import base64
import json

import pytest

from src.registry import (
    PREFIX,
    build_note,
    decode_registry_note,
    filter_records_by_type,
    search_records_by_item,
    search_records_by_location,
    validate_item,
)


def test_build_note_contains_registry_fields():
    note = build_note(
        "lost",
        "Black Backpack",
        "Black backpack containing notebooks",
        "University Library",
    )

    payload = json.loads(
        note.decode("utf-8")
    )

    assert payload["v"] == 1
    assert payload["app"] == PREFIX
    assert payload["type"] == "lost"
    assert payload["item"] == "Black Backpack"
    assert (
        payload["description"]
        == "Black backpack containing notebooks"
    )
    assert (
        payload["location"]
        == "University Library"
    )
    assert "reported_at" in payload


def test_found_item_is_valid():
    validate_item(
        "found",
        "Mobile Phone",
        "Black smartphone found near the library",
        "University Library",
    )


def test_invalid_item_type_is_rejected():
    with pytest.raises(ValueError):
        validate_item(
            "unknown",
            "Backpack",
            "Black backpack",
            "Library",
        )


def test_empty_item_is_rejected():
    with pytest.raises(ValueError):
        validate_item(
            "lost",
            "",
            "Black backpack",
            "Library",
        )


def test_empty_description_is_rejected():
    with pytest.raises(ValueError):
        validate_item(
            "lost",
            "Backpack",
            "",
            "Library",
        )


def test_empty_location_is_rejected():
    with pytest.raises(ValueError):
        validate_item(
            "lost",
            "Backpack",
            "Black backpack",
            "",
        )


def test_whitespace_is_removed():
    note = build_note(
        "lost",
        "  Black Backpack  ",
        "  Black backpack  ",
        "  University Library  ",
    )

    payload = json.loads(
        note.decode("utf-8")
    )

    assert payload["item"] == "Black Backpack"
    assert payload["description"] == "Black backpack"
    assert payload["location"] == "University Library"


def test_decode_registry_note():
    note = build_note(
        "found",
        "Mobile Phone",
        "Black smartphone",
        "Library",
    )

    encoded = base64.b64encode(
        note
    ).decode("utf-8")

    payload = decode_registry_note(
        encoded
    )

    assert payload is not None
    assert payload["app"] == PREFIX
    assert payload["type"] == "found"
    assert payload["item"] == "Mobile Phone"


def test_decode_invalid_note_returns_none():
    encoded = base64.b64encode(
        b'{"app":"OTHER","item":"Test"}'
    ).decode("utf-8")

    assert (
        decode_registry_note(encoded)
        is None
    )


def sample_records():
    """Return sample records for testing filtering/search."""

    return [
        {
            "txid": "TXID-1",
            "confirmed_round": 100,
            "record": {
                "v": 1,
                "app": PREFIX,
                "type": "lost",
                "item": "Black Backpack",
                "description": "Backpack with notebooks",
                "location": "University Library",
            },
        },
        {
            "txid": "TXID-2",
            "confirmed_round": 101,
            "record": {
                "v": 1,
                "app": PREFIX,
                "type": "found",
                "item": "Mobile Phone",
                "description": "Black smartphone",
                "location": "University Library",
            },
        },
        {
            "txid": "TXID-3",
            "confirmed_round": 102,
            "record": {
                "v": 1,
                "app": PREFIX,
                "type": "lost",
                "item": "Blue Water Bottle",
                "description": "Steel bottle",
                "location": "Computer Lab",
            },
        },
    ]


def test_filter_records_by_type():
    records = sample_records()

    lost_records = filter_records_by_type(
        records,
        "lost",
    )

    assert len(lost_records) == 2
    assert (
        lost_records[0]["record"]["item"]
        == "Black Backpack"
    )
    assert (
        lost_records[1]["record"]["item"]
        == "Blue Water Bottle"
    )


def test_filter_found_records_by_type():
    records = sample_records()

    found_records = filter_records_by_type(
        records,
        "found",
    )

    assert len(found_records) == 1
    assert (
        found_records[0]["record"]["item"]
        == "Mobile Phone"
    )


def test_search_records_by_item():
    records = sample_records()

    results = search_records_by_item(
        records,
        "backpack",
    )

    assert len(results) == 1
    assert (
        results[0]["record"]["item"]
        == "Black Backpack"
    )


def test_search_records_by_item_is_case_insensitive():
    records = sample_records()

    results = search_records_by_item(
        records,
        "MOBILE",
    )

    assert len(results) == 1
    assert (
        results[0]["record"]["item"]
        == "Mobile Phone"
    )


def test_search_records_by_location():
    records = sample_records()

    results = search_records_by_location(
        records,
        "library",
    )

    assert len(results) == 2


def test_search_records_by_location_is_case_insensitive():
    records = sample_records()

    results = search_records_by_location(
        records,
        "COMPUTER LAB",
    )

    assert len(results) == 1
    assert (
        results[0]["record"]["item"]
        == "Blue Water Bottle"
    )


def test_empty_item_search_is_rejected():
    records = sample_records()

    with pytest.raises(ValueError):
        search_records_by_item(
            records,
            "",
        )


def test_empty_location_search_is_rejected():
    records = sample_records()

    with pytest.raises(ValueError):
        search_records_by_location(
            records,
            "",
        )


def test_invalid_filter_type_is_rejected():
    records = sample_records()

    with pytest.raises(ValueError):
        filter_records_by_type(
            records,
            "unknown",
        )
