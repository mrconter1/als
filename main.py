import tkinter as tk
from tkinter import font

root = tk.Tk()
root.title("Keyboard")

HIGHLIGHT_INTERVAL = 1000  # milliseconds

title_font = font.Font(family="Helvetica", size=16, weight="bold")
title_label = tk.Label(root, text="Keyboard", font=title_font)
title_label.pack(pady=15)

keyboard_layout = [
    [('1', 1), ('2', 1), ('3', 1), ('4', 1), ('5', 1), ('6', 1), ('7', 1), ('8', 1), ('9', 1), ('0', 1), ('BACK', 1.5)],
    [('Q', 1), ('W', 1), ('E', 1), ('R', 1), ('T', 1), ('Y', 1), ('U', 1), ('I', 1), ('O', 1), ('P', 1)],
    [('CAPS', 1.5), ('A', 1), ('S', 1), ('D', 1), ('F', 1), ('G', 1), ('H', 1), ('J', 1), ('K', 1), ('L', 1), ('ENTER', 1.5)],
    [('Z', 1), ('X', 1), ('C', 1), ('V', 1), ('B', 1), ('N', 1), ('M', 1), (',', 1), ('.', 1)],
    [('!', 1), ('"', 1), ('#', 1), ('$', 1), ('%', 1), ('^', 1), ('&', 1), ('*', 1), ('(', 1), (')', 1)],
    [('-', 1), ('=', 1), ('[', 1), (']', 1), (';', 1), ("'", 1), ('/', 1), ('?', 1)],
    [('SPACE', 7)],
    [('←', 1), ('↑', 1), ('↓', 1), ('→', 1)]
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

def create_click_handler(char):
    def on_click():
        if char == 'BACK':
            current_text = text_entry.get(1.0, tk.END)
            text_entry.delete(1.0, tk.END)
            text_entry.insert(1.0, current_text[:-1])
            capitalize_next[0] = False
        elif char == 'ENTER':
            text_entry.insert(tk.END, '\n')
            capitalize_next[0] = True
        elif char == 'CAPS':
            pass
        elif char == 'SPACE':
            text_entry.insert(tk.END, ' ')
            if should_capitalize_after_space():
                capitalize_next[0] = True
        else:
            if char.isalpha() and capitalize_next[0]:
                text_entry.insert(tk.END, char.upper())
                capitalize_next[0] = False
            elif char.isalpha():
                text_entry.insert(tk.END, char.lower())
            else:
                text_entry.insert(tk.END, char)
                if char in '.!?':
                    pass
                elif char == ' ':
                    if should_capitalize_after_space():
                        capitalize_next[0] = True
    return on_click

def update_highlight():
    show_first_half = toggle_state[0]
    start_idx, end_idx = current_range[0]
    mid_idx = (start_idx + end_idx) // 2
    
    for i in range(len(key_labels)):
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

def on_space_key(event):
    start_idx, end_idx = current_range[0]
    
    if start_idx == end_idx - 1:
        char = flat_keys[start_idx]
        if char == 'BACK':
            current_text = text_entry.get(1.0, tk.END)
            text_entry.delete(1.0, tk.END)
            text_entry.insert(1.0, current_text[:-1])
            capitalize_next[0] = False
        elif char == 'ENTER':
            text_entry.insert(tk.END, '\n')
            capitalize_next[0] = True
        elif char == 'CAPS':
            pass
        elif char == 'SPACE':
            text_entry.insert(tk.END, ' ')
            if should_capitalize_after_space():
                capitalize_next[0] = True
        else:
            if char.isalpha() and capitalize_next[0]:
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
                current_text = text_entry.get(1.0, tk.END)
                text_entry.delete(1.0, tk.END)
                text_entry.insert(1.0, current_text[:-1])
                capitalize_next[0] = False
            elif char == 'ENTER':
                text_entry.insert(tk.END, '\n')
                capitalize_next[0] = True
            elif char == 'CAPS':
                pass
            elif char == 'SPACE':
                text_entry.insert(tk.END, ' ')
                if should_capitalize_after_space():
                    capitalize_next[0] = True
            else:
                if char.isalpha() and capitalize_next[0]:
                    text_entry.insert(tk.END, char.upper())
                    capitalize_next[0] = False
                elif char.isalpha():
                    text_entry.insert(tk.END, char.lower())
                else:
                    text_entry.insert(tk.END, char)
            current_range[0] = [0, len(key_labels)]
            toggle_state[0] = True
            update_highlight()
        else:
            update_highlight()

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

text_entry = tk.Text(root, font=font.Font(family="Helvetica", size=12), width=50, height=5)
text_entry.pack(pady=15, padx=5)

root.bind("<space>", on_space_key)

root.update_idletasks()
root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

highlight_timer = [None]
highlight_timer[0] = root.after(HIGHLIGHT_INTERVAL, update_highlight)

root.mainloop()
