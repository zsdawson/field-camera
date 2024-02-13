
import tkinter as tk
from tkinter import messagebox
from gpiozero import Button
from picamera import PiCamera
from datetime import datetime
import os

# Set up the camera
camera = PiCamera()

# Set up GPIO buttons
take_picture_button = Button(2)  # Assuming the button is connected to GPIO pin 2
exit_button = Button(3)  # Assuming the button is connected to GPIO pin 3

# Function to take a picture
def take_picture():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'/media/usb/{timestamp}.jpg'
    camera.capture(filename)
    messagebox.showinfo("Success", "Picture taken successfully!")
    return filename

# Function to update the image on the GUI
def update_image():
    file_path = take_picture()
    photo = tk.PhotoImage(file=file_path)
    image_label.config(image=photo)
    image_label.image = photo

# Function to exit the program
def exit_program():
    root.destroy()

# Setting up the GUI
root = tk.Tk()
root.title("Raspberry Pi Camera")

take_picture_btn = tk.Button(root, text="Take Picture", command=update_image)
take_picture_btn.pack()

image_label = tk.Label(root)
image_label.pack()

exit_btn = tk.Button(root, text="Exit", command=exit_program)
exit_btn.pack()

# Loop to check button press
def check_button():
    if take_picture_button.is_pressed:
        update_image()
    if exit_button.is_pressed:
        exit_program()
    root.after(100, check_button)

check_button()

# Run the application
root.mainloop()
