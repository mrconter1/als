import tkinter as tk
from tkinter import font
import pyttsx3
import threading

root = tk.Tk()
root.title("Keyboard")

HIGHLIGHT_INTERVAL = 1000  # milliseconds

title_font = font.Font(family="Helvetica", size=16, weight="bold")
title_label = tk.Label(root, text="Keyboard", font=title_font)
title_label.pack(pady=15)

progress_canvas = tk.Canvas(root, height=8, bg="white", highlightthickness=0)
progress_canvas.pack(fill=tk.X, padx=10, pady=5)
progress_bar = progress_canvas.create_rectangle(0, 0, 0, 8, fill="blue", outline="blue")

def calculate_split_depth(index, total_items):
    """Calculate how many binary splits needed to reach position index"""
    depth = 0
    start, end = 0, total_items
    while end - start > 1:
        mid = (start + end) // 2
        if index < mid:
            end = mid
        else:
            start = mid
        depth += 1
    return depth

def optimize_keyboard_layout():
    """Reorganize keyboard with frequency optimization and clean visual layout"""
    
    # Organize keys by frequency tiers for visual organization
    tier1 = [('E', 1), ('T', 1), ('A', 1), ('O', 1), ('I', 1), ('N', 1), ('S', 1), ('H', 1), ('R', 1), ('.', 1)]
    tier2 = [('D', 1), ('L', 1), ('C', 1), ('U', 1), ('M', 1), ('W', 1), ('F', 1), ('G', 1), ('Y', 1), ('P', 1)]
    tier3 = [('B', 1), ('V', 1), ('K', 1), (',', 1), ('-', 1), ("'", 1), ('?', 1), ('J', 1), ('X', 1), ('!', 1)]
    tier4 = [(':', 1), ('=', 1), ('>', 1), ('(', 1), (')', 1), ('/', 1)]
    
    layout = [
        tier1,
        tier2,
        tier3,
        tier4,
        [('BACK', 1.5), ('SAY', 1.5), ('ENTER', 1.5), ('CLR', 2)],
        [('SPACE', 7)],
        [('←', 1), ('↑', 1), ('↓', 1), ('→', 1)]
    ]
    
    return layout

def update_progress_bar():
    if state['highlight_timer'] is not None:
        elapsed = (time.time() - state['timer_start']) * 1000
        progress = min(elapsed / HIGHLIGHT_INTERVAL, 1.0)
        canvas_width = progress_canvas.winfo_width()
        if canvas_width > 1:
            fill_width = canvas_width * progress
            progress_canvas.coords(progress_bar, 0, 0, fill_width, 8)
    root.after(10, update_progress_bar)

import time

keyboard_layout = optimize_keyboard_layout()

keyboard_frame = tk.Frame(root)
keyboard_frame.pack(pady=10)

key_font = font.Font(family="Helvetica", size=12, weight="bold")
key_labels = []
flat_keys = []

def should_capitalize_after_space():
    current_text = text_entry.get(1.0, tk.END).rstrip('\n')
    if len(current_text) > 0:
        last_char = current_text[-1]
        return last_char in '.!?'
    return False

def speak_text():
    text_content = text_entry.get(1.0, tk.END).rstrip('\n')
    if text_content:
        def speak_in_thread():
            local_engine = pyttsx3.init()
            local_engine.setProperty('rate', 150)
            local_engine.say(text_content)
            local_engine.runAndWait()
        thread = threading.Thread(target=speak_in_thread, daemon=True)
        thread.start()

def handle_backspace():
    cursor_pos = text_entry.index(tk.INSERT)
    prev_pos = text_entry.index(cursor_pos + "-1c")
    if cursor_pos != prev_pos:
        text_entry.delete(prev_pos, cursor_pos)
    state['capitalize_next'] = False

def handle_character_action(char):
    """Handle insertion or action for any character or special key"""
    if char == 'BACK':
        handle_backspace()
    elif char == 'SAY':
        speak_text()
    elif char == 'ENTER':
        text_entry.insert(tk.END, '\n')
        state['capitalize_next'] = True
    elif char == 'CAPS':
        pass
    elif char == 'SPACE':
        text_entry.insert(tk.END, ' ')
        if should_capitalize_after_space():
            state['capitalize_next'] = True
    elif char == '←':
        text_entry.mark_set(tk.INSERT, text_entry.index(tk.INSERT + "-1c"))
    elif char == '→':
        text_entry.mark_set(tk.INSERT, text_entry.index(tk.INSERT + "+1c"))
    elif char == '↑':
        text_entry.mark_set(tk.INSERT, text_entry.index(tk.INSERT + "-1l linestart"))
    elif char == '↓':
        text_entry.mark_set(tk.INSERT, text_entry.index(tk.INSERT + "+1l linestart"))
    elif char == 'CLR':
        text_entry.delete(1.0, tk.END)
    else:
        if char.lower() == 'i':
            current_text = text_entry.get(1.0, tk.END).rstrip('\n')
            if len(current_text) == 0 or current_text[-1] == ' ':
                text_entry.insert(tk.END, 'I')
            else:
                text_entry.insert(tk.END, 'i')
            state['capitalize_next'] = False
        elif char.isalpha() and state['capitalize_next']:
            text_entry.insert(tk.END, char.upper())
            state['capitalize_next'] = False
        elif char.isalpha():
            text_entry.insert(tk.END, char.lower())
        else:
            text_entry.insert(tk.END, char)

