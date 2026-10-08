import socket
import sys
import threading

from config import CHAT_PORT
from discovery import find_server
from protocol import pack_message, read_message
from ui import banner, clear, connection_info, help_menu, message, system


def receiver(sock, state):
    while True:
        try:
            msg = read_message(sock)
        except (ConnectionError, OSError, ValueError):
            break

        if msg is None:
            break

        if msg.get("type") == "message":
            message(
                msg.get("name", "?"),
                msg.get("text", ""),
                own=msg.get("name") == state["name"],
            )
        elif msg.get("type") == "system":
            system(msg.get("text", ""))
        elif msg.get("type") == "users":
            system("online: " + ", ".join(msg.get("users", [])))

    system("connection closed")


def main():
    banner()

    host = sys.argv[1] if len(sys.argv) > 1 else None
    port = CHAT_PORT

    if host:
        print(f"connecting to {host}...")
    else:
        print("looking around for lanchat...")
        found = find_server()
        if not found:
            print("couldn't find a server")
            print("try: python client.py 192.168.x.x")
            return
        host, port = found
        print(f"found it at {host}:{port}")

    sock = socket.create_connection((host, port), timeout=5)
    sock.settimeout(None)

    hello = read_message(sock)
    state = {"name": hello.get("name", "guest")}

    connection_info(host, port)
    print(f"you are {state['name']}")
    print("type /help for commands\n")

    threading.Thread(
        target=receiver,
        args=(sock, state),
        daemon=True,
    ).start()

    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            text = "/quit"

        if not text:
            continue

        if text == "/quit":
            break

        if text == "/help":
            help_menu()
            continue

        if text == "/clear":
            clear()
            banner()
            connection_info(host, port)
            continue

        if text == "/who":
            sock.sendall(pack_message({"type": "users"}))
            continue

        if text.startswith("/name "):
            new_name = text[6:].strip()
            if new_name:
                sock.sendall(pack_message({"type": "name", "name": new_name}))
            continue

        sock.sendall(pack_message({
            "type": "message",
            "text": text,
        }))

    try:
        sock.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    sock.close()


if __name__ == "__main__":
    main()
