"""All personal values from env vars. Nothing leaks."""
import os

# Router — login + WOL page
ROUTER_BASE  = os.environ["ROUTER_BASE"]
ROUTER_USER  = os.environ["ROUTER_USER"]
ROUTER_PASS  = os.environ["ROUTER_PASS"]

# Target PC
TARGET_IP    = os.environ["TARGET_IP"]
FALLBACK_MAC = os.environ["FALLBACK_MAC"]

# Network
BROADCAST_IP = os.environ["BROADCAST_IP"]
WOL_PORT     = int(os.environ.get("WOL_PORT", "9"))
LISTEN_PORT  = int(os.environ.get("LISTEN_PORT", "8080"))