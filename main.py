import tkinter as tk
from tkinter import font

root = tk.Tk()
root.title("English Alphabet")

HIGHLIGHT_INTERVAL = 1000  # milliseconds

title_font = font.Font(family="Helvetica", size=16, weight="bold")
title_label = tk.Label(root, text="English Alphabet", font=title_font)
title_label.grid(row=0, column=0, columnspan=7, pady=15)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ."
letters_font = font.Font(family="Helvetica", size=24, weight="bold")

text_entry = tk.Entry(root, font=font.Font(family="Helvetica", size=12), width=40)

letter_labels = []
current_highlight_idx = [0]
highlight_timer = [None]

def create_click_handler(char):
    def on_click():
        text_entry.insert(tk.END, char)
    return on_click

def update_highlight():
    old_idx = current_highlight_idx[0]
    letter_labels[old_idx].config(bg="SystemButtonFace", fg="black")
    
    current_highlight_idx[0] = (current_highlight_idx[0] + 1) % len(letter_labels)
    new_idx = current_highlight_idx[0]
    letter_labels[new_idx].config(bg="blue", fg="white")
    
    highlight_timer[0] = root.after(HIGHLIGHT_INTERVAL, update_highlight)

def on_space_key(event):
    char = alphabet[current_highlight_idx[0]]
    text_entry.insert(tk.END, char)

for idx, letter in enumerate(alphabet):
    row = (idx // 7) + 1
    col = idx % 7
    letter_label = tk.Label(root, text=letter, font=letters_font, width=4, height=2, relief="solid", borderwidth=1, cursor="hand2")
    letter_label.grid(row=row, column=col, padx=5, pady=5)
    letter_label.bind("<Button-1>", lambda e, char=letter: create_click_handler(char)())
    letter_labels.append(letter_label)

letter_labels[0].config(bg="blue", fg="white")

text_entry.grid(row=5, column=0, columnspan=7, pady=15, padx=5, sticky="ew")

root.bind("<space>", on_space_key)

root.update_idletasks()
root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

highlight_timer[0] = root.after(HIGHLIGHT_INTERVAL, update_highlight)

root.mainloop()
