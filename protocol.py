import json
import struct

MAX_FRAME = 64 * 1024


def pack_message(payload):
    raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    if len(raw) > MAX_FRAME:
        raise ValueError("message is too big")
    return struct.pack("!I", len(raw)) + raw


def read_message(sock):
    header = _read_exact(sock, 4)
    if not header:
        return None

    size = struct.unpack("!I", header)[0]
    if size <= 0 or size > MAX_FRAME:
        raise ValueError("bad message size")

    body = _read_exact(sock, size)
    if not body:
        return None

    return json.loads(body.decode("utf-8"))


def _read_exact(sock, size):
    chunks = []
    while size:
        chunk = sock.recv(size)
        if not chunk:
            return b""
        chunks.append(chunk)
        size -= len(chunk)
    return b"".join(chunks)
