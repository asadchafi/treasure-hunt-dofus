import pyautogui

def print_mouse_position():
    # Get the current mouse position
    x, y = pyautogui.position()
    print(f"Mouse position: x={x}, y={y}")

# Call the function
print_mouse_position()