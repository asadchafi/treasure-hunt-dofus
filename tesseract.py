import pyautogui
from PIL import Image
import pytesseract

def screenshot_and_extract_text():
    print("Move your mouse to the top-left corner of the area and press Enter.")
    input("Press Enter to set the first corner...")
    x1, y1 = pyautogui.position()  # First corner

    print("Move your mouse to the bottom-right corner of the area and press Enter.")
    input("Press Enter to set the second corner...")
    x2, y2 = pyautogui.position()  # Second corner

    # Calculate the region dimensions
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    print("Capturing screenshot...")
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save("captured_area.png")  # Optional: Save the screenshot for reference

    # Perform OCR using Tesseract
    print("Extracting text from the screenshot...")
    extracted_text = pytesseract.image_to_string(screenshot)
    print("\nExtracted Text:")
    print(extracted_text)

# Run the function
screenshot_and_extract_text()
