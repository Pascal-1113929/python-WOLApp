"""All personal values come from environment variables. No defaults leak."""
import os

ROUTER_URL   = os.environ["ROUTER_URL"]       # e.g. https://192.168.50.1:8443/Main_WOL_Content.asp
TARGET_IP    = os.environ["TARGET_IP"]        # e.g. 192.168.50.14
FALLBACK_MAC = os.environ["FALLBACK_MAC"]     # e.g. 34:5A:60:4C:2D:86
BROADCAST_IP = os.environ["BROADCAST_IP"]     # e.g. 192.168.50.255
WOL_PORT     = int(os.environ.get("WOL_PORT", "9"))
LISTEN_PORT  = int(os.environ.get("LISTEN_PORT", "8080"))