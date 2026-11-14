#!/usr/bin/env python3
"""Flask app — routes only. Logic lives in wol.py / health.py / config.py."""
from flask import Flask, jsonify, render_template

import config
from health import is_up
from wol import fetch_mac_from_router, send_wol

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/init")
def api_init():
    macs = []
    try:
        macs = fetch_mac_from_router()
    except Exception:
        pass
    return jsonify({"macs": macs, "up": is_up()})


@app.route("/api/status")
def api_status():
    return jsonify({"up": is_up()})


@app.route("/api/wake", methods=["POST"])
def api_wake():
    mac = None
    try:
        macs = fetch_mac_from_router()
        if macs:
            mac = macs[0]
    except Exception:
        pass
    if not mac:
        mac = config.FALLBACK_MAC
    ok = send_wol(mac)
    return jsonify({"ok": ok, "mac": mac})


@app.route("/health")
def health_check():
    return jsonify({"ok": True}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.LISTEN_PORT)