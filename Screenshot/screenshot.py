import os
import pyautogui

def screenshot():
    save_path = os.path.join(os.path.expanduser("~"), "Pictures")
    shot = pyautogui.screenshot()
    shot.save(f"{save_path}\\python_screenshot.png")

    return print(f"\nScreenshot taken, and saved to {save_path}")

screenshot()