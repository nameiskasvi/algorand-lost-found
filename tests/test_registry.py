import json
from src.registry import build_note


def test_build_note_contains_registry_fields():
    note = json.loads(build_note("lost", "Black backpack", "Near library", "Library").decode())
    assert note["app"] == "LFR1"
    assert note["type"] == "lost"
    assert note["item"] == "Black backpack"
