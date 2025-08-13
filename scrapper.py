import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import random
import time
import os

class Scrapper:
    def __init__(self):
        ua = UserAgent()
        options = uc.ChromeOptions()
        
        # Stealth configurations
        options.add_argument(f'--user-agent={ua.random}')
        options.add_argument('--no-first-run')
        options.add_argument('--disable-blink-features=AutomationControlled')
        #options.add_argument("--headless");
        
        # Random viewport size
        viewport_width = random.randint(1200, 1920)
        viewport_height = random.randint(800, 1080)
        options.add_argument(f'--window-size={viewport_width},{viewport_height}')
        
        # Initialize undetected Chrome
        self.driver = uc.Chrome(options=options)
        
        # Remove webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(f"Initialized stealth browser with viewport: {viewport_width}x{viewport_height}")


    def random_delay(self, min_seconds=1, max_seconds=5):
        """Human-like random delay"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    def safe_click(self, element):
        """Click element with human-like behavior"""
        self.random_delay(0.5, 1.5)
        self.driver.execute_script("arguments[0].scrollIntoView(0);", element)
        self.random_delay(0.3, 0.8)
        element.click()
        
    def safe_find_element(self, by, value, timeout=10):
        """Find element with wait and error handling"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located((by, value)))
        except Exception as e:
            print(f"Element not found: {by}={value}, Error: {e}")
            return None

    def screenshot(self, filename, element=None):
        """Take a screenshot of the current page"""
        filename = f"images/{filename}"
        self.random_delay(0.5, 1.5)
        if element:
            self.driver.execute_script(f"ScrollToDiv('{element}');")
            self.random_delay(0.5, 1.5)

        self.driver.save_screenshot(filename)
        return filename

       
    def scrap(self, query) -> str | None:
        raise NotImplementedError("This method should be overridden by subclasses")
