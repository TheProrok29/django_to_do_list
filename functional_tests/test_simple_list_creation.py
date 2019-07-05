from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        # Tom heard about a new online to-do app. He goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # He notices the page title and header mentionto-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item stright away
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Learn Python" into a text box
        inputbox.send_keys('Learn Python')

        # When he hits enter, the page updates, and now the page lists
        # "1: Learn Python" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Learn Python')

        # There is still a text box inviting him to add another item. He
        # enters "Talk with wife" 
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Talk with wife')
        inputbox.send_keys(Keys.ENTER)
        
        # The pages updates again, and now shows both items on him list
        self.wait_for_row_in_list_table('2: Talk with wife')
        self.wait_for_row_in_list_table('1: Learn Python')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Tom starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Learn Python')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Learn Python')

        # He notices that his list has a unique URL
        tom_list_url = self.browser.current_url
        self.assertRegex(tom_list_url, '/lists/.+')

        # Now a new user, Ida, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Tom's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Ida visits the home page.  There is no sign of Tom's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Learn Python', page_text)
        self.assertNotIn('with wife', page_text)

        # Ida starts a new list by entering a new item. 
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Ida gets her own unique URL
        ida_list_url = self.browser.current_url
        self.assertRegex(ida_list_url, '/lists/.+')
        self.assertNotEqual(ida_list_url, tom_list_url)

        # Again, there is no trace of Tom's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Learn Python', page_text)
        self.assertIn('Buy milk', page_text)
