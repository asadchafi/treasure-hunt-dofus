from seleniumwire import webdriver  # Use selenium-wire to intercept requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from typing import Optional


class TokenCapture:
    def __init__(self):
        # Setup Chrome options
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')  # Run in headless mode
        self.options.add_argument('--disable-gpu')  # Disable GPU acceleration
        self.options.add_argument('--no-sandbox')  # Bypass OS security model
        self.options.add_argument('--disable-dev-shm-usage')  # Overcome resource constraints in some systems
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.token: Optional[str] = None

    def get_token(self) -> Optional[str]:
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
            time.sleep(2)

            # Monitor network traffic to capture the token
            for request in driver.requests:
                if request.url.startswith("https://api.dofusdb.fr/treasure-hunt") and 'token' in request.headers:
                    self.token = request.headers['token']
                    print(f'Token found: {self.token}')
                    break

            # Check if the token was captured
            if not self.token:
                print("Token not found in network requests.")
                return None

            return self.token

        except TimeoutException as e:
            print(f'Error waiting for selector: {str(e)}')
            return None
        finally:
            # Clean up
            driver.quit()


# Example usage
if __name__ == "__main__":
    token_capture = TokenCapture()
    token = token_capture.get_token()
    if token:
        print(f"Captured Token: {token}")
    else:
        print("Failed to capture token.")
