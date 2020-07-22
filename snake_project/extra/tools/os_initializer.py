import platform


def init_os() -> str:
    os = platform.system()
    return os
