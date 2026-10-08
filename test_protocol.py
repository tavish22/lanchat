import socket
import threading

from protocol import pack_message, read_message


def test_round_trip():
    left, right = socket.socketpair()
    payload = {"type": "message", "text": "hello"}

    def sender():
        left.sendall(pack_message(payload))
        left.close()

    thread = threading.Thread(target=sender)
    thread.start()

    assert read_message(right) == payload
    right.close()
    thread.join()


if __name__ == "__main__":
    test_round_trip()
    print("protocol test passed")
