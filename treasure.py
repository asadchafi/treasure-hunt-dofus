from seleniumwire import webdriver  # Use selenium-wire to intercept requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import requests
from typing import Optional

class TreasureHuntAutomation:
    def __init__(self):
        # Setup Chrome options
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')  # Run in headless mode
        self.options.add_argument('--disable-gpu')  # Disable GPU acceleration
        self.options.add_argument('--no-sandbox')  # Bypass OS security model
        self.options.add_argument('--disable-dev-shm-usage')  # Overcome resource constraints in some systems
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.token: Optional[str] = None

    def run(self):
        try:
            # Initialize the driver
            driver = webdriver.Chrome(options=self.options)
            
            print('Running tests in headless mode...')
            
            # Navigate to the page
            driver.get('https://dofusdb.fr/en/tools/treasure-hunt')
            
            # Wait for and set X coordinate
            x_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="X"]'))
            )
            x_input.clear()
            x_input.send_keys('-6')
            
            # Wait for and set Y coordinate
            y_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Y"]'))
            )
            y_input.clear()
            y_input.send_keys('-7')
            
            print('Coordinates for X and Y have been set.')
            
            # Click the arrow icon
            arrow_icon = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.treasure-hunt-direction-icon.fa-arrow-right'))
            )
            arrow_icon.click()
            print('Arrow icon clicked.')
            
            # Small delay to ensure network requests are captured
            time.sleep(1)

            # Monitor network traffic to capture the token
            for request in driver.requests:
                if request.url.startswith("https://api.dofusdb.fr/treasure-hunt") and 'token' in request.headers:
                    self.token = request.headers['token']
                    print(f'Token found: {self.token}')
                    break

            # Check if the token was captured
            if not self.token:
                raise TimeoutError("Token not found in network requests.")

            # Make API request with token
            x = '-6'
            y = '-7'
            direction = 'right'
            url = 'https://dofus-map.com/huntTool/getData.php?x='+x+'&y='+y+'&direction='+direction+'&world=0&language=en'
            headers = {'Authorization': f'Bearer {self.token}'}
            
            response = requests.get(url, headers=headers)
            print('Response from API:', response.json())

        except TimeoutException as e:
            print(f'Error waiting for selector: {str(e)}')
        except TimeoutError as e:
            print(f'Error: {str(e)}')
        except requests.RequestException as e:
            print(f'Error sending GET request: {str(e)}')
        finally:
            # Clean up
            driver.quit()

if __name__ == "__main__":
    automation = TreasureHuntAutomation()
    automation.run()
