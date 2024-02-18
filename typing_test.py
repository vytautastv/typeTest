import curses
import random
import time

class TypingTest:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.to_type_text = self.get_line_to_type()
        self.user_typed_text = []
        self.wpm = 0
        self.start_time = time.time()

        # Initialize color pairs
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    def get_line_to_type(self):
        try:
            with open("typing_texts.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
            return random.choice(lines).strip()
        except FileNotFoundError:
            return "Error: typing_texts.txt not found!"

    def display_wpm(self):
        self.stdscr.addstr(1, 0, f"WPM: {self.wpm}", curses.color_pair(3))

    def display_accuracy(self):
        self.stdscr.addstr(
            2,
            0,
            f"Accuracy: {self.test_accuracy()}%",
            curses.color_pair(3),
        )

    def display_typed_chars(self):
        for i, char in enumerate(self.user_typed_text):
            correct_character = self.to_type_text[i] if i < len(self.to_type_text) else ' '
            # Use color pair 1 if correct, else color pair 2.
            color = 1 if char == correct_character else 2
            self.stdscr.addstr(0, i, char, curses.color_pair(color))

    def display_details(self):
        self.stdscr.addstr(3, 0, "Type the following text:")
        self.stdscr.addstr(4, 0, self.to_type_text)
        self.display_wpm()
        self.display_accuracy()
        self.display_typed_chars()

    def test_accuracy(self):
        total_characters = min(len(self.user_typed_text), len(self.to_type_text))

        # If there are no typed chars, show accuracy 0.
        if total_characters == 0:
            return 0.0

        matching_characters = sum(1 for current_char, target_char in zip(self.user_typed_text, self.to_type_text[:total_characters]) if current_char == target_char)
        matching_percentage = (matching_characters / total_characters) * 100
        return round(matching_percentage, 2)

    def test_wpm(self):
        # getkey method by default is blocking.
        # We do not want to wait until the user types each char to check WPM.
        # Else the entire logic will be faulty.
        self.stdscr.nodelay(True)

        while True:
            # Since we have nodelay = True, if not using max(), 
            # users might end up with time.time() equal to start_time,
            # resulting in 0 and potentially causing a zero-divisible error in the below line.
            time_elapsed = max(time.time() - self.start_time, 1)

            # Considering the average word length in English is 5 characters
            self.wpm = round((len(self.user_typed_text) / (time_elapsed / 60)) / 5)
            self.stdscr.clear()
            self.display_details()
            self.stdscr.refresh()

            # Exit the loop when the user types in the total length of the text.
            if len(self.user_typed_text) == len(self.to_type_text):
                self.stdscr.nodelay(False)
                break

            # We have `nodelay = True`, so we don't want to wait for the keystroke.
            # If we do not get a key, it will throw an exception
            # in the below lines when accessing the key.
            try:
                key = self.stdscr.getkey()
            except Exception:
                continue

            # Check if the key is a single character before using ord()
            if isinstance(key, str) and len(key) == 1:
                if ord(key) == 27:  # ASCII value for ESC
                    break

            # If the user has not typed anything reset to the current time
            if not self.user_typed_text:
                self.start_time = time.time()

            if key in ("KEY_BACKSPACE", "\b", "\x7f"):
                if len(self.user_typed_text) > 0:
                    self.user_typed_text.pop()
            elif len(self.user_typed_text) < len(self.to_type_text):
                self.user_typed_text.append(key)
