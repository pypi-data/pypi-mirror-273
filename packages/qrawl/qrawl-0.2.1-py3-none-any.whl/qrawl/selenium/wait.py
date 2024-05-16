from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable,
    presence_of_element_located,
    presence_of_all_elements_located,
)
from selenium.webdriver.support.ui import WebDriverWait


class QSeleniumWait:
    """
    QSeleniumWait is an extension of wait-related functions for QSelenium.

    Args:
        driver (WebDriver): The WebDriver instance.
        timeout_default (int): The default timeout value. Defaults to 10.
    """

    def __init__(self, driver: WebDriver, timeout_default: int = 10):
        self._dr = driver
        self._timeout_default = timeout_default

    def wait_for(self, condition, timeout=None):
        if timeout is None:
            timeout = self._timeout_default

        return WebDriverWait(self._dr, timeout).until(condition)

    # * WAIT FOR SINGLE ELEMENT TO BE PRESENT

    def wait_for_element(self, locator: tuple, timeout=None):
        if timeout is None:
            timeout = self._timeout_default

        condition = presence_of_element_located(locator)

        return self.wait_for(condition, timeout)

    def wait_for_xpath(self, xpath: str, timeout=None):
        if timeout is None:
            timeout = self._timeout_default

        return self.wait_for_element((By.XPATH, xpath), timeout)

    # * WAIT FOR ALL ELEMENTS TO BE PRESENT

    def wait_for_all_elements(self, locator: tuple, timeout=None):
        if timeout is None:
            timeout = self._timeout_default

        condition = presence_of_all_elements_located(locator)

        return WebDriverWait(self._dr, timeout).until(condition)

    # * WAIT FOR ELEMENT TO BE CLICKABLE

    def wait_for_element_clickable(self, locator: tuple, timeout=None):
        if timeout is None:
            timeout = self._timeout_default

        condition = element_to_be_clickable(locator)

        return self.wait_for(condition, timeout)

    def wait_for_xpath_clickable(self, xpath: str, timeout=None):
        if timeout is None:
            timeout = self._timeout_default

        return self.wait_for_element_clickable((By.XPATH, xpath), timeout)

    # * WAIT FOR ELEMENT TO HAVE TEXT

    def wait_for_text(self, locator: tuple, timeout=None):
        if timeout is None:
            timeout = self._timeout_default

        def condition():
            return self._dr.find_element(*locator).text.strip() != ""

        WebDriverWait(self._dr, timeout).until(condition)

        return self._dr.find_element(*locator)

    def wait_for_xpath_text(self, xpath: str, timeout=None):
        if timeout is None:
            timeout = self._timeout_default

        return self.wait_for_text((By.XPATH, xpath), timeout)
