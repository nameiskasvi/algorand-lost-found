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


@app.route("/")
def index():
    """Display the Lost & Found dashboard."""

    try:
        records = list_records()
    except Exception as exc:
        records = []

        flash(
            f"Could not retrieve blockchain records: {exc}",
            "error",
        )

    return render_template(
        "index.html",
        records=records,
        search_query="",
        search_type="item",
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
        records = list_records()

        if not query:
            filtered_records = records

        elif search_type == "location":
            filtered_records = search_records_by_location(
                records,
                query,
            )

        else:
            filtered_records = search_records_by_item(
                records,
                query,
            )

        return render_template(
            "index.html",
            records=filtered_records,
            search_query=query,
            search_type=search_type,
        )

    except Exception as exc:
        flash(
            f"Search failed: {exc}",
            "error",
        )

        return render_template(
            "index.html",
            records=[],
            search_query=query,
            search_type=search_type,
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
