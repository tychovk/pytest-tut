from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
# element = WebDriverWait(driver, secs).until(find)


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(50)

    def tearDown(self):
        self.browser.quit()

    def check_for_rows_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_layout_and_styling(self):
        # Go to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Seeing the input box is centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        # Starts a new list and sees that input is nicely centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Person wants to try out an to-do app, and goes to the homepage:
        self.browser.get(self.live_server_url)
        self.browser.implicitly_wait(50)

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
        unique_list_url = self.browser.current_url
        self.assertRegex(unique_list_url, '/lists/.+')
        self.check_for_rows_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item
        # She enters "Use peacock feather to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feather to make a fly')
        inputbox.send_keys(Keys.ENTER)

     
        # The page updates again, now it shows both items on her list
        self.check_for_rows_in_list_table('1: Buy peacock feathers')
        self.check_for_rows_in_list_table('2: Use peacock feather to make a fly')


        # Now a new user2 comes along to the site

        ## we use a new browser session to make sure that no information of
        ## user1 is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(5)


        # user2 visits the home page. There is no sign of user1's list.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # user2 starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # user2 gets his own unique URL
        unique2_list_url = self.browser.current_url
        self.assertRegex(unique2_list_url, '/lists/.+')
        self.assertNotEqual(unique_list_url, unique2_list_url)

        # New page, no trace of user1 list
        page_text = self.browser.find_element_by_tag_name('body').text        
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        self.fail('Finish the test!')

        # She visits that URL: her to-do list is still There

        # She is happy and goes back to sleep.
        
