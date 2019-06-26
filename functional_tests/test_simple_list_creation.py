from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        inputbox.send_keys('Learn Python')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Learn Python')

        inputbox = self.get_item_input_box()
        inputbox.send_keys('Talk with wife')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Learn Python')
        self.wait_for_row_in_list_table('2: Talk with wife')

        table = self.get_item_input_box()
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Learn Python', [row.text for row in rows])
        self.assertIn('2: Talk with wife', [row.text for row in rows])

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
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

        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy milk')

        second_list_url = self.browser.current_url
        self.assertRegex(second_list_url, '/lists/.+')
        self.assertNotEqual(first_list_url, second_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Learn Python', page_text)
        self.assertIn('Buy milk', page_text)
