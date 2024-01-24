import hashlib
from uuid import uuid4

import base62


def shorten_url(url: str) -> str:
    md5_hash = hashlib.md5(f"{url}{uuid4()}".encode()).hexdigest()
    return base62.encode(int(md5_hash, 16))
