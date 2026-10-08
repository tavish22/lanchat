import os
from datetime import datetime


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def stamp():
    return datetime.now().strftime("%H:%M")


def banner():
    print("\033[96m")
    print("  lanchat")
    print("  local chat. no cloud. no nonsense.")
    print("\033[0m")


def system(text):
    print(f"\033[90m[{stamp()}] * {text}\033[0m")


def message(name, text, own=False):
    color = "\033[92m" if own else "\033[96m"
    print(f"{color}[{stamp()}] {name}: {text}\033[0m")


def action(text):
    print(f"\033[95m[{stamp()}] {text}\033[0m")


def help_menu():
    print()
    print("\033[96mcommands\033[0m")
    print("  /name <name>  change your name")
    print("  /who           show online people")
    print("  /me <text>     send an action")
    print("  /clear         clear the terminal")
    print("  /help          show this")
    print("  /quit          leave")
    print()


def connection_info(host, port):
    system(f"connected to {host}:{port}")
