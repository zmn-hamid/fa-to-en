import pyperclip
import keyboard
from deep_translator import GoogleTranslator
import time
import sys
import pystray
from PIL import Image, ImageDraw
import threading

SHORTCUT = "ctrl+alt+f9"


def translate_and_copy():
    """
    Fetches text from the clipboard, translates it to English,
    copies the result back to the clipboard, and automatically pastes it.
    """
    print("\n--- Shortcut Activated! ---")
    try:
        original_text = pyperclip.paste()
        if not original_text or not original_text.strip():
            print("Clipboard is empty. Nothing to translate.")
            return

        print(f"Original Text (from clipboard): {original_text}")
        print("Translating...")
        translated_text = GoogleTranslator(source="auto", target="en").translate(
            original_text
        )

        if not translated_text:
            print("Translation failed or resulted in empty text.")
            return

        print(f"Translated Text: {translated_text}")
        pyperclip.copy(translated_text)
        print("--- Translated text has been copied to your clipboard! ---")

        # Simulate Ctrl+V to paste the translated text
        time.sleep(0.1)  # Small delay to ensure clipboard is ready
        keyboard.press_and_release("ctrl+v")
        print("--- Translated text has been pasted! ---")

    except Exception as e:
        print(f"An error occurred: {e}")


def create_icon():
    """Create a simple 32x32 icon for the system tray with a 'T'."""
    image = Image.new("RGB", (32, 32), color="blue")
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), "T", fill="white")
    return image


def run_system_tray():
    """Run the system tray icon with an exit option."""
    icon = pystray.Icon("Translator")
    icon.icon = create_icon()
    icon.menu = pystray.Menu(pystray.MenuItem("Exit", lambda: on_exit(icon)))
    icon.run()


def on_exit(icon):
    """Handle the exit action from the system tray."""
    icon.stop()
    print("\nSystem tray closed. Exiting.")
    keyboard.unhook_all()  # Clean up hotkey
    sys.exit(0)


def main():
    """Main function to set up the hotkey and system tray."""
    print("-----------------------------------------------------")
    print("Shortcut Translator is running...")
    print(f"Press '{SHORTCUT.upper()}' to translate clipboard text.")
    print("Right-click the system tray icon to exit.")
    print("-----------------------------------------------------")

    # Start the system tray in a separate thread
    tray_thread = threading.Thread(target=run_system_tray, daemon=True)
    tray_thread.start()

    # Register the hotkey
    keyboard.add_hotkey(SHORTCUT, translate_and_copy)

    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting.")
        sys.exit(0)


if __name__ == "__main__":
    main()
