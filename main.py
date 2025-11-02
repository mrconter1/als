import tkinter as tk
from tkinter import font

root = tk.Tk()
root.title("Keyboard")

HIGHLIGHT_INTERVAL = 1000  # milliseconds

title_font = font.Font(family="Helvetica", size=16, weight="bold")
title_label = tk.Label(root, text="Keyboard", font=title_font)
title_label.pack(pady=15)

progress_canvas = tk.Canvas(root, height=8, bg="white", highlightthickness=0)
progress_canvas.pack(fill=tk.X, padx=10, pady=5)
progress_bar = progress_canvas.create_rectangle(0, 0, 0, 8, fill="blue", outline="blue")

def update_progress_bar():
    if highlight_timer[0] is not None:
        elapsed = (time.time() - timer_start[0]) * 1000
        progress = min(elapsed / HIGHLIGHT_INTERVAL, 1.0)
        canvas_width = progress_canvas.winfo_width()
        if canvas_width > 1:
            fill_width = canvas_width * progress
            progress_canvas.coords(progress_bar, 0, 0, fill_width, 8)
    root.after(10, update_progress_bar)

import time
timer_start = [time.time()]

keyboard_layout = [
    [('E', 1), ('T', 1), ('O', 1), ('A', 1), ('N', 1), ('I', 1), ('R', 1), ('S', 1), ('H', 1), ('BACK', 1.5)],
    [('C', 1), ('L', 1), ('D', 1), ('ENTER', 1.5), ('.', 1), ('W', 1), ('U', 1), ('B', 1), ('K', 1), ('P', 1)],
    [('Y', 1), ('F', 1), ('G', 1), ('M', 1), ('?', 1), ('-', 1), ('X', 1), ('"', 1), ('V', 1), (',', 1)],
    [("'", 1), (')', 1), (':', 1), ('J', 1), ('Z', 1), ('=', 1), ('>', 1), ('(', 1), ('!', 1), ('/', 1)],
    [('å', 1)],
    [('SPACE', 7)],
    [('←', 1), ('↑', 1), ('↓', 1), ('→', 1), ('CLR', 2)]
]

keyboard_frame = tk.Frame(root)
keyboard_frame.pack(pady=10)

key_font = font.Font(family="Helvetica", size=12, weight="bold")
key_labels = []
flat_keys = []
capitalize_next = [True]

def should_capitalize_after_space():
    current_text = text_entry.get(1.0, tk.END).rstrip('\n')
    if len(current_text) > 0:
        last_char = current_text[-1]
        return last_char in '.!?'
    return False

def handle_backspace():
    cursor_pos = text_entry.index(tk.INSERT)
    prev_pos = text_entry.index(cursor_pos + "-1c")
    if cursor_pos != prev_pos:
        text_entry.delete(prev_pos, cursor_pos)
    capitalize_next[0] = False

def create_click_handler(char):
    def on_click():
        if char == 'BACK':
            handle_backspace()
        elif char == 'ENTER':
            text_entry.insert(tk.END, '\n')
            capitalize_next[0] = True
        elif char == 'CAPS':
            pass
        elif char == 'SPACE':
            text_entry.insert(tk.END, ' ')
            if should_capitalize_after_space():
                capitalize_next[0] = True
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
                capitalize_next[0] = False
            elif char.isalpha() and capitalize_next[0]:
                text_entry.insert(tk.END, char.upper())
                capitalize_next[0] = False
            elif char.isalpha():
                text_entry.insert(tk.END, char.lower())
            else:
                text_entry.insert(tk.END, char)
    return on_click

def update_highlight():
    show_first_half = toggle_state[0]
    start_idx, end_idx = current_range[0]
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
        
        toggle_state[0] = not toggle_state[0]
        highlight_timer[0] = root.after(HIGHLIGHT_INTERVAL, update_highlight)
        timer_start[0] = time.time()

