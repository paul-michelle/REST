import time
from typing import Any
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from auto_testing_settings import WEBDRIVER_PATH

MAX_WAIT = 1
SLEEP_TIME = 0.1


class BaseFunctionalTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        options = webdriver.ChromeOptions()
        options.headless = True
        self.browser = webdriver.Chrome(WEBDRIVER_PATH, options=options)

    def tearDown(self) -> None:
        self.browser.quit()

    @staticmethod
    def wait_for(fn) -> Any:
        start_time = time.time()
        while True:
            try:
                return fn()
            except (WebDriverException, AssertionError) as e:
                time_elapsed = time.time() - start_time
                if time_elapsed > MAX_WAIT:
                    raise e
                time.sleep(SLEEP_TIME)

    def send_info(self, info: str) -> None:
        post_form = self.browser.find_element(By.CLASS_NAME, 'form-horizontal')
        post_text_box = post_form.find_element(By.NAME, '_content')
        post_text_box.send_keys(info)
        post_button = post_form.find_element(By.CLASS_NAME, 'btn')
        post_button.send_keys(Keys.ENTER)

    def wait_and_assert_is_in_response(self, info: str) -> bool:
        return self.wait_for(
            lambda: self.assertIn(
                info, self.browser.find_element(By.CLASS_NAME, 'response-info').text
            )
        )
