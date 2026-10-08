import os


def env_int(name, default):
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


CHAT_PORT = env_int("LANCHAT_PORT", 42691)
DISCOVERY_PORT = env_int("LANCHAT_DISCOVERY_PORT", 42690)
MAX_NAME = 24
MAX_MESSAGE = 2000
DISCOVERY_TIMEOUT = 1.5