def on_space_key(event):
    start_idx, end_idx = current_range[0]
    
    if start_idx == end_idx - 1:
        char = flat_keys[start_idx]
        if char == 'BACK':
            handle_backspace()
        elif char == 'ENTER':
            text_entry.insert(tk.END, '\n')
            capitalize_next[0] = True
        elif char == 'CAPS':
            pass
        elif char == 'SPACE':
            text_entry.insert(tk.END, ' ')
            if should_capitalize_after_space():
                capitalize_next[0] = True
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
                capitalize_next[0] = False
            elif char.isalpha() and capitalize_next[0]:
                text_entry.insert(tk.END, char.upper())
                capitalize_next[0] = False
            elif char.isalpha():
                text_entry.insert(tk.END, char.lower())
            else:
                text_entry.insert(tk.END, char)
        current_range[0] = [0, len(key_labels)]
        toggle_state[0] = True
        root.after_cancel(highlight_timer[0])
        update_highlight()
        timer_start[0] = time.time()
    else:
        mid_idx = (start_idx + end_idx) // 2
        if toggle_state[0]:
            current_range[0] = [mid_idx, end_idx]
        else:
            current_range[0] = [start_idx, mid_idx]
        toggle_state[0] = True
        root.after_cancel(highlight_timer[0])
        for i in range(len(key_labels)):
            key_labels[i].config(bg="SystemButtonFace", fg="black")
        
        new_start, new_end = current_range[0]
        if new_start == new_end - 1:
            char = flat_keys[new_start]
            if char == 'BACK':
                handle_backspace()
            elif char == 'ENTER':
                text_entry.insert(tk.END, '\n')
                capitalize_next[0] = True
            elif char == 'CAPS':
                pass
            elif char == 'SPACE':
                text_entry.insert(tk.END, ' ')
                if should_capitalize_after_space():
                    capitalize_next[0] = True
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
                    capitalize_next[0] = False
                elif char.isalpha() and capitalize_next[0]:
                    text_entry.insert(tk.END, char.upper())
                    capitalize_next[0] = False
                elif char.isalpha():
                    text_entry.insert(tk.END, char.lower())
                else:
                    text_entry.insert(tk.END, char)
            current_range[0] = [0, len(key_labels)]
            toggle_state[0] = True
            update_highlight()
            timer_start[0] = time.time()
        else:
            update_highlight()
            timer_start[0] = time.time()
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

current_range = [[0, len(key_labels)]]
toggle_state = [True]

text_entry = tk.Text(root, font=font.Font(family="Helvetica", size=12), width=50, height=5, insertwidth=2, insertbackground="blue")
text_entry.pack(pady=15, padx=5)

cursor_visible = [True]
cursor_blink_timer = [None]

def toggle_cursor_blink():
    if cursor_visible[0]:
        text_entry.config(insertwidth=2)
    else:
        text_entry.config(insertwidth=0)
    cursor_visible[0] = not cursor_visible[0]
    cursor_blink_timer[0] = root.after(500, toggle_cursor_blink)

def on_arrow_left(event):
    text_entry.mark_set(tk.INSERT, text_entry.index(tk.INSERT + "-1c"))
    return "break"

def on_arrow_right(event):
    text_entry.mark_set(tk.INSERT, text_entry.index(tk.INSERT + "+1c"))
    return "break"

def on_arrow_up(event):
    text_entry.mark_set(tk.INSERT, text_entry.index(tk.INSERT + "-1l linestart"))
    return "break"

def on_arrow_down(event):
    text_entry.mark_set(tk.INSERT, text_entry.index(tk.INSERT + "+1l linestart"))
    return "break"

text_entry.bind("<Left>", on_arrow_left)
text_entry.bind("<Right>", on_arrow_right)
text_entry.bind("<Up>", on_arrow_up)
text_entry.bind("<Down>", on_arrow_down)
text_entry.bind(".", on_space_key)

text_entry.focus()
toggle_cursor_blink()

root.bind(".", on_space_key)

root.update_idletasks()
root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

highlight_timer = [None]
highlight_timer[0] = root.after(HIGHLIGHT_INTERVAL, update_highlight)
timer_start[0] = time.time()
update_progress_bar()

root.mainloop()
