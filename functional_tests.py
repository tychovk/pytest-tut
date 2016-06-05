from selenium import webdriver
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
        self.fail('Finish the test!')

        # She is invited to enter a to-do item straight away

        # She types "Buy feathers" into a text box

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers"  as an item in a to-do list

        # There is still a text box inviting her to add another item
        # She enters "Use peacock feather to make a fly"

        # The page updates again, now it shows both items on her list

        # The person wonders whether the site will remember her list. 
        # She sees that the site has generated a unique URL <-- some text explains this

        # She visits that URL: her to-do list is still There

        # She is happy and goes back to sleep.

if __name__ == '__main__':
    unittest.main(warnings='ignore')