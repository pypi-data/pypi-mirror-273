from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os, pickle
from io import open as io_open
from urllib.parse import urlparse
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ElementWrapper:
    def __init__(self, element):
        self.element = element

class ElementsWrapper:
    def __init__(self, elements):
        self.elements = elements

global driver1 
driver1 = ''

def driver(driver_path):
    try:
        global driver1
        driver1 = webdriver.Chrome(service=Service(driver_path))
        return driver1
    except Exception as e:
        print("An error occurred while initializing driver:", e)

def close():
    try:
        global driver1
        driver1.quit()
    except Exception as e:
        print("An error occurred while closing driver:", e)

def open(url):
    try:
        global driver1
        driver1.get(url)
    except Exception as e:
        print("An error occurred while opening URL:", e)

def find_element(by, value, time=0):
    try:
        locator = (by, value)
        wait = WebDriverWait(driver1, time)
        return ElementWrapper(wait.until(EC.presence_of_element_located(locator)))
    except TimeoutException:
        print("Timeout occurred while waiting for element.")
    except NoSuchElementException:
        print("Element not found.")

def find_elements(by, value, time=0):
    try:
        locator = (by, value)
        wait = WebDriverWait(driver1, time)
        return ElementWrapper(wait.until(EC.presence_of_all_elements_located(locator)))
        # return ElementsWrapper(driver1.find_elements(*locator))
    except Exception as e:
        print("An error occurred while finding elements:", e)

def id(value,  time=0):
    try:
        return find_element(By.ID, value, time).element
    except Exception as e:
        print("An error occurred while finding element by ID:", e)

def name(value,  time=0):
    try:
        return find_element(By.NAME, value, time).element
    except Exception as e:
        print("An error occurred while finding element by name:", e)

def xpath(value,  time=0):
    try:
        return find_element(By.XPATH, value, time).element
    except Exception as e:
        print("An error occurred while finding element by xpath:", e)

def link_text(value,  time=0):
    try:
        return find_element(By.LINK_TEXT, value, time).element
    except Exception as e:
        print("An error occurred while finding element by link text:", e)

def partial_link_text(value,  time=0):
    try:
        return find_element(By.PARTIAL_LINK_TEXT, value, time).element
    except Exception as e:
        print("An error occurred while finding element by partial link text:", e)

def tag_name(value,  time=0):
    try:
        return find_element(By.TAG_NAME, value, time).element
    except Exception as e:
        print("An error occurred while finding element by tag name:", e)
        
def class_name(value, time=0):
    try:
        return find_element(By.CLASS_NAME, value, time).element
    except Exception as e:
        print("An error occurred while finding element by class name:", e)

def css_selector(value,  time=0):
    try:
        return find_element(By.CSS_SELECTOR, value, time).element
    except Exception as e:
        print("An error occurred while finding element by CSS selector:", e)

def ids(value, time=0):
    try:
        return find_elements(By.ID, value, time).elements
    except Exception as e:
        print("An error occurred while finding elements by ID:", e)

def names(value, time=0):
    try:
        return find_elements(By.NAME, value, time).elements
    except Exception as e:
        print("An error occurred while finding elements by name:", e)

def xpaths(value, time=0):
    try:
        return find_elements(By.XPATH, value, time).elements
    except Exception as e:
        print("An error occurred while finding elements by xpath:", e)

def link_texts(value, time=0):
    try:
        return find_elements(By.LINK_TEXT, value, time).elements
    except Exception as e:
        print("An error occurred while finding elements by link text:", e)

def partial_link_texts(value, time=0):
    try:
        return find_elements(By.PARTIAL_LINK_TEXT, value, time).elements
    except Exception as e:
        print("An error occurred while finding elements by partial link text:", e)

def tag_names(value, time=0):
    try:
        return find_elements(By.TAG_NAME, value, time).elements
    except Exception as e:
        print("An error occurred while finding elements by tag name:", e)

def class_names(value, time=0):
    try:
        return find_elements(By.CLASS_NAME, value, time).elements
    except Exception as e:
        print("An error occurred while finding elements by class name:", e)

def css_selectors(value, time=0):
    try:
        return find_elements(By.CSS_SELECTOR, value, time).elements
    except Exception as e:
        print("An error occurred while finding elements by CSS selector:", e)

