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


def test_unicode():
    left, right = socket.socketpair()
    payload = {"type": "message", "text": "yo 😭 नमस्ते"}

    left.sendall(pack_message(payload))
    assert read_message(right) == payload

    left.close()
    right.close()


def test_big_message_gets_rejected():
    payload = {"type": "message", "text": "x" * 70000}

    try:
        pack_message(payload)
    except ValueError:
        return

    raise AssertionError("big message was accepted")


if __name__ == "__main__":
    test_round_trip()
    test_unicode()
    test_big_message_gets_rejected()
    print("protocol tests passed")
