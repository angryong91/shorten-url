import hashlib
import base62

from uuid import uuid4


def shorten_url(url: str) -> str:
    md5_hash = hashlib.md5(f"{url}{uuid4()}".encode()).hexdigest()
    return base62.encode(int(md5_hash, 16))
