"""Ping the target to check if it's awake."""
import subprocess

import config


def is_up(ip: str | None = None) -> bool:
    ip = ip or config.TARGET_IP
    try:
        r = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=3,
        )
        return r.returncode == 0
    except Exception:
        return False