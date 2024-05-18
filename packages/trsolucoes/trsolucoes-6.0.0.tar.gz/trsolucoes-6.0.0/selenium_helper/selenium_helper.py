from selenium.webdriver.chrome.webdriver import WebDriver 
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep


class SeleniumHelper():
    def wait_element(self, driver: WebDriver, locator:tuple, tag_filter: tuple = None, timeout: int = 30, delay_before: float = 0.3, delay_after: float = 0.3, return_element:bool = False, max_result:bool = False) -> bool | WebElement:
        sleep(delay_before)
        checked: bool = False
        element: WebElement
        try:
            if(locator[0] == By.TAG_NAME):
                elements = driver.find_elements(locator[0], locator[1])
                for el in elements:
                    if (el.get_attribute(tag_filter[0]) == tag_filter[1]):
                        element = el
                        if(max_result):
                            continue
                        else:
                            break
            else:
                element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
            if(element):
                checked = True
            else:
                checked = False
        except:
            checked = False
        sleep(delay_after)
        if(return_element):
            return element
        else:
            return checked

    def wait_and_send_keys(self, driver: WebDriver, locator: tuple, text: str, tag_filter: tuple = None, timeout: int = 30, delay_before: float = 0.3, delay_after: float = 0.3, clear_form: bool = True, click_before: bool = False, max_result:bool = False) -> None:
        sleep(delay_before)
        element: WebElement
        if(locator[0] == By.TAG_NAME):
            elements = driver.find_elements(locator[0], locator[1])
            for el in elements:
                if (el.get_attribute(tag_filter[0]) == tag_filter[1] and el.get_attribute("data-disabled") == None):
                    element = el
                    if max_result:
                        continue
                    else:
                        break
        else:
            element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        if(click_before):
            self.wait_and_click(driver, locator, tag_filter)
        if(clear_form):
            element.clear()
        element.send_keys(text)
        sleep(delay_after)

    def wait_and_click(self, driver: WebDriver, locator: tuple, tag_filter: tuple = None, timeout: int = 30, delay_before: float = 0.3, delay_after: float = 0.3) -> None:
        sleep(delay_before)
        element: WebElement
        if(locator[0] == By.TAG_NAME):
            elements = driver.find_elements(locator[0], locator[1])
            for el in elements:
                if (el.get_attribute(tag_filter[0]) == tag_filter[1]):
                    element = el
                    break
        else:
            element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()
        sleep(delay_after)

    def wait_and_select(self, driver: WebDriver, locator, text: str, timeout: int = 30, delay_before: float = 0.3, delay_after: float = 0.3) -> None:
        sleep(delay_before)
        element: WebElement = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        select_object = Select(element)
        select_object.select_by_visible_text(text)
        sleep(delay_after)

    def wait_and_click_in_text(self, driver: WebDriver, locator, text: str, delay_before: float = 0.3, delay_after: float = 0.3) -> None:
        sleep(delay_before)
        elements: list[WebElement] = driver.find_elements(locator[0], locator[1])
        for element in elements:
            if(text.lower() == element.text.lower()):
                element.click()
                break
        sleep(delay_after)

    def wait_and_hover(self, driver: WebDriver, locator, timeout: int = 30, delay_before: float = 0.3, delay_after: float = 0.3) -> None:
        sleep(delay_before)
        element: WebElement = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        sleep(delay_after)