import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import subprocess
from PIL import Image, ImageTk
import os
from datetime import datetime

class CameraApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Raspberry Pi Camera App")
        self.attributes("-fullscreen", True)  # Set window to fullscreen
        
        # Bind the Escape key to the quit_program method
        self.bind("<Escape>", lambda event=None: self.quit_program())

        # Configure style
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Configure layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Custom font
        custom_font = font.Font(size=int(font.nametofont("TkDefaultFont").cget("size") * 1.9))  # 190% of the default font size

        # Controls frame (at the bottom)
        self.controls_frame = ttk.Frame(self)
        self.controls_frame.grid(row=2, column=0, sticky="ew")
        self.controls_frame.grid_columnconfigure(0, weight=1)

        # Filename entry
        self.filename_var = tk.StringVar()
        self.filename_entry = ttk.Entry(self.controls_frame, textvariable=self.filename_var, font=custom_font)
        self.filename_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.filename_entry.focus()

        # Take Picture button
        self.take_picture_btn = ttk.Button(self.controls_frame, text="Take Picture", command=self.take_picture, style="Large.TButton")
        self.take_picture_btn.grid(row=0, column=1, padx=10, pady=10)

        # Quit button
        self.quit_btn = ttk.Button(self.controls_frame, text="Quit", command=self.quit_program, style="Large.TButton")
        self.quit_btn.grid(row=0, column=2, padx=10, pady=10)

        # Apply custom font to buttons
        self.style.configure("Large.TButton", font=custom_font)

        # Image preview label (occupies most of the window)
        self.preview_label = ttk.Label(self)
        self.preview_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.preview_frame = ttk.Frame(self.preview_label)  # Container frame for the label, if needed

    def take_picture(self):
        filename = self.filename_var.get().strip() or datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        save_path = os.path.expanduser(f'~/{filename}.jpg')
        command = ['libcamera-still', '-o', save_path]

        try:
            subprocess.run(command, check=True)
            self.update_preview(save_path)
            messagebox.showinfo("Success", f"Picture taken successfully and saved to {save_path}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to capture the image: {e}")

    def update_preview(self, image_path):
        img = Image.open(image_path)
        # Resize the image to fill the screen while maintaining aspect ratio
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight() - self.controls_frame.winfo_height()  # Adjust for control frame height
        img.thumbnail((screen_width, screen_height), Image.ANTIALIAS)
        
        photo = ImageTk.PhotoImage(img)
        self.preview_label.configure(image=photo)
        self.preview_label.image = photo  # Keep a reference!

    def quit_program(self):
        self.destroy()

if __name__ == "__main__":
    app = CameraApp()
    app.mainloop()