def create_click_handler(char):
    def on_click():
        handle_character_action(char)
    return on_click

def update_highlight():
    show_first_half = state['toggle_state']
    start_idx, end_idx = state['current_range']
    mid_idx = (start_idx + end_idx) // 2
    
    for i in range(len(key_labels)):
        if start_idx <= i < end_idx:
            key_labels[i].config(bg="lightgray", fg="black")
        else:
            key_labels[i].config(bg="SystemButtonFace", fg="black")
    
    if start_idx == end_idx - 1:
        key_labels[start_idx].config(bg="blue", fg="white")
    else:
        if show_first_half:
            for i in range(start_idx, mid_idx):
                key_labels[i].config(bg="blue", fg="white")
        else:
            for i in range(mid_idx, end_idx):
                key_labels[i].config(bg="blue", fg="white")
        
        state['toggle_state'] = not state['toggle_state']
        state['highlight_timer'] = root.after(HIGHLIGHT_INTERVAL, update_highlight)
        state['timer_start'] = time.time()

def on_space_key(event):
    start_idx, end_idx = state['current_range']
    
    if start_idx == end_idx - 1:
        char = flat_keys[start_idx]
        handle_character_action(char)
        state['current_range'] = [0, len(key_labels)]
        state['toggle_state'] = True
        root.after_cancel(state['highlight_timer'])
        update_highlight()
        state['timer_start'] = time.time()
    else:
        mid_idx = (start_idx + end_idx) // 2
        if state['toggle_state']:
            state['current_range'] = [mid_idx, end_idx]
        else:
            state['current_range'] = [start_idx, mid_idx]
        state['toggle_state'] = True
        root.after_cancel(state['highlight_timer'])
        for i in range(len(key_labels)):
            key_labels[i].config(bg="SystemButtonFace", fg="black")
        
        new_start, new_end = state['current_range']
        if new_start == new_end - 1:
            char = flat_keys[new_start]
            handle_character_action(char)
            state['current_range'] = [0, len(key_labels)]
            state['toggle_state'] = True
            update_highlight()
            state['timer_start'] = time.time()
        else:
            update_highlight()
            state['timer_start'] = time.time()
    return "break"

for row_idx, row in enumerate(keyboard_layout):
    row_frame = tk.Frame(keyboard_frame)
    row_frame.pack()
    
    for key_info in row:
        if isinstance(key_info, tuple):
            key, width = key_info
        else:
            key = key_info
            width = 1
        
        key_label = tk.Label(row_frame, text=key, font=key_font, width=int(width*4), height=2, relief="solid", borderwidth=1, cursor="hand2")
        key_label.pack(side=tk.LEFT, padx=2, pady=2)
        key_label.bind("<Button-1>", lambda e, char=key: create_click_handler(char)())
        key_labels.append(key_label)
        flat_keys.append(key)

state = {
    'current_range': [0, len(key_labels)],
    'toggle_state': True,
    'highlight_timer': None,
    'timer_start': time.time()
}

text_entry = tk.Text(root, font=font.Font(family="Helvetica", size=12), width=50, height=5, insertwidth=2, insertbackground="blue")
text_entry.pack(pady=15, padx=5)

state['cursor_visible'] = True
state['cursor_blink_timer'] = None
state['capitalize_next'] = True

def toggle_cursor_blink():
    if state['cursor_visible']:
        text_entry.config(insertwidth=2)
    else:
        text_entry.config(insertwidth=0)
    state['cursor_visible'] = not state['cursor_visible']
    state['cursor_blink_timer'] = root.after(500, toggle_cursor_blink)

def create_arrow_handler(movement):
    def on_arrow(event):
        text_entry.mark_set(tk.INSERT, text_entry.index(tk.INSERT + movement))
        return "break"
    return on_arrow

text_entry.bind("<Left>", create_arrow_handler("-1c"))
text_entry.bind("<Right>", create_arrow_handler("+1c"))
text_entry.bind("<Up>", create_arrow_handler("-1l linestart"))
text_entry.bind("<Down>", create_arrow_handler("+1l linestart"))
text_entry.bind(".", on_space_key)

text_entry.focus()
toggle_cursor_blink()

root.bind(".", on_space_key)

root.update_idletasks()
root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

state['highlight_timer'] = root.after(HIGHLIGHT_INTERVAL, update_highlight)
update_progress_bar()

root.mainloop()
