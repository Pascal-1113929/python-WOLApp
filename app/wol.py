"""Wake-on-LAN logic: fetch MAC from router, send magic packet."""
import re
import socket
import ssl
import urllib.request

import config


def fetch_mac_from_router(url: str | None = None) -> list:
    """GET the router WOL page and return every MAC it contains."""
    url = url or config.ROUTER_URL
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url, headers={"User-Agent": "woken-up/1.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    macs = re.findall(r"([0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}", html)
    seen, out = set(), []
    for m in macs:
        norm = m.replace("-", ":").upper()
        if norm not in seen:
            seen.add(norm)
            out.append(norm)
    return out


def send_wol(mac: str) -> bool:
    """Send the 102-byte magic packet to the LAN broadcast address."""
    mac_bytes = bytes.fromhex(mac.replace(":", "").replace("-", ""))
    packet = b"\xff" * 6 + mac_bytes * 16

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    try:
        sock.sendto(packet, (config.BROADCAST_IP, config.WOL_PORT))
        return True
    finally:
        sock.close()