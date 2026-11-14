"""
Wake-on-LAN: login to router, fetch MAC, send magic packet.

Router login flow (classic ASP router):
  1. GET  /Main_Login.asp        → get session cookie
  2. POST /Main_Login.asp        → submit credentials
  3. GET  /Main_WOL_Content.asp  → parse MACs
"""
import http.cookiejar
import re
import socket
import ssl
import urllib.parse
import urllib.request

import config

_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE

_cj = http.cookiejar.CookieJar()
_opener = urllib.request.build_opener(
    urllib.request.HTTPSHandler(context=_ctx),
    urllib.request.HTTPCookieProcessor(_cj),
)


def _get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "woken-up/1.0"})
    with _opener.open(req, timeout=5) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _login() -> None:
    """GET the login page (sets cookie), then POST credentials."""
    base = config.ROUTER_BASE.rstrip("/")

    # Step 1: GET the login page — server sets the session cookie here
    _get(f"{base}/Main_Login.asp")

    # Step 2: POST the credentials
    data = urllib.parse.urlencode({
        "username": config.ROUTER_USER,
        "password": config.ROUTER_PASS,
    }).encode()
    req = urllib.request.Request(
        f"{base}/Main_Login.asp",
        data=data,
        headers={"User-Agent": "woken-up/1.0"},
    )
    _opener.open(req, timeout=5).read()


def fetch_mac_from_router() -> list:
    """Login to router, fetch WOL page, return all MACs found."""
    try:
        _login()
    except Exception as e:
        print(f"[wol] login failed: {e}")

    url = f"{config.ROUTER_BASE.rstrip('/')}/Main_WOL_Content.asp"
    html = _get(url)

    macs = re.findall(r"([0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}", html)
    seen, out = set(), []
    for m in macs:
        norm = m.replace("-", ":").upper()
        if norm not in seen:
            seen.add(norm)
            out.append(norm)
    return out


def send_wol(mac: str) -> bool:
    """Send the 102-byte magic packet to the LAN broadcast."""
    mac_bytes = bytes.fromhex(mac.replace(":", "").replace("-", ""))
    packet = b"\xff" * 6 + mac_bytes * 16

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    try:
        sock.sendto(packet, (config.BROADCAST_IP, config.WOL_PORT))
        return True
    finally:
        sock.close()