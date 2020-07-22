import sys
import termios


fd = sys.stdin.fileno()

new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)
new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)


def set_normal_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)


def set_curses_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)
