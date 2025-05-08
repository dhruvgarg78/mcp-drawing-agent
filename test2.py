# run_add_text_only.py

import time
from pywinauto.application import Application
from win32api import GetSystemMetrics
import win32gui
import win32con

# Ensure Paint is already open
paint_app = Application().connect(class_name='MSPaintApp')

def add_text_in_paint(text: str):
    try:
        paint_window = paint_app.window(class_name='MSPaintApp')
        print("[DEBUG] Paint window accessed.")

        if not paint_window.has_focus():
            print("[DEBUG] Paint not focused, setting focus...")
            paint_window.set_focus()
            time.sleep(0.5)

        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        print("[DEBUG] Canvas found.")

        # Try selecting the Text Tool via mouse click
        print("[DEBUG] Clicking on Text tool location.")
        paint_window.click_input(coords=(428, 111))  # Might need tweaking based on screen res
        time.sleep(0.5)

        # Select text tool using keyboard (optional backup)
        paint_window.type_keys('t')
        time.sleep(0.5)
        paint_window.type_keys('x')
        time.sleep(0.5)

        print("[DEBUG] Clicking canvas to activate text tool.")
        canvas.click_input(coords=(834, 409))  # Should be inside your rectangle
        time.sleep(0.5)
        
        # Click where to start typing
        canvas.click_input(coords=(834, 409))
        print(f"[DEBUG] Cursor placed at (x=817, y=450)")
        time.sleep(0.5)

        # Type the desired text
        paint_window.type_keys(text)
        print(f"[DEBUG] Typed text: {text}")
        time.sleep(0.5)

        # Click somewhere to exit text box
        canvas.click_input(coords=(1050, 800))
        print("[DEBUG] Clicked to exit text box.")

        print(f"[SUCCESS] Text '{text}' added successfully.")
    except Exception as e:
        print(f"[ERROR] {str(e)}")

if __name__ == "__main__":
    time.sleep(2)  # Give time to switch to Paint window
    add_text_in_paint("AUTOMATED SUCCESS")
