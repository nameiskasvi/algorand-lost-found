from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from src.registry import (
    list_records,
    register_item,
    search_records_by_item,
    search_records_by_location,
    verify_transaction,
)


app = Flask(__name__)

# Development-only secret key.
# Replace with a secure random value before production deployment.
app.secret_key = "algorand-lost-found-development-key"


def calculate_statistics(records):
    """Calculate dashboard statistics from registry records."""

    total_records = len(records)

    lost_count = sum(
        1
        for entry in records
        if entry.get("record", {}).get("type") == "lost"
    )

    found_count = sum(
        1
        for entry in records
        if entry.get("record", {}).get("type") == "found"
    )

    return {
        "total_records": total_records,
        "lost_count": lost_count,
        "found_count": found_count,
    }


def render_dashboard(
    records,
    search_query="",
    search_type="item",
    all_records=None,
):
    """Render the dashboard with records and statistics."""

    if all_records is None:
        all_records = records

    statistics = calculate_statistics(
        all_records
    )

    return render_template(
        "index.html",
        records=records,
        search_query=search_query,
        search_type=search_type,
        total_records=statistics["total_records"],
        lost_count=statistics["lost_count"],
        found_count=statistics["found_count"],
    )


@app.route("/")
def index():
    """Display the Lost & Found dashboard."""

    try:
        records = list_records()

        return render_dashboard(
            records
        )

    except Exception as exc:
        flash(
            f"Could not retrieve blockchain records: {exc}",
            "error",
        )

        return render_dashboard(
            [],
            all_records=[],
        )


@app.route("/register", methods=["POST"])
def register():
    """Register a new lost/found item."""

    item_type = request.form.get(
        "item_type",
        "",
    ).strip()

    item = request.form.get(
        "item",
        "",
    ).strip()

    description = request.form.get(
        "description",
        "",
    ).strip()

    location = request.form.get(
        "location",
        "",
    ).strip()

    try:
        txid = register_item(
            item_type,
            item,
            description,
            location,
        )

        flash(
            f"Registration successful! Transaction ID: {txid}",
            "success",
        )

    except ValueError as exc:
        flash(
            f"Validation error: {exc}",
            "error",
        )

    except RuntimeError as exc:
        flash(
            f"Configuration error: {exc}",
            "error",
        )

    except Exception as exc:
        flash(
            f"Registration failed: {exc}",
            "error",
        )

    return redirect(
        url_for("index")
    )


@app.route("/search")
def search():
    """Search records by item or location."""

    search_type = request.args.get(
        "type",
        "item",
    ).strip()

    query = request.args.get(
        "q",
        "",
    ).strip()

    try:
        all_records = list_records()

        if not query:
            filtered_records = all_records

        elif search_type == "location":
            filtered_records = search_records_by_location(
                all_records,
                query,
            )

        else:
            filtered_records = search_records_by_item(
                all_records,
                query,
            )

        return render_dashboard(
            filtered_records,
            search_query=query,
            search_type=search_type,
            all_records=all_records,
        )

    except Exception as exc:
        flash(
            f"Search failed: {exc}",
            "error",
        )

        return render_dashboard(
            [],
            search_query=query,
            search_type=search_type,
            all_records=[],
        )


@app.route("/verify", methods=["GET", "POST"])
def verify():
    """Verify a Lost & Found transaction on Algorand."""

    if request.method == "POST":
        txid = request.form.get(
            "txid",
            "",
        ).strip()

    else:
        txid = request.args.get(
            "txid",
            "",
        ).strip()

    result = verify_transaction(
        txid
    )

    return render_template(
        "verify.html",
        result=result,
        txid=txid,
    )


@app.route("/health")
def health():
    """Simple application health check."""

    return {
        "status": "ok",
        "application": "Algorand Lost & Found Registry",
    }


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
