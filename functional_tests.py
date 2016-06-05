from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Person wants to try out an to-do app, and goes to the homepage:
        self.browser.get('http://localhost:8000')

        # She notices the page title and header that mention a to-do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
            )

        # She types "Buy feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')
        
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers"  as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )

        # There is still a text box inviting her to add another item
        # She enters "Use peacock feather to make a fly"
        self.fail('Finish the test!')

        # The page updates again, now it shows both items on her list

        # The person wonders whether the site will remember her list. 
        # She sees that the site has generated a unique URL <-- some text explains this

        # She visits that URL: her to-do list is still There

        # She is happy and goes back to sleep.

if __name__ == '__main__':
    unittest.main(warnings='ignore')