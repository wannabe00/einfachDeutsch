"""Two-factor codes from an authenticator app (TOTP, RFC 6238: HMAC-SHA1,
6 digits, 30-second steps), plus one-time backup codes. Standard library only."""

import base64
import hashlib
import hmac
import secrets
import struct
import time
from urllib.parse import quote

STEP = 30
DIGITS = 6
ISSUER = "einfachDeutsch"


def new_secret() -> str:
    return base64.b32encode(secrets.token_bytes(20)).decode()


def code_at(secret: str, step: int, digits: int = DIGITS) -> str:
    key = base64.b32decode(secret)
    digest = hmac.new(key, struct.pack(">Q", step), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    number = struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF
    return str(number % 10**digits).zfill(digits)


def matching_step(secret: str, code: str, now: float | None = None) -> int | None:
    """The time step the code belongs to (this one or a neighbour, for clock
    drift), or None if it's wrong."""
    code = "".join(code.split())
    if not (code.isdigit() and len(code) == DIGITS):
        return None
    current = int((time.time() if now is None else now) // STEP)
    for step in (current, current - 1, current + 1):
        if hmac.compare_digest(code_at(secret, step), code):
            return step
    return None


def setup_uri(secret: str, account: str) -> str:
    """What the QR code holds; authenticator apps read it."""
    label = quote(f"{ISSUER}:{account}")
    return f"otpauth://totp/{label}?secret={secret}&issuer={ISSUER}&digits={DIGITS}&period={STEP}"


def new_backup_codes(n: int = 8) -> list[str]:
    return [f"{secrets.token_hex(2)}-{secrets.token_hex(2)}" for _ in range(n)]


def hash_backup(code: str) -> str:
    return hashlib.sha256(code.strip().lower().encode()).hexdigest()
