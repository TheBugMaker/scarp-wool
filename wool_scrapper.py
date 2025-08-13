import traceback

from scrapper import Scrapper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

WOOLPLATZ_URL = "https://www.wollplatz.de"

PRODUCT_CSS_SELECTOR = ".sqr-resultItem .innerproductlist a"
COOKIE_DIALOG_CSS_SELECTOR = "#CookieInfoDialogDecline"


class WoolScrapper(Scrapper):
    def __init__(self):
        super().__init__()

    def _search_query(self, query):
        return f"/#sqr:(q[{query}])"

    def search_product(self, product_name):
        """Navigate to product search with stealth improvements"""
        search_url = WOOLPLATZ_URL + self._search_query(product_name)
        print(f"Navigating to: {search_url}")
        
        # Add random delay before navigation
        self.random_delay(1, 2)
        
        self.driver.get(search_url)
        
        # Wait for page to load properly
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            print("Page load timeout, continuing anyway")

    def go_product_page(self):
        """Navigate to first product page using native Selenium"""
        try:
            # Wait for products to load
            try:
                wait = WebDriverWait(self.driver, 10)
                accept_cookie = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, COOKIE_DIALOG_CSS_SELECTOR)))
                
                if accept_cookie:
                    print("Accepting cookie dialog")
                    self.safe_click(accept_cookie[0])

            except TimeoutException:
                print("No cookie dialog found")
                
            products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, PRODUCT_CSS_SELECTOR)))
            
            if products:
                first_product = products[0]
                print(f"Clicked on product: {first_product.get_attribute('href')}")
                self.safe_click(first_product)
                return True
            else:
                print("No products found")
                return False
                
        except (TimeoutException, NoSuchElementException) as e:
            traceback.print_exc()
            print(f"Failed to find product elements: {e}")
            return False


    def scrap(self, query) -> list[str] | None:
        """Main scraping method"""
        print(f"Starting to scrape for: {query}")
        
        # Navigate to search
        self.search_product(query)
        
        # Human-like delay instead of fixed 5 seconds
        self.random_delay(2, 6)
        
        # Navigate to product page
        success = self.go_product_page()
        
        if success:
            print("Successfully navigated to product page")
            # Additional delay before next action
            images = [
                self.screenshot(f"{query}_product_page.png"),
                self.screenshot(
                    f"{query}_specs.png",
                    ".pdetail-detailholder" 
                )
            ]

            return images
        else:
            print("Failed to navigate to product page")
