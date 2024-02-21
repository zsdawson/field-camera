import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
from datetime import datetime
import os
from PIL import Image, ImageTk

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 is the default camera

# Function to update the preview
def update_preview():
    ret, frame = cap.read()
    if ret:
        # Resize frame to 50%
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        preview_label.imgtk = imgtk
        preview_label.configure(image=imgtk)
    preview_label.after(10, update_preview)

# Function to take a picture
def take_picture():
    ret, frame = cap.read()
    if ret:
        filename = filename_entry.get()
        if not filename:
            filename = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename += '.jpg'
        cv2.imwrite(filename, frame)
        messagebox.showinfo("Success", "Picture taken successfully!")

        # Save to a specified location
        save_path = filedialog.askdirectory(initialdir='/Volumes')
        if save_path:
            os.rename(filename, os.path.join(save_path, filename))
            messagebox.showinfo("Saved", f"Image saved to {save_path}")
    else:
        messagebox.showerror("Error", "Failed to capture the image")

# Function to exit the program
def exit_program():
    cap.release()
    root.destroy()

# Setting up the GUI
root = tk.Tk()
root.title("Mac Camera App")

# Preview Label
preview_label = tk.Label(root)
preview_label.pack()

# Filename Entry
filename_label = tk.Label(root, text="Enter Filename:")
filename_label.pack()
filename_entry = tk.Entry(root, width=20)
filename_entry.pack()

# Take Picture Button
take_picture_btn = tk.Button(root, text="Take Picture", command=take_picture, width=20, height=3)
take_picture_btn.pack()

# Exit Button
exit_btn = tk.Button(root, text="Exit", command=exit_program, width=20, height=3)
exit_btn.pack()

# Start the preview
update_preview()

# Run the application
root.mainloop()
