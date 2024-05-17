import logging
from parsel import Selector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class BaseScraper:
    def initdriver(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox") # linux only
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(
            "--enable-features=NetworkService,NetworkServiceInProcess")

        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--ignore-certificate-errors')

        return webdriver.Chrome(options=chrome_options)

    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)
        self.driver = self.initdriver()

    def get_selector(self):
        """Gets a selector from current page source"""
        return Selector(text=self.driver.page_source)

    def get(self, url, title_text=None):
        """Get a webpage, optionally waiting for text in the title."""
        self.driver.get(url)
        if title_text is not None:
            WebDriverWait(self.driver, 100).until(
                    EC.title_contains(title_text))

    def click(self, xpath):
        """Clicks on an xpath"""
        try:
            el = self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            self.logger.info("NoSuchElement")
            el = None

        if el is not None:
            classes = el.get_attribute('class').split(' ')
            # only click if not already selected
            if 'selected' not in classes:
                # Convoluted way of clicking to avoid overlay problems
                ActionChains(self.driver).move_to_element(el).click().perform()
                #el.click()
            return True
            self.logger.info("already selected...")
        return False

    def csswait(self, selector, time=30):
        """Wait until CSS element located"""
        return WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def element_exists(self, by, tag):
        """Returns True if element exists by tag"""
        try:
            self.driver.find_element(by, tag)
            return True
        except NoSuchElementException:
            return False
        except Exception as e:
            self.logger.error(e)
            return False

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()
