import sys
import time
import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit
from PyQt5 import QtCore
from PyQt5.QtGui import QClipboard
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
from typing import Optional

class TreasureHuntAutomation:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.token: Optional[str] = None

    def capture_token(self):
        if self.token:
            return self.token  # Return the stored token if already captured
        
        try:
            driver = webdriver.Chrome(options=self.options)
            driver.get('https://dofusdb.fr/en/tools/treasure-hunt')
            
            x_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="X"]'))
            )
            x_input.clear()
            x_input.send_keys('-6')
            
            y_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Y"]'))
            )
            y_input.clear()
            y_input.send_keys('-7')
            
            arrow_icon = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.treasure-hunt-direction-icon.fa-arrow-right'))
            )
            arrow_icon.click()
            time.sleep(1)

            for request in driver.requests:
                if request.url.startswith("https://api.dofusdb.fr/treasure-hunt") and 'token' in request.headers:
                    self.token = request.headers['token']
                    break

            if not self.token:
                raise TimeoutError("Token not found in network requests.")
        except TimeoutException as e:
            print(f'Error waiting for selector: {str(e)}')
        except TimeoutError as e:
            print(f'Error: {str(e)}')
        finally:
            driver.quit()

        return self.token

    def make_request(self, x, y, direction):
        if not self.token:
            print("No token available")
            return []

        url = f'https://api.dofusdb.fr/treasure-hunt?x={x}&y={y}&direction={direction}&$limit=100&lang=fr'
        
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Origin': 'https://dofusdb.fr',
            'Referer': 'https://dofusdb.fr/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'token': self.token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                response_json = response.json()
                return self.extract_pois_from_json(response_json)
            else:
                print(f'Error: Received status code {response.status_code}')
                print(response.text)
        except requests.RequestException as e:
            print(f'Error sending GET request: {str(e)}')
            return []

    def extract_pois_from_json(self, response_json):
        pois_data = []
        for item in response_json['data']:
            posX = item['posX']
            posY = item['posY']
            for pos in item.get('pois', []):
                fr_name = pos['name'].get('fr', '')
                if fr_name:
                    pois_data.append({
                        'name': fr_name,
                        'posX': posX,
                        'posY': posY
                    })
        return pois_data

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Treasure Hunt UI')
        self.setGeometry(100, 100, 300, 600)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        self.main_layout = QVBoxLayout()

        # Create a horizontal layout for X and Y input fields
        coordinates_layout = QHBoxLayout()

        # Create input fields for X and Y coordinates
        self.x_input = QLineEdit(self)
        self.y_input = QLineEdit(self)

        # Set placeholder text for the input fields
        self.x_input.setPlaceholderText('Enter X coordinate')
        self.y_input.setPlaceholderText('Enter Y coordinate')

        # Add input fields next to each other in the layout
        coordinates_layout.addWidget(self.x_input)
        coordinates_layout.addWidget(self.y_input)

        # Add the coordinates layout to the main layout
        self.main_layout.addLayout(coordinates_layout)

        button_box = QVBoxLayout()

        top_button = QPushButton('Top', self)
        right_button = QPushButton('Right', self)
        bottom_button = QPushButton('Bottom', self)
        left_button = QPushButton('Left', self)

        self.list_widget = QListWidget(self)

        top_row = QHBoxLayout()
        bottom_row = QHBoxLayout()

        top_row.addWidget(top_button)
        top_row.addWidget(right_button)

        bottom_row.addWidget(bottom_button)
        bottom_row.addWidget(left_button)

        button_box.addLayout(top_row)
        button_box.addLayout(bottom_row)

        self.main_layout.addLayout(button_box)
        self.main_layout.addWidget(self.list_widget)

        self.setLayout(self.main_layout)

        self.automation = TreasureHuntAutomation()

        # Connect buttons to the direction function
        top_button.clicked.connect(lambda: self.on_direction_button_clicked(6))
        right_button.clicked.connect(lambda: self.on_direction_button_clicked(0))
        bottom_button.clicked.connect(lambda: self.on_direction_button_clicked(2))
        left_button.clicked.connect(lambda: self.on_direction_button_clicked(4))

        self.list_widget.itemClicked.connect(self.on_list_item_clicked)

        # Fetch the auth token as soon as the app starts
        self.automation.capture_token()

    def on_direction_button_clicked(self, direction):
        # Get the coordinates from the input fields
        x = self.x_input.text()
        y = self.y_input.text()

        # Validate input
        if not x or not y:
            print("Please enter both X and Y coordinates.")
            return

        # Make the request based on the direction and coordinates
        pois = self.automation.make_request(x, y, direction)
        self.update_pois(pois)

    def update_pois(self, pois):
        self.list_widget.clear()

        # Sort POIs alphabetically by name (the entire string)
        sorted_pois = sorted(pois, key=lambda poi: poi['name'])

        if sorted_pois:
            # Adding names and coordinates to the list for display
            for poi in sorted_pois:
                self.list_widget.addItem(f"{poi['name']} : ({poi['posX']}, {poi['posY']})")
        else:
            self.list_widget.addItem("No POIs found")

    def on_list_item_clicked(self, item):
        selected_text = item.text()
        # Extract X and Y from the selected item text
        parts = selected_text.split(" : (")
        if len(parts) == 2:
            name_part, coords_part = parts
            coords_part = coords_part.rstrip(")")
            posX, posY = coords_part.split(", ")
            # Set the coordinates in the input fields
            self.x_input.setText(posX)
            self.y_input.setText(posY)

            # Create the '/travel x y' command
            travel_command = f"/travel {posX} {posY}"

            # Copy the command to the clipboard immediately
            clipboard = QApplication.clipboard()
            clipboard.setText(travel_command)
            print(f"Copied to clipboard: {travel_command}")

            # Wait 200ms
            time.sleep(0.2)

            # Hardcoded position for clicking (replace with actual position)
             
            pyautogui.moveTo(100, 150)  # Move the mouse to a specific location
            pyautogui.click()  # Click on (100, 200) screen coordinates
    
            time.sleep(0.2)

            # Press space
            pyautogui.press('space')
            time.sleep(0.2)

            # Paste clipboard content
            pyautogui.hotkey('command', 'v')
            time.sleep(0.2)

            # Press enter twice
            pyautogui.press('enter')
            time.sleep(0.2)
            pyautogui.press('enter')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
