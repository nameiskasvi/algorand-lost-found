from unittest.mock import patch

from web.app import app


SAMPLE_RECORDS = [
    {
        "txid": "TESTTXID001",
        "confirmed_round": 100,
        "record": {
            "v": 1,
            "app": "LFR1",
            "type": "lost",
            "item": "Black Backpack",
            "description": "Black backpack containing notebooks",
            "location": "University Library",
            "reported_at": "2026-09-17T10:00:00+00:00",
        },
    },
    {
        "txid": "TESTTXID002",
        "confirmed_round": 101,
        "record": {
            "v": 1,
            "app": "LFR1",
            "type": "found",
            "item": "Blue Water Bottle",
            "description": "Blue steel water bottle",
            "location": "Computer Lab",
            "reported_at": "2026-09-17T11:00:00+00:00",
        },
    },
    {
        "txid": "TESTTXID003",
        "confirmed_round": 102,
        "record": {
            "v": 1,
            "app": "LFR1",
            "type": "lost",
            "item": "Laptop Bag",
            "description": "Black laptop bag",
            "location": "Computer Lab",
            "reported_at": "2026-09-17T12:00:00+00:00",
        },
    },
]


def setup_function():
    """Configure Flask testing mode before each test."""

    app.config["TESTING"] = True


def test_dashboard_loads_successfully():
    with patch(
        "web.app.list_records",
        return_value=SAMPLE_RECORDS,
    ):

        client = app.test_client()

        response = client.get("/")

        assert response.status_code == 200

        page = response.get_data(
            as_text=True
        )

        assert "Lost &amp; Found Registry" in page
        assert "Black Backpack" in page
        assert "Blue Water Bottle" in page


def test_dashboard_statistics_are_displayed():
    with patch(
        "web.app.list_records",
        return_value=SAMPLE_RECORDS,
    ):

        client = app.test_client()

        response = client.get("/")

        page = response.get_data(
            as_text=True
        )

        assert "TOTAL RECORDS" in page
        assert "LOST ITEMS" in page
        assert "FOUND ITEMS" in page

        assert "3" in page
        assert "2" in page
        assert "1" in page


def test_health_endpoint():
    client = app.test_client()

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"

    assert (
        data["application"]
        == "Algorand Lost & Found Registry"
    )


def test_search_by_item():
    with patch(
        "web.app.list_records",
        return_value=SAMPLE_RECORDS,
    ):

        client = app.test_client()

        response = client.get(
            "/search?type=item&q=backpack"
        )

        assert response.status_code == 200

        page = response.get_data(
            as_text=True
        )

        assert "Black Backpack" in page
        assert "<h3>Blue Water Bottle</h3>" not in page


def test_search_by_location():
    with patch(
        "web.app.list_records",
        return_value=SAMPLE_RECORDS,
    ):

        client = app.test_client()

        response = client.get(
            "/search?type=location&q=computer%20lab"
        )

        assert response.status_code == 200

        page = response.get_data(
            as_text=True
        )

        assert "Blue Water Bottle" in page
        assert "Laptop Bag" in page

        # Check the actual record heading rather than
        # searching the entire HTML page. The registration
        # form contains "Black Backpack" as a placeholder.
        assert "<h3>Black Backpack</h3>" not in page


def test_empty_search_returns_all_records():
    with patch(
        "web.app.list_records",
        return_value=SAMPLE_RECORDS,
    ):

        client = app.test_client()

        response = client.get(
            "/search?type=item&q="
        )

        assert response.status_code == 200

        page = response.get_data(
            as_text=True
        )

        assert "Black Backpack" in page
        assert "Blue Water Bottle" in page
        assert "Laptop Bag" in page


def test_successful_registration():
    with patch(
        "web.app.register_item",
        return_value="NEWTXID123",
    ):

        client = app.test_client()

        response = client.post(
            "/register",
            data={
                "item_type": "found",
                "item": "Red Umbrella",
                "description": "Red umbrella found near entrance",
                "location": "Main Entrance",
            },
            follow_redirects=False,
        )

        assert response.status_code == 302

        assert response.headers["Location"].endswith(
            "/"
        )


def test_registration_validation_error():
    with patch(
        "web.app.register_item",
        side_effect=ValueError(
            "Item name cannot be empty."
        ),
    ):

        client = app.test_client()

        response = client.post(
            "/register",
            data={
                "item_type": "lost",
                "item": "",
                "description": "Test description",
                "location": "Library",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200

        page = response.get_data(
            as_text=True
        )

        assert (
            "Validation error: Item name cannot be empty."
            in page
        )


def test_verification_page_for_valid_transaction():
    verification_result = {
        "verified": True,
        "confirmed_round": 200,
        "record": {
            "v": 1,
            "app": "LFR1",
            "type": "found",
            "item": "Blue Water Bottle",
            "description": "Blue steel water bottle",
            "location": "Computer Lab",
            "reported_at": "2026-09-17T11:00:00+00:00",
        },
    }

    with patch(
        "web.app.verify_transaction",
        return_value=verification_result,
    ):

        client = app.test_client()

        response = client.get(
            "/verify?txid=TESTTXID002"
        )

        assert response.status_code == 200

        page = response.get_data(
            as_text=True
        )

        assert (
            "Blockchain Record Verified"
            in page
        )

        assert "Blue Water Bottle" in page
        assert "Computer Lab" in page
        assert "LFR1" in page


def test_verification_page_for_invalid_transaction():
    verification_result = {
        "verified": False,
        "reason": (
            "Could not retrieve transaction: "
            "Transaction not found."
        ),
    }

    with patch(
        "web.app.verify_transaction",
        return_value=verification_result,
    ):

        client = app.test_client()

        response = client.get(
            "/verify?txid=INVALID_TRANSACTION_ID"
        )

        assert response.status_code == 200

        page = response.get_data(
            as_text=True
        )

        assert (
            "Blockchain Record Could Not Be Verified"
            in page
        )

        assert (
            "Transaction not found."
            in page
        )
