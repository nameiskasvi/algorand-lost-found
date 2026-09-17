import json

import pytest

from src.registry import (
    PREFIX,
    build_note,
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
