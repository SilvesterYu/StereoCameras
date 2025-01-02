from pynput import keyboard

def on_press(key):
    try:
        if key.char == 'a':  # Detect a one-time press of the 'a' key
            print("Key 'a' detected!")
            return False  # Stop the listener
    except AttributeError:
        pass  # Handle special keys (like shift, ctrl, etc.)

    if key == keyboard.Key.esc:  # Exit on 'Esc' key
        print("Exiting...")
        return False

if __name__ == "__main__":
    print("Press the 'a' key to detect a one-time key press. Press 'Esc' to exit.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()