import json
import os
from pynput import keyboard
from pathlib import Path
from datetime import datetime
import threading
import time

STATS_FILE = "keystats.json"
SAVE_INTERVAL = 5  # seconds

keystats = {}
running = True
modifiers = {
    'shift': False,
    'ctrl': False,
    'alt': False
}

def load_stats():
    global keystats
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            keystats = json.load(f)
    else:
        keystats = {}

def save_stats():
    sorted_stats = dict(sorted(keystats.items(), key=lambda x: x[1], reverse=True))
    with open(STATS_FILE, 'w') as f:
        json.dump(sorted_stats, f, indent=2)

def periodic_save():
    global running
    while running:
        time.sleep(SAVE_INTERVAL)
        if running:
            save_stats()
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Stats saved ({len(keystats)} unique keys)", end='\r')

def is_control_character(char):
    if not char:
        return True
    if len(char) == 1:
        code = ord(char)
        return code < 32 and code not in [9, 10, 13]  # Allow tab, newline, carriage return
    return False

def normalize_key(key):
    try:
        if hasattr(key, 'char'):
            char = key.char
            if char is None or is_control_character(char):
                return None
            # If shift is held and it's a letter, just use lowercase
            if modifiers['shift'] and char.isalpha():
                return char.lower()
            return char
        elif hasattr(key, 'name'):
            name = key.name
            if name == 'space':
                return ' '
            # Special combinations
            if name == 'backspace' and modifiers['shift']:
                return 'delete_word'
            if name == 'backspace':
                return 'backspace'
            if name == 'enter':
                return 'enter'
            # Ignore pure modifier keys
            if name in ['shift', 'shift_l', 'shift_r', 'ctrl_l', 'ctrl_r', 'alt_l', 'alt_r', 'alt_gr', 'caps_lock']:
                return None
            return name
        else:
            return None
    except:
        return None

def update_modifiers(key, is_press):
    try:
        if hasattr(key, 'name'):
            name = key.name
            if name in ['shift', 'shift_l', 'shift_r']:
                modifiers['shift'] = is_press
            elif name in ['ctrl_l', 'ctrl_r']:
                modifiers['ctrl'] = is_press
            elif name in ['alt_l', 'alt_r', 'alt_gr']:
                modifiers['alt'] = is_press
    except:
        pass

def on_press(key):
    update_modifiers(key, True)
    try:
        normalized = normalize_key(key)
        if normalized:
            keystats[normalized] = keystats.get(normalized, 0) + 1
            print(f"{normalized}: {keystats[normalized]}", end='\r')
    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    global running
    update_modifiers(key, False)
    try:
        if key == keyboard.Key.esc:
            running = False
            save_stats()
            print("\n\nKeylogger stopped. Stats saved to keystats.json")
            return False
    except AttributeError:
        pass

load_stats()
print("Keylogger started. Press ESC to stop...")
print(f"Auto-saving every {SAVE_INTERVAL} seconds.\n")

save_thread = threading.Thread(target=periodic_save, daemon=True)
save_thread.start()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

running = False
save_thread.join(timeout=1)
