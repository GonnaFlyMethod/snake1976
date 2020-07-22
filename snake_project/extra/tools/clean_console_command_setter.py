from .os_initializer import init_os


def set_cleaning_command():
    command = None
    if init_os() == "Windows":
        command = "cls"
    else:
        command = "clear"
    return command