def browser_version():
    global driver1
    try:
        return driver1.capabilities['browserVersion']
    except Exception as e:
        print("Exception:", e)
        return ""
    
def window_position(x, y):
    global driver1
    try:
        driver1.set_window_position(x, y)
    except Exception as e:
        print("Exception:", e)

def window_size(width, height):
    global driver1
    try:
        driver1.set_window_size(width, height)
    except Exception as e:
        print("Exception:", e)

def screenshot(filename=None):
    global driver1
    try:
        if filename is None:
            filename = "screenshot.png"
        elif not os.path.isabs(filename):
            filename = os.path.join(os.getcwd(), filename)
        
        driver1.save_screenshot(filename)
        print("Screenshot saved at:", filename)
    except Exception as e:
        print("Exception:", e)
    
def save_cookies(filename=None):
    try:
        if filename is None:
            current_url = driver1.current_url
            parsed_url = urlparse(current_url)
            hostname = parsed_url.hostname
            if hostname:
                if hostname.startswith("www."):
                    hostname = hostname[4:]
                if "." in hostname:
                    hostname = hostname.split(".")[0]
                filename = hostname + ".pkl"
            else:
                filename = "cookies.pkl"

        if not os.path.isabs(filename):
            filename = os.path.join(os.getcwd(), filename)
        
        cookies = driver1.get_cookies()
        with io_open(filename, 'wb') as file:
            pickle.dump(cookies, file)
    except Exception as e:
        print("Exception:", e)

def delete_cookies():
    try:
        driver1.delete_all_cookies()
    except Exception as e:
        print("Exception:", e)

def set_cookies(filename):
    try:

        with io_open(filename, 'rb') as file:
            cookies = pickle.load(file)

        for cookie in cookies:
            driver1.add_cookie(cookie)
    except Exception as e:
        print("Exception:", e)

def switch_to_alert(action='accept'):
    try:
        alert = driver1.switch_to.alert
        if action == 'accept':
            alert.accept()
        elif action == 'cancel':
            alert.dismiss()
        elif action == 'text':
            return alert.text
        else:
            print("Invalid action specified.")
    except NoAlertPresentException:
        print("No alert present")
    except Exception as e:
        print("Exception:", e)

def switch_to_default():
    try:
        driver1.switch_to.default_content()
    except Exception as e:
        print("Exception:", e)

def switch_to_frame(frame):
    try:
        driver1.switch_to.frame(frame)
    except Exception as e:
        print("Exception:", e)

def switch_to_window(index_or_name):
    try:
        if isinstance(index_or_name, int):
            driver1.switch_to.window(driver1.window_handles[index_or_name])
        else:
            driver1.switch_to.window(index_or_name)
    except Exception as e:
        print("Exception:", e)

def new_window(url="about:blank"):
    try:
        driver1.execute_script("window.open(arguments[0], '_blank');", url)
    except Exception as e:
        print("Exception:", e)

def js(script):
    try:
        driver1.execute_script(script)
    except Exception as e:
        print("Exception:", e)

def refresh():
    try:
        driver1.refresh()
    except Exception as e:
        print("Exception:", e)

def forward():
    try:
        driver1.forward()
    except Exception as e:
        print("Exception:", e)

def back():
    try:
        driver1.back()
    except Exception as e:
        print("Exception:", e)



# def perform_actions(*actions):
#     global driver1
#     try:
#         action_chains = webdriver.ActionChains(driver1)
#         for action in actions:
#             action_chains = action_chains.perform(action)
#     except Exception as e:
#         print("Exception:", e)



__all__ = ['driver', 'open', 'close', 'id', 'name', 'xpath', 'link_text', 'partial_link_text', 'tag_name', 'class_name', 'css_selector', 
           'ids', 'names', 'xpaths', 'link_texts', 'partial_link_texts', 'tag_names', 'class_names', 'css_selectors', 'browser_version',
           'window_position', 'window_size', 'screenshot', 'save_cookies', 'delete_cookies', 'set_cookies', 'switch_to_alert', 'switch_to_default',
           'switch_to_frame', 'switch_to_window', 'new_window', 'js', 'refresh', 'back', 'forward']