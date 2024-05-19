import threading
import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from werkzeug.serving import make_server
from app import create_app, db
from app.config import TestConfig

class ForumSeleniumTestCase(unittest.TestCase):

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()

        self.server = make_server('127.0.0.1', 5000, self.testApp)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()

        time.sleep(1)

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("http://127.0.0.1:5000/")

    def tearDown(self):
        self.driver.quit()

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        self.server.shutdown()
        self.server_thread.join()

        time.sleep(1)

    def test_home_page(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Home")))
            home_link = self.driver.find_element(By.LINK_TEXT, "Home")
            self.assertIsNotNone(home_link)

        except Exception as e:
            print(f"Error during test execution: {e}")
            raise

    def test_about_us(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "aboutus022")))
            about_us_button = self.driver.find_element(By.CLASS_NAME, "aboutus022")
            self.assertIsNotNone(about_us_button)
            about_us_button.click()

            self.driver.back()

        except Exception as e:
            print(f"Error during test execution: {e}")
            raise

    def test_register_page(self):
        try:
            self.driver.get("http://127.0.0.1:5000/register")
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-body-step-1")))

            title = self.driver.find_element(By.CLASS_NAME, "title")
            self.assertIsNotNone(title)
            self.assertEqual(title.text, "SIGN UP")

            description = self.driver.find_element(By.CLASS_NAME, "description")
            self.assertIsNotNone(description)
            self.assertEqual(description.text, "Hello there, Register Form")

        except Exception as e:
            print(f"Error during test execution: {e}")
            raise


    def test_register_form(self):
        try:
            self.driver.get("http://127.0.0.1:5000/register")
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-body-step-1")))

            username_input = self.driver.find_element(By.ID, "username")
            self.assertIsNotNone(username_input)
            self.assertEqual(username_input.get_attribute("placeholder"), "Username*")

            email_input = self.driver.find_element(By.ID, "email")
            self.assertIsNotNone(email_input)
            self.assertEqual(email_input.get_attribute("placeholder"), "E-Mail*")

            password_input = self.driver.find_element(By.ID, "password")
            self.assertIsNotNone(password_input)
            self.assertEqual(password_input.get_attribute("placeholder"), "Password*")

            password_confirm_input = self.driver.find_element(By.ID, "password_confirm")
            self.assertIsNotNone(password_confirm_input)
            self.assertEqual(password_confirm_input.get_attribute("placeholder"), "Confirm Password*")
        except Exception as e:
            print(f"Error during test execution: {e}")
            raise


    def test_register_submit(self):
        try:
            self.driver.get("http://127.0.0.1:5000/register")
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-body-step-1")))

            submit_button = self.driver.find_element(By.ID, "submit")
            self.assertIsNotNone(submit_button)
            self.assertEqual(submit_button.text, "SIGN UP")

        except Exception as e:
            print(f"Error during test execution: {e}")
            raise

if __name__ == '__main__':
    unittest.main()
