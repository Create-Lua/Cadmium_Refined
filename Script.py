import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import requests
import tempfile
import os
import zipfile

def close_window():
    root.destroy()

root = tk.Tk()
root.overrideredirect(True)
root.geometry("400x300")
root.configure(bg="black")

title_bar = tk.Frame(root, bg="black", relief="raised", bd=0)
title_bar.pack(fill=tk.X)

title_label = tk.Label(title_bar, text="Cadmium Refined V1.0", bg="black", fg="white")
title_label.pack(side=tk.LEFT, padx=10)

close_btn = tk.Button(title_bar, text="X", bg="black", fg="white", bd=0, command=close_window)
close_btn.pack(side=tk.RIGHT, padx=5)

separator = tk.Frame(root, bg="gray", height=2)
separator.pack(fill=tk.X)
separator.pack_propagate(False)

center_text = tk.Label(root, text="Welcome To Cadmium Refined", bg="black", fg="white", font=("Segoe UI", 12))
center_text.pack(fill=tk.X, pady=(10,0))

second_text = tk.Label(root, text="Your all in one solution to gorilla tag modding", bg="black", fg="white", font=("Segoe UI", 12))
second_text.pack(fill=tk.X, pady=(5,10))

button_canvas = tk.Canvas(root, width=140, height=40, bg="black", highlightthickness=0)
button_canvas.pack(side=tk.BOTTOM, pady=20)

def draw_rounded_rect(canvas, x1, y1, x2, y2, radius, outline, width):
    canvas.create_arc(x1, y1, x1+2*radius, y1+2*radius, start=90, extent=90, style='arc', outline=outline, width=width)
    canvas.create_arc(x2-2*radius, y1, x2, y1+2*radius, start=0, extent=90, style='arc', outline=outline, width=width)
    canvas.create_arc(x2-2*radius, y2-2*radius, x2, y2, start=270, extent=90, style='arc', outline=outline, width=width)
    canvas.create_arc(x1, y2-2*radius, x1+2*radius, y2, start=180, extent=90, style='arc', outline=outline, width=width)
    canvas.create_line(x1+radius, y1, x2-radius, y1, fill=outline, width=width)
    canvas.create_line(x2, y1+radius, x2, y2-radius, fill=outline, width=width)
    canvas.create_line(x2-radius, y2, x1+radius, y2, fill=outline, width=width)
    canvas.create_line(x1, y2-radius, x1, y1+radius, fill=outline, width=width)

draw_rounded_rect(button_canvas, 5, 5, 135, 35, radius=12, outline="gray", width=0.25)
text = button_canvas.create_text(70, 20, text="Begin Installation", fill="white", font=("Segoe UI", 12))

def download_zip_to_temp():
    url = "https://github.com/Create-Lua/Cadmium_Refined/raw/refs/heads/main/BepInEx_win_x64_5.4.23.2.zip"
    temp_dir = tempfile.gettempdir()
    save_path = os.path.join(temp_dir, "BepInEx_win_x64_5.4.23.2.zip")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded to: {save_path}")
        return save_path
    except Exception as e:
        print(f"Download failed: {e}")
        return None

def extract_zip_to_folder(zip_path, target_folder):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_folder)
        print(f"Extracted to: {target_folder}")
        tk.messagebox.showinfo("Success", "The installation was successful")
        root.destroy()
    except Exception as e:
        print(f"Extraction failed: {e}")
        tk.messagebox.showerror("Error", f"Extraction failed: {e}")
    finally:
        try:
            os.remove(zip_path)
            print(f"Deleted zip: {zip_path}")
        except Exception as e:
            print(f"Could not delete zip: {e}")

def on_canvas_button_click(event):
    file_path = filedialog.askopenfilename(
        title="Select an EXE file",
        filetypes=[("Executable Files", "*.exe")],
        defaultextension=".exe"
    )
    if file_path:
        exe_folder = os.path.dirname(file_path)
        print(f"Selected EXE: {file_path}")
        zip_path = download_zip_to_temp()
        if zip_path:
            extract_zip_to_folder(zip_path, exe_folder)

button_canvas.tag_bind(text, "<Button-1>", on_canvas_button_click)

def start_move(event):
    root.x_offset = event.x
    root.y_offset = event.y

def move_window(event):
    win_width = root.winfo_width()
    bar_height = title_bar.winfo_height()
    new_x = event.x_root - win_width // 2
    new_y = event.y_root - bar_height // 2
    root.geometry(f'+{new_x}+{new_y}')

for widget in (title_bar, title_label, close_btn):
    widget.bind('<Button-1>', start_move)
    widget.bind('<B1-Motion>', move_window)

root.mainloop()
