import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def terDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_latter(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        inputbox.send_keys('Learn Python')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Learn Python')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Talk with wife')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Learn Python')
        self.wait_for_row_in_list_table('1: Learn Python')
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Learn Python', [row.text for row in rows])
        self.assertIn('2: Talk with wife', [row.text for row in rows])

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Learn Python')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Learn Python')
        first_list_url = self.browser.current_url

        self.assertRegex(first_list_url, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Learn Python', page_text)
        self.assertNotIn('with wife', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy milk')

        second_list_url = self.browser.current_url
        self.assertRegex(second_list_url, '/lists/.+')
        self.assertNotEqual(first_list_url, second_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Learn Python', page_text)
        self.assertIn('Buy milk', page_text)
