from flask import jsonify

from . import health_check


@health_check.route("/health_check")
def health_check():
    return jsonify(ok=True)
