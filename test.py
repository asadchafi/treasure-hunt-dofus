import pyautogui
import time


def capture_and_extract_text(region):
    """
    Capture screenshot of a region and extract text using OCR.
    
    :param region: A tuple (x, y, width, height) defining the region to capture.
    :return: Extracted text from the screenshot.
    """
    # Take screenshot of the given region
    screenshot = pyautogui.screenshot(region=region)
    
    # Use pytesseract to extract text from the screenshot
    text = pytesseract.image_to_string(screenshot)
    
    return text

# List of all coordinates
coordinates = [
   {"x": 575, "y": 441},
  {"x": 655, "y": 480},
  {"x": 738, "y": 523},
  {"x": 817, "y": 562},
  {"x": 900, "y": 603},
  {"x": 981, "y": 643},
    {"x": 654, "y": 399},
  {"x": 734, "y": 438},
  {"x": 817, "y": 481},
  {"x": 896, "y": 520},
  {"x": 979, "y": 561},
  {"x": 1060, "y": 601},
    {"x": 733, "y": 357},
  {"x": 813, "y": 396},
  {"x": 896, "y": 439},
  {"x": 975, "y": 478},
  {"x": 1058, "y": 519},
  {"x": 1139, "y": 559},
  {"x": 812, "y": 315},
  {"x": 892, "y": 354},
  {"x": 975, "y": 397},
  {"x": 1054, "y": 436},
  {"x": 1137, "y": 477},
  {"x": 1218, "y": 517}
]


time.sleep(1)




for coord in coordinates:
    print(f"Clicking at: {coord['x']}, {coord['y']}")  # Debugging line
    time.sleep(4)
        # Move mouse and click at the specified coordinates
    pyautogui.click(coord['x'], coord['y'])
    time.sleep(1)
    break  # Remove this line to continue through all coordinates
