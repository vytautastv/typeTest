from curses import wrapper
from typing_test import TypingTest

def main(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the typing speed test")
    stdscr.addstr("\nPress any key to continue!")

    while True:
        typing_test = TypingTest(stdscr)
        stdscr.getkey()
        typing_test.test_wpm()
        stdscr.addstr(
            6,
            0,
            "Congratulations! You have completed the test! Press any key to continue...",
        )
        stdscr.nodelay(False)
        key = stdscr.getkey()

        # Check if the key is a single character before using ord()
        if isinstance(key, str) and len(key) == 1:
            if ord(key) == 27:  # ASCII value for ESC
                break

if __name__ == "__main__":
    wrapper(main)