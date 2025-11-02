import tkinter as tk
from tkinter import font
import pyautogui
import time
import keyboard
import threading

space_pressed = False

def handle_space():
    x1, y1, x2, y2 = current_region
    width = x2 - x1
    height = y2 - y1
    
    if split_horizontal[0]:
        mid_x = x1 + width // 2
        if toggle_state[0]:
            current_region[0] = x1
            current_region[2] = mid_x
        else:
            current_region[0] = mid_x
            current_region[2] = x2
    else:
        mid_y = y1 + height // 2
        if toggle_state[0]:
            current_region[1] = y1
            current_region[3] = mid_y
        else:
            current_region[1] = mid_y
            current_region[3] = y2
    
    split_horizontal[0] = not split_horizontal[0]
    toggle_state[0] = True
    
    new_width = current_region[2] - current_region[0]
    new_height = current_region[3] - current_region[1]
    
    if new_width <= MIN_BOX_SIZE or new_height <= MIN_BOX_SIZE:
        x1, y1, x2, y2 = current_region
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        pyautogui.click(center_x, center_y)
        reset_region()
    else:
        draw_regions()

def handle_escape():
    root.destroy()

root = tk.Tk()
root.attributes('-topmost', True)
root.wm_attributes('-transparentcolor', 'white')
root.overrideredirect(True)

SPLIT_INTERVAL = 1000  # milliseconds
MIN_BOX_SIZE = 50

canvas = tk.Canvas(root, bg='white', highlightthickness=0, cursor='crosshair')
canvas.pack(fill=tk.BOTH, expand=True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f'{screen_width}x{screen_height}+0+0')

current_region = [0, 0, screen_width, screen_height]
toggle_state = [True]
split_horizontal = [True]
split_timer = [None]
rect_id = None

def draw_regions():
    global rect_id
    canvas.delete("all")
    
    x1, y1, x2, y2 = current_region
    width = x2 - x1
    height = y2 - y1
    
    if split_horizontal[0]:
        mid_x = x1 + width // 2
        
        if toggle_state[0]:
            canvas.create_rectangle(x1, y1, mid_x, y2, outline="blue", width=3)
            canvas.create_rectangle(mid_x, y1, x2, y2, outline="gray", width=2)
        else:
            canvas.create_rectangle(x1, y1, mid_x, y2, outline="gray", width=2)
            canvas.create_rectangle(mid_x, y1, x2, y2, outline="blue", width=3)
    else:
        mid_y = y1 + height // 2
        
        if toggle_state[0]:
            canvas.create_rectangle(x1, y1, x2, mid_y, outline="blue", width=3)
            canvas.create_rectangle(x1, mid_y, x2, y2, outline="gray", width=2)
        else:
            canvas.create_rectangle(x1, y1, x2, mid_y, outline="gray", width=2)
            canvas.create_rectangle(x1, mid_y, x2, y2, outline="blue", width=3)
    
    update_timer()

def update_timer():
    if split_timer[0] is not None:
        root.after_cancel(split_timer[0])
    
    def toggle_highlight():
        toggle_state[0] = not toggle_state[0]
        draw_regions()
        split_timer[0] = root.after(SPLIT_INTERVAL, toggle_highlight)
    
    split_timer[0] = root.after(SPLIT_INTERVAL, toggle_highlight)

def reset_region():
    current_region[0] = 0
    current_region[1] = 0
    current_region[2] = screen_width
    current_region[3] = screen_height
    toggle_state[0] = True
    split_horizontal[0] = True
    draw_regions()

root.focus_force()

def on_space_pressed(event):
    handle_space()
    return True

def on_escape_pressed(event):
    handle_escape()
    return True

keyboard.on_press_key('space', on_space_pressed, suppress=True)
keyboard.on_press_key('esc', on_escape_pressed, suppress=True)

draw_regions()
root.mainloop()
