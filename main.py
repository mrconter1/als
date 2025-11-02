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

def create_click_handler(char):
    def on_click():
        if char == 'BACK':
            current_text = text_entry.get()
            text_entry.delete(0, tk.END)
            text_entry.insert(0, current_text[:-1])
        elif char == 'ENTER':
            text_entry.insert(tk.END, '\n')
        elif char == 'CAPS':
            pass
        elif char == 'SPACE':
            text_entry.insert(tk.END, ' ')
        else:
            text_entry.insert(tk.END, char)
    return on_click

def update_highlight():
    old_idx = current_highlight_idx[0]
    key_labels[old_idx].config(bg="SystemButtonFace", fg="black")
    
    current_highlight_idx[0] = (current_highlight_idx[0] + 1) % len(key_labels)
    new_idx = current_highlight_idx[0]
    key_labels[new_idx].config(bg="blue", fg="white")
    
    highlight_timer[0] = root.after(HIGHLIGHT_INTERVAL, update_highlight)

def on_space_key(event):
    char = flat_keys[current_highlight_idx[0]]
    if char == 'BACK':
        current_text = text_entry.get()
        text_entry.delete(0, tk.END)
        text_entry.insert(0, current_text[:-1])
    elif char == 'ENTER':
        text_entry.insert(tk.END, '\n')
    elif char == 'CAPS':
        pass
    elif char == 'SPACE':
        text_entry.insert(tk.END, ' ')
    else:
        text_entry.insert(tk.END, char)

current_highlight_idx = [0]
highlight_timer = [None]

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

key_labels[0].config(bg="blue", fg="white")

text_entry = tk.Text(root, font=font.Font(family="Helvetica", size=12), width=50, height=5)
text_entry.pack(pady=15, padx=5)

root.bind("<space>", on_space_key)

root.update_idletasks()
root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

highlight_timer[0] = root.after(HIGHLIGHT_INTERVAL, update_highlight)

root.mainloop()
