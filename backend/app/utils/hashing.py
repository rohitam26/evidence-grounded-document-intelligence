import hashlib
from typing import Union

def compute_sha256(data: Union[bytes, str]) -> str:
    """Compute SHA-256 hash for byte content or string."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def compute_file_hash(file_path: str) -> str:
    """Compute SHA-256 hash of a file incrementally."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()
