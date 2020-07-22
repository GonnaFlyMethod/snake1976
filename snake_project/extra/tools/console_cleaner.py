import os

from .os_initializer import init_os


def set_the_console_cleaning_command():
    if init_os() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
