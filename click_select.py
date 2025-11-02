import tkinter as tk
from tkinter import font
import pyautogui
import time
import keyboard
import threading

space_pressed = False

def handle_space():
    if menu_active[0]:
        option = menu_options[menu_selected[0]]
        x1, y1, x2, y2 = current_region
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        
        try:
            if option == 'LEFT CLICK':
                pyautogui.click(center_x, center_y, button='left')
            elif option == 'RIGHT CLICK':
                pyautogui.mouseDown(center_x, center_y, button='right')
                time.sleep(0.05)
                pyautogui.mouseUp(button='right')
            elif option == 'CANCEL':
                pass
        except Exception as e:
            print(f"Click error: {e}")
        
        time.sleep(0.2)
        reset_region()
    else:
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
        timer_start[0] = time.time()
        
        new_width = current_region[2] - current_region[0]
        new_height = current_region[3] - current_region[1]
        
        if new_width <= MIN_BOX_SIZE or new_height <= MIN_BOX_SIZE:
            enter_menu()
        else:
            draw_regions()

def handle_escape():
    root.destroy()

root = tk.Tk()
root.attributes('-topmost', True)
root.wm_attributes('-transparentcolor', 'white')
root.overrideredirect(True)

progress_canvas = tk.Canvas(root, height=8, bg='white', highlightthickness=0)
progress_canvas.pack(fill=tk.X, side=tk.TOP)
progress_bar = progress_canvas.create_rectangle(0, 0, 0, 8, fill="blue", outline="blue")

timer_start = [time.time()]

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
menu_active = [False]
menu_options = ['LEFT CLICK', 'RIGHT CLICK', 'CANCEL']
menu_selected = [0]
menu_selection_locked = [False]
menu_region = [0, len(menu_options)]

def handle_menu_selection():
    start_idx, end_idx = menu_region
    selected_idx = start_idx
    option = menu_options[selected_idx]
    
    x1, y1, x2, y2 = current_region
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    
    if option == 'LEFT CLICK':
        pyautogui.click(center_x, center_y, button='left')
    elif option == 'RIGHT CLICK':
        pyautogui.click(center_x, center_y, button='right')
    elif option == 'CANCEL':
        pass
    
    reset_region()

def draw_menu():
    canvas.delete("all")
    
    x1, y1, x2, y2 = current_region
    width = x2 - x1
    height = y2 - y1
    center_x = x1 + width // 2
    center_y = y1 + height // 2
    
    box_width = 90
    box_height = 70
    box_spacing = 60
    
    boxes = [
        (center_x - box_width - box_spacing, center_y - box_height // 2, center_x - box_spacing, center_y + box_height // 2, "LEFT\nCLICK"),
        (center_x + box_spacing, center_y - box_height // 2, center_x + box_width + box_spacing, center_y + box_height // 2, "RIGHT\nCLICK"),
        (center_x - box_width // 2, center_y + box_spacing + box_height // 2, center_x + box_width // 2, center_y + box_spacing + box_height, "CANCEL")
    ]
    
    for i, (bx1, by1, bx2, by2, label) in enumerate(boxes):
        if i == menu_selected[0]:
            bg_color = "blue"
            text_color = "white"
            outline_width = 4
        else:
            bg_color = "lightgray"
            text_color = "black"
            outline_width = 2
        
        canvas.create_rectangle(bx1, by1, bx2, by2, fill=bg_color, outline="blue" if i == menu_selected[0] else "gray", width=outline_width)
        canvas.create_text((bx1 + bx2) // 2, (by1 + by2) // 2, text=label, font=("Arial", 13, "bold"), fill=text_color)
    
    canvas.create_line(center_x - 10, center_y, center_x + 10, center_y, fill="red", width=2)
    canvas.create_line(center_x, center_y - 10, center_x, center_y + 10, fill="red", width=2)

def enter_menu():
    global menu_active
    menu_active[0] = True
    menu_selected[0] = 0
    toggle_state[0] = True
    timer_start[0] = time.time()
    draw_menu()

def update_progress_bar():
    try:
        if root.winfo_exists():
            elapsed = (time.time() - timer_start[0]) * 1000
            progress = min(max(elapsed / SPLIT_INTERVAL, 0), 1.0)
            canvas_width = progress_canvas.winfo_width()
            if canvas_width > 1:
                fill_width = max(0, min(canvas_width * progress, canvas_width))
                progress_canvas.coords(progress_bar, 0, 0, fill_width, 8)
            root.after(10, update_progress_bar)
    except:
        root.after(10, update_progress_bar)

def draw_regions():
    global rect_id
    canvas.delete("all")
    
    x1, y1, x2, y2 = current_region
    width = x2 - x1
    height = y2 - y1
    
    if split_horizontal[0]:
        mid_x = x1 + width // 2
        
        if toggle_state[0]:
            canvas.create_rectangle(x1, y1, mid_x, y2, fill="#F0F8FF", outline="blue", width=8, stipple="gray12")
            canvas.create_rectangle(mid_x, y1, x2, y2, outline="lightgray", width=2)
        else:
            canvas.create_rectangle(x1, y1, mid_x, y2, outline="lightgray", width=2)
            canvas.create_rectangle(mid_x, y1, x2, y2, fill="#F0F8FF", outline="blue", width=8, stipple="gray12")
    else:
        mid_y = y1 + height // 2
        
        if toggle_state[0]:
            canvas.create_rectangle(x1, y1, x2, mid_y, fill="#F0F8FF", outline="blue", width=8, stipple="gray12")
            canvas.create_rectangle(x1, mid_y, x2, y2, outline="lightgray", width=2)
        else:
            canvas.create_rectangle(x1, y1, x2, mid_y, outline="lightgray", width=2)
            canvas.create_rectangle(x1, mid_y, x2, y2, fill="#F0F8FF", outline="blue", width=8, stipple="gray12")
    
    update_timer()

def update_timer():
    if split_timer[0] is not None:
        root.after_cancel(split_timer[0])
    
    def toggle_highlight():
        toggle_state[0] = not toggle_state[0]
        timer_start[0] = time.time()
        
        if menu_active[0]:
            menu_selected[0] = (menu_selected[0] + 1) % len(menu_options)
            draw_menu()
        else:
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
    menu_active[0] = False
    timer_start[0] = time.time()
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

timer_start[0] = time.time()
update_progress_bar()

draw_regions()
root.mainloop()
