import time
from pywinauto.application import Application
from win32gui import FindWindow, ShowWindow, SetForegroundWindow
from win32con import SW_MAXIMIZE
from win32api import GetSystemMetrics
from pywinauto.findwindows import find_window
from pywinauto import mouse

# Constants: rectangle coordinates (modify as needed)
x1, y1 = 780, 380
x2, y2 = 1140, 700

def debug_draw_rectangle():
    try:
        print("🔍 Searching for Paint window...")
        hwnd = FindWindow("MSPaintApp", None)
        if not hwnd:
            print("❌ Paint window not found. Make sure Paint is open.")
            return

        # Maximize and bring to front
        print("📌 Maximizing Paint window and setting focus...")
        ShowWindow(hwnd, SW_MAXIMIZE)
        SetForegroundWindow(hwnd)
        time.sleep(1)

        print("✅ Paint window focused.")

        print(f"🧮 Rectangle coordinates:\n  From: ({x1}, {y1})\n  To:   ({x2}, {y2})")

        print("📍 Clicking Rectangle tool (approximate coords — adjust if needed)...")
        mouse.move(coords=(658, 106))
        time.sleep(0.5)
        mouse.click(button='left', coords=(658, 106))
        time.sleep(0.5)
        mouse.click(button='left', coords=(658, 106))

        print("🖱️ Clicking canvas to activate draw mode...")
        mouse.click(button='left', coords=(800, 400))
        time.sleep(0.3)

        print("✏️ Drawing rectangle...")
        mouse.move(coords=(x1, y1))
        print("🔄 Pressing and holding left mouse button... at:", x1, y1)
        mouse.press(button='left', coords=(x1, y1))
        time.sleep(0.3)
        mouse.move(coords=(x2, y2))
        time.sleep(0.3)
        mouse.release(button='left', coords=(x2, y2))

        print("✅ Rectangle drawn.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Running test for draw_rectangle()")
    debug_draw_rectangle()
