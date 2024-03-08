import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
from PIL import Image, ImageTk
import os
from datetime import datetime

class CameraApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Raspberry Pi Camera App")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")  # A more modern theme than the default

        # Image preview frame
        self.preview_frame = ttk.Frame(self, width=640, height=480)  # Adjust size as needed
        self.preview_frame.pack(padx=10, pady=10)

        # Placeholder for the image preview
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.pack()

        # Controls frame
        self.controls_frame = ttk.Frame(self)
        self.controls_frame.pack(fill=tk.X, padx=10, pady=5)

        # Filename entry
        self.filename_var = tk.StringVar()
        self.filename_entry = ttk.Entry(self.controls_frame, textvariable=self.filename_var, width=50)
        self.filename_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.filename_entry.focus()

        # Take Picture button
        self.take_picture_btn = ttk.Button(self.controls_frame, text="Take Picture", command=self.take_picture)
        self.take_picture_btn.pack(side=tk.LEFT, padx=5)

        # Refresh Camera button
        self.refresh_btn = ttk.Button(self.controls_frame, text="Refresh Camera", command=self.refresh_camera)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)

        # Quit button
        self.quit_btn = ttk.Button(self.controls_frame, text="Quit", command=self.quit_program)
        self.quit_btn.pack(side=tk.LEFT, padx=5)

        self.geometry("800x600")  # Adjust the main window size

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
        # Open the image file
        img = Image.open(image_path)
        img.thumbnail((640, 480), Image.ANTIALIAS)  # Resize to fit the frame
        photo = ImageTk.PhotoImage(img)

        # Update the preview label
        self.preview_label.configure(image=photo)
        self.preview_label.image = photo  # Keep a reference!

    def refresh_camera(self):
        # This method could restart the camera service or refresh the UI
        # Currently just a placeholder
        messagebox.showinfo("Info", "Refreshed camera settings (placeholder).")

    def quit_program(self):
        self.destroy()

if __name__ == "__main__":
    app = CameraApp()
    app.mainloop()
