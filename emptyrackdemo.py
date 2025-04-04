import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from roboflow import Roboflow
import webbrowser
import os

# Initialize Roboflow model
rf = Roboflow(api_key="5VOF2OcYifmOkClliopV")
project = rf.workspace().project("empty-spaces-detection-in-shelf-data")
model = project.version(2).model

# Class for empty shelf detection
OUT_OF_STOCK_CLASS = "empty_space"

def play_intro_video(video_path):
    print("📼 Playing intro video from:", video_path)
    if not os.path.exists(video_path):
        print("❌ Video file does not exist!")
        return
    try:
        os.startfile(video_path)
    except Exception as e:
        print("❌ Could not play video:", e)

def show_popup():
    popup_path = os.path.abspath("popup.html")
    print(f"🌐 Attempting to open popup at: {popup_path}")
    if os.path.exists(popup_path):
        webbrowser.open_new_tab('file://' + popup_path.replace('\\', '/'))
    else:
        print("❌ popup.html not found.")

def process_default_image(default_path):
    if not os.path.exists(default_path):
        print("❌ Default image not found.")
        return

    image = Image.open(default_path)
    draw = ImageDraw.Draw(image)

    try:
        result = model.predict(default_path, confidence=40, overlap=30).json()
        print("✅ Detection results:", result)
    except Exception as e:
        print("❌ Detection failed:", e)
        result = {'predictions': []}  # fallback

    for prediction in result['predictions']:
        class_name = prediction['class']
        x, y, width, height = prediction['x'], prediction['y'], prediction['width'], prediction['height']
        left, top, right, bottom = x - width / 2, y - height / 2, x + width / 2, y + height / 2

        draw.rectangle([left, top, right, bottom], outline="red", width=2)
        draw.text((left, top - 10), f"{class_name} {prediction['confidence']:.2f}", fill="red")

    image.thumbnail((800, 800))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

    # ✅ Always open popup
    show_popup()

# GUI
root = tk.Tk()
root.title("📦 Empty Shelf Detection")

# Intro video
video_file = "rackspace for empty.mp4"
play_intro_video(video_file)

# Image label setup
image_label = tk.Label(root)
image_label.pack(pady=10)

# Process the default image
default_image_path = "rackspace 1.jpg"
process_default_image(default_image_path)

root.mainloop()
