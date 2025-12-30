import hashlib


def make_content_hash(work_content: str) -> str:
    return hashlib.sha256(work_content.encode("utf-8")).hexdigest()
