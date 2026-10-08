import socket

DISCOVERY_PORT = 42690
DISCOVERY_MESSAGE = b"lanchat?\n"
REPLY_PREFIX = b"lanchat!"


def find_server(timeout=1.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)

    try:
        sock.sendto(DISCOVERY_MESSAGE, ("255.255.255.255", DISCOVERY_PORT))

        while True:
            data, address = sock.recvfrom(1024)
            if data.startswith(REPLY_PREFIX):
                port = int(data[len(REPLY_PREFIX):].split(b":", 1)[0])
                return address[0], port
    except (TimeoutError, socket.timeout):
        return None
    finally:
        sock.close()


def listen_for_discovery(host, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, DISCOVERY_PORT))
    sock.settimeout(0.5)

    try:
        while not stop_event.is_set():
            try:
                data, address = sock.recvfrom(1024)
            except socket.timeout:
                continue

            if data.strip() == DISCOVERY_MESSAGE.strip():
                reply = REPLY_PREFIX + f"{port}:ok".encode()
                sock.sendto(reply, address)
    finally:
        sock.close()
