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
