import webbrowser
import os

from extra.tools.clean_console_command_setter import set_cleaning_command


def open_git_repo_in_browser():
    webbrowser.open("https://github.com/GonnaFlyMethod/snake1976")
    clean = set_cleaning_command()
    os.system(clean)
