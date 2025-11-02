import tkinter as tk
from tkinter import font

root = tk.Tk()
root.title("English Alphabet")

title_font = font.Font(family="Helvetica", size=16, weight="bold")
title_label = tk.Label(root, text="English Alphabet", font=title_font)
title_label.grid(row=0, column=0, columnspan=7, pady=15)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ."
letters_font = font.Font(family="Helvetica", size=24, weight="bold")

text_entry = tk.Entry(root, font=font.Font(family="Helvetica", size=12), width=40)

def create_click_handler(char):
    def on_click():
        text_entry.insert(tk.END, char)
    return on_click

for idx, letter in enumerate(alphabet):
    row = (idx // 7) + 1
    col = idx % 7
    letter_label = tk.Label(root, text=letter, font=letters_font, width=4, height=2, relief="solid", borderwidth=1, cursor="hand2")
    letter_label.grid(row=row, column=col, padx=5, pady=5)
    letter_label.bind("<Button-1>", lambda e, char=letter: create_click_handler(char)())

text_entry.grid(row=5, column=0, columnspan=7, pady=15, padx=5, sticky="ew")

root.update_idletasks()
root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

root.mainloop()
