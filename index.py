import os
import random
import requests
from PIL import Image, ImageTk, ImageSequence
import tkinter as tk
import threading
import ctypes
import time

# Configuration
IMAGE_URLS = [
    "https://files.roxcelic.love/funny/image.webp",
]

REACTION_URLS = [
    "https://files.roxcelic.love/funny/item1.gif",
    "https://files.roxcelic.love/funny/item2.gif",
    "https://files.roxcelic.love/funny/item3.gif"
]
LOCAL_VERSION = "1.0.4"
BASE_URL = "https://files.roxcelic.love/funny/"
VERSION_URL = f"{BASE_URL}version.txt"
EXE_URL = f"{BASE_URL}funny.exe"
IMAGE_DIR = os.path.expanduser("~/Documents/funny")

# Define RECT structure for working area calculation
class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long)
    ]

def get_working_area():
    """Get the working area of the screen."""
    user32 = ctypes.windll.user32
    work_area = RECT()
    user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(work_area), 0)
    return work_area

def show_update_window(local_version, online_version):
    """Show a Tkinter window notifying the user about an update."""
    update_window = tk.Tk()
    update_window.title("Update Required")
    update_window.configure(bg="black")
    
    message = (f"Your version is {local_version}. The newest version is {online_version}. "
               f"Please update by downloading {EXE_URL}")
    
    label = tk.Label(update_window, text=message, bg="black", fg="white", font=("Courier New", 12), wraplength=500)
    label.pack(expand=True, fill=tk.BOTH)
    
    update_window.geometry("600x300")
    update_window.protocol("WM_DELETE_WINDOW", update_window.destroy)
    update_window.mainloop()

def check_for_updates():
    """Check for updates and show the update window if needed."""
    try:
        response = requests.get(VERSION_URL)
        response.raise_for_status()
        latest_version = response.text.strip()
        
        if latest_version > LOCAL_VERSION:
            update_thread = threading.Thread(target=show_update_window, args=(LOCAL_VERSION, latest_version), daemon=True)
            update_thread.start()
    except requests.RequestException as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def download_file(url, path):
    """Download a file from a URL to a specified path."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.RequestException as e:
        print(f"Error downloading file {url}: {e}")

def ensure_images():
    """Ensure all images and GIFs are downloaded."""
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    
    all_urls = IMAGE_URLS + REACTION_URLS
    for url in all_urls:
        filename = os.path.basename(url)
        path = os.path.join(IMAGE_DIR, filename)
        download_file(url, path)

def get_gif_frames(gif_path):
    """Extract frames from a GIF and calculate the total duration."""
    frames = []
    durations = []
    try:
        with Image.open(gif_path) as gif:
            for frame in ImageSequence.Iterator(gif):
                frame = frame.convert("RGBA")
                frame.thumbnail((100, 100), Image.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame))
                durations.append(frame.info.get('duration', 100))
    except IOError as e:
        print(f"Error processing GIF {gif_path}: {e}")
    return frames, sum(durations)

def load_image(image_file):
    """Load and resize an image."""
    try:
        with Image.open(image_file) as img:
            img.thumbnail((100, 100), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
    except IOError as e:
        print(f"Error loading image {image_file}: {e}")
        return None

def show_image():
    """Display images and handle GIF switching."""
    root = tk.Tk()
    root.overrideredirect(True)

    # Prepare reaction images and GIFs
    reaction_files = [os.path.join(IMAGE_DIR, os.path.basename(url)) for url in REACTION_URLS]
    gif_files = [file for file in reaction_files if file.endswith('.gif')]
    static_files = [file for file in reaction_files if not file.endswith('.gif')]

    gif_frames_list = []
    gif_durations_list = []
    for gif_file in gif_files:
        frames, total_duration = get_gif_frames(gif_file)
        gif_frames_list.append(frames)
        gif_durations_list.append(total_duration)

    default_image_file = os.path.join(IMAGE_DIR, os.path.basename(random.choice(IMAGE_URLS)))
    img = load_image(default_image_file)

    if img is None:
        print("Failed to load default image.")
        return

    label = tk.Label(root, image=img)
    label.pack()

    # Ensure window is above the taskbar
    work_area = get_working_area()
    x_options = [0, work_area.right - 100]
    y_options = [0, work_area.bottom - 100]
    x = random.choice(x_options)
    y = random.choice(y_options)
    
    root.geometry(f"+{x}+{y}")
    root.attributes("-topmost", True)

    def switch_images():
        """Switch between images and GIFs periodically."""
        while True:
            time.sleep(5)

            # Switch to a random reaction GIF
            if gif_frames_list:
                gif_frames = random.choice(gif_frames_list)
                gif_duration = gif_durations_list[gif_frames_list.index(gif_frames)]
                for frame in gif_frames:
                    label.config(image=frame)
                    root.update_idletasks()
                    time.sleep(0.1)
                time.sleep(gif_duration / 1000)

            # Switch to a random static image
            default_image_file = os.path.join(IMAGE_DIR, os.path.basename(random.choice(IMAGE_URLS)))
            img = load_image(default_image_file)
            if img is None:
                print("Failed to load new image.")
                return
            label.config(image=img)
            root.update_idletasks()
            
            time.sleep(5)

    threading.Thread(target=switch_images, daemon=True).start()
    root.mainloop()

# Ensure all images and GIFs are downloaded
ensure_images()

# Start the update check in a separate thread
update_thread = threading.Thread(target=check_for_updates, daemon=True)
update_thread.start()

# Run the image display function
show_image()
