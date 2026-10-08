import socket
import threading

from config import CHAT_PORT, MAX_MESSAGE, MAX_NAME
from discovery import listen_for_discovery
from protocol import pack_message, read_message

HOST = "0.0.0.0"
PORT = CHAT_PORT


class ChatServer:
    def __init__(self):
        self.clients = {}
        self.lock = threading.Lock()
        self.next_id = 1

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(20)

        stop = threading.Event()
        threading.Thread(
            target=listen_for_discovery,
            args=(HOST, PORT, stop),
            daemon=True,
        ).start()

        print(f"lanchat server running on port {PORT}")
        print("waiting for people...")

        try:
            while True:
                client, address = sock.accept()
                with self.lock:
                    user_id = self.next_id
                    self.next_id += 1

                threading.Thread(
                    target=self.handle_client,
                    args=(client, address, user_id),
                    daemon=True,
                ).start()
        except KeyboardInterrupt:
            print("\nstopping...")
        finally:
            stop.set()
            sock.close()

    def handle_client(self, sock, address, user_id):
        name = f"guest{user_id}"
        try:
            sock.sendall(pack_message({
                "type": "hello",
                "name": name,
                "users": self.user_list(),
            }))

            with self.lock:
                self.clients[sock] = {"name": name, "address": address}

            self.broadcast({
                "type": "system",
                "text": f"{name} joined",
            }, skip=sock)

            while True:
                msg = read_message(sock)
                if msg is None:
                    break

                kind = msg.get("type")

                if kind == "name":
                    new_name = str(msg.get("name", "")).strip()[:MAX_NAME]
                    if not new_name:
                        continue

                    with self.lock:
                        taken = any(
                            info["name"].lower() == new_name.lower()
                            and client is not sock
                            for client, info in self.clients.items()
                        )

                    if taken:
                        sock.sendall(pack_message({
                            "type": "system",
                            "text": "that name is already taken",
                        }))
                        continue

                    old_name = name
                    name = new_name

                    with self.lock:
                        self.clients[sock]["name"] = name

                    self.broadcast({
                        "type": "system",
                        "text": f"{old_name} is now {name}",
                    })
                    continue

                if kind == "users":
                    sock.sendall(pack_message({
                        "type": "users",
                        "users": self.user_list(),
                    }))
                    continue

                if kind == "message":
                    text = str(msg.get("text", "")).strip()
                    if text:
                        self.broadcast({
                            "type": "message",
                            "name": name,
                            "text": text[:MAX_MESSAGE],
                        })

        except (ConnectionError, OSError, ValueError):
            pass
        finally:
            with self.lock:
                self.clients.pop(sock, None)
            try:
                sock.close()
            except OSError:
                pass
            self.broadcast({
                "type": "system",
                "text": f"{name} left",
            })

    def user_list(self):
        with self.lock:
            return [info["name"] for info in self.clients.values()]

    def broadcast(self, payload, skip=None):
        packet = pack_message(payload)
        dead = []

        with self.lock:
            clients = list(self.clients)

        for client in clients:
            if client is skip:
                continue
            try:
                client.sendall(packet)
            except OSError:
                dead.append(client)

        if dead:
            with self.lock:
                for client in dead:
                    self.clients.pop(client, None)


if __name__ == "__main__":
    ChatServer().start()
