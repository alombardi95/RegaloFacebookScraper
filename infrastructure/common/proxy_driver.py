import os
import pickle
import random
import tempfile
import time
from sys import platform
from typing import Optional
import shutil

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from webdriver_manager.chrome import ChromeDriverManager

from infrastructure.common.exceptions import ElementNotFoundError, PageNotLoadedError

import undetected_chromedriver as uc
from undetected_chromedriver import WebElement

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException

from retry import retry


class ProxyDriver:
    FOLDER_NAME = 'cookies'

    def __init__(self, timeout: int, browser: str, headless: bool, detached: bool):
        # shared variables
        self.base_url = None
        self.browser: str = browser
        self.driver: uc.Chrome = None
        self.driver_base_loc = os.path.join(os.getcwd(), 'driver')

        # setups
        self.setup_browser(browser, headless, detached)

        self.wait = WebDriverWait(self.driver, timeout)

    def is_page_loaded(self) -> bool:
        """
        Checks if page is loaded successfully
        """
        try:
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            return True
        except:
            return False

    @retry(exceptions=PageNotLoadedError, delay=5, tries=2)
    def goto(self, to_: str):
        self.get(to_)
        if not self.is_page_loaded():
            raise PageNotLoadedError

    def goto_home(self):
        self.get(self.base_url)

    def get(self, url):
        self.driver.get(url)

    def setup_browser(self, browser: str, headless: bool = False, detached: bool = False):
        # Firefox
        if browser.lower() == 'firefox':
            pass
        # Chrome
        else:
            chromedriver_path = ChromeDriverManager().install()
            self.temp_chrome_path = tempfile.mkdtemp()
            shutil.copy(chromedriver_path, self.temp_chrome_path)

            # Chrome Options
            options = uc.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            if detached:
                options.add_experimental_option("detach", True)
            options.add_argument("--disable-notifications")
            options.add_argument("--start-maximized")
            options.add_argument('--lang=en-US')
            # options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument("--log-level=3")

            options.add_argument(r"--user-data-dir=" + tempfile.mkdtemp())
            options.add_argument(r'--profile-directory=' + str(random.randint(1, 999999999)))
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0")

            if platform == 'linux' or platform == 'linux2':
                options.add_argument('--disable-dev-shm-usage')

            # current working directory/driver/chrome
            self.driver = uc.Chrome(options=options, driver_executable_path=os.path.join(self.temp_chrome_path, "chromedriver"))
            # self.driver = webdriver.Chrome(options=options)

    @property
    def actions(self) -> ActionChains:
        return ActionChains(self.driver)

    def click_element(self, xpath: str):
        self.driver.find_element(By.XPATH, xpath).click()

    @retry((ElementClickInterceptedException, StaleElementReferenceException), delay=5, tries=3)
    def wait_then_click(self, xpath: str, from_element: Optional[WebElement] = None):
        element: uc.WebElement | None = None

        if from_element:
            element = from_element.find_element(By.XPATH, xpath)
            self.actions \
                .move_to_element(element) \
                .click() \
                .perform()
        else:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.actions \
                .move_to_element(element) \
                .click() \
                .perform()

        return element

    def send_keys(self, xpath: str, text: str):
        self.driver.find_element(By.XPATH, xpath).send_keys(text)

    @retry((ElementClickInterceptedException, StaleElementReferenceException), delay=3, tries=3)
    def wait_send_keys(self, xpath: str, text: str):
        self.wait.until(EC.presence_of_element_located((By.XPATH, xpath))) \
            .send_keys(text)

    def wait_for(self, xpath: str, from_element: Optional[WebElement] = None) -> WebElement:
        if from_element:
            return from_element.find_element(By.XPATH, xpath)

        try:
            return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            return None

    def wait_for_many(self, xpath: str, from_element: Optional[WebElement] = None) -> WebElement:
        if from_element:
            return from_element.find_elements(By.XPATH, xpath)

        try:
            return self.driver.find_elements(By.XPATH, xpath)
        except TimeoutException:
            return None

    def wait_for_select(self, xpath: str, from_element: Optional[WebElement] = None):
        return Select(self.wait_for(xpath, from_element))

    def find_by_id(self, element_id: str):
        return self.driver.find_element(By.ID, element_id)

    def find_by_tag(self, element_tag: str, from_element: Optional[WebElement] = None):
        if from_element:
            return from_element.find_elements(By.TAG_NAME, element_tag)

        return self.driver.find_elements(By.TAG_NAME, element_tag)

    @retry(ElementNotFoundError, tries=2, delay=5)
    def find_accessible_name(self, main_xpath: str, accessible_name: str):
        elements = self.driver.find_elements(by=By.XPATH, value=main_xpath)
        for e in elements:
            if e.accessible_name == accessible_name:
                return e
        raise ElementNotFoundError

    def mouse_scroll(self, offset: int, xpath: str):
        self.driver.switch_to.window(self.driver.window_handles[0])

        element = self.driver.find_element(by=By.XPATH, value=xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        actions.send_keys(Keys.ARROW_DOWN).perform()
        print('scrolling...')

    def scroll_into_view(self, element) -> None:
        """
        Scrolls an element into view
        """
        self.driver.execute_script('arguments[0].scrollIntoView()', element)

    def get_element_children(self, element_xpath: str, children_xpath: str) -> list[WebElement]:
        parent = self.wait_for(element_xpath)
        return parent.find_elements(by=By.XPATH, value=children_xpath)

    def get_first_visible(self, xpath: str) -> WebElement:
        elements = self.driver.find_elements(by=By.XPATH, value=xpath)
        return next(iter([e for e in elements if ProxyDriver.__element_in_viewport(self.driver, e)]))

    def get_parent_button(self, element: uc.WebElement, run: int = 0, max_run: int = 10) -> uc.WebElement | None:
        if element.tag_name == 'button' or element.get_attribute('role') == 'button':
            return element

        if run > max_run:
            return None

        parent_element = element.find_element(by=By.XPATH, value='./..')

        return self.get_parent_button(parent_element, run + 1, max_run)

    # Funzione per salvare una sessione di Chrome
    def save_session(self, filename):
        # Salva la sessione di Chrome utilizzando la libreria pickle
        with open(os.path.join(self.FOLDER_NAME, filename), 'wb') as file:
            pickle.dump(self.driver.get_cookies(), file)

    # Funzione per caricare una sessione di Chrome salvata in precedenza
    def load_session(self, filename):
        try:
            # Carica la sessione di Chrome utilizzando la libreria pickle
            with open(os.path.join(self.FOLDER_NAME, filename), 'rb') as file:
                cookies = pickle.load(file)

            # Aggiunge i cookie salvati alla sessione di Chrome
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except:
            print('Not possible to load session.')

    @staticmethod
    def __element_in_viewport(driver, elem):
        elem_left_bound = elem.location.get('x')
        elem_top_bound = elem.location.get('y')
        elem_width = elem.size.get('width')
        elem_height = elem.size.get('height')
        elem_right_bound = elem_left_bound + elem_width
        elem_lower_bound = elem_top_bound + elem_height

        win_upper_bound = driver.execute_script('return window.pageYOffset')
        win_left_bound = driver.execute_script('return window.pageXOffset')
        win_width = driver.execute_script('return document.documentElement.clientWidth')
        win_height = driver.execute_script('return document.documentElement.clientHeight')
        win_right_bound = win_left_bound + win_width
        win_lower_bound = win_upper_bound + win_height

        return all((win_left_bound <= elem_left_bound,
                    win_right_bound >= elem_right_bound,
                    win_upper_bound <= elem_top_bound,
                    win_lower_bound >= elem_lower_bound)
                   )

    def paste_content(self, el, content):
        self.driver.execute_script(
            f'''
    const text = `{content}`;
    const dataTransfer = new DataTransfer();
    dataTransfer.setData('text', text);
    const event = new ClipboardEvent('paste', {{
      clipboardData: dataTransfer,
      bubbles: true
    }});
    arguments[0].dispatchEvent(event)
    ''',
            el)


if __name__ == '__main__':
    browser = webdriver.C()
    browser.get("https://en.wikipedia.org")
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
    browser.close()
