from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import unittest
from datetime import datetime


class AutoWebTests(unittest.TestCase):
    browser = None

    '''
    Method to set up the browser and the page to test
    '''
    def setUp(self):
        # Create a new Chrome session
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        self.browser = webdriver.Chrome(options=options)
        # Navigate to the INNOCV home page
        self.browser.get('https://www.innocv.com')
        self.addCleanup(self.browser.quit)

    '''
    Test for the first case
    '''
    def test1(self):
        # Accept cookies
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.ID, "rcc-decline-button")
        )).click()

        # Go to the contact page
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Contacto")
        )).click()

        # Get the phone number
        num = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div/div/div/div[1]/div/div[1]/div/div/div/div/p[2]/span/span[2]')
        )).text[6:]

        # Get the legal notice link page
        aviso = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.LINK_TEXT, "AVISO LEGAL")
        ))
        # Go to the legal notice link position
        self.browser.execute_script("arguments[0].scrollIntoView();", aviso)
        sleep(1)
        # Wait for the legal notice link to be present and click it
        aviso = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//a[.//li[text()='AVISO LEGAL']]")
        ))
        self.browser.execute_script("arguments[0].click();", aviso)

        # Accept cookies
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.ID, "rcc-decline-button")
        )).click()
        # Get the phone number from the legal notice page
        num2 = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Teléfono')]")
        )).text.split('Teléfono ')[1].split('.')[0]
        self.assertEqual(num, num2)

    '''
    Test for the second case
    '''
    def test2(self):
        word = 'Faraday'
        # Accept cookies
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.ID, "rcc-decline-button")
        )).click()

        # Go to the contact page
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Contacto")
        )).click()

        # Get the elements that contain the word 'Faraday' and print it
        faraday = WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, f"//*[contains(text(),'{word}')]")
        ))
        print(f'Numero de veces que aparece {word}: {len(faraday)}')

    '''
    Test for the third case
    '''
    def test3(self):
        # Accept cookies
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.ID, "rcc-decline-button")
        )).click()

        # Go to the contact page
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Contacto")
        )).click()

        # Get the element of the title form
        enviar = WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "p.MuiTypography-root"\
             " jss197 MuiTypography-body1".replace(' ', '.'))
        ))
        # Move to the title form
        self.browser.execute_script("arguments[0].scrollIntoView();", enviar)
        # Get the submit button and click it
        enviar = WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.MuiButtonBase-root MuiButton-root "\
             "MuiButton-contained jss200 MuiButton-containedPrimary".replace(' ', '.'))
        ))
        self.browser.execute_script("arguments[0].click();", enviar)
        # Get the error message
        error = self.browser.find_element(By.CSS_SELECTOR,
                                          'p.MuiFormHelperText-root'\
                                          ' jss206 Mui-error'.replace(' ', '.')
                                          )
        error = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//p[text()='Campo requerido']")
        ))
        # Assert that the error message is not null
        self.assertIsNotNone(error)

    '''
    Test for the fourth case
    '''
    def test4(self):
        # Accept cookies
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.ID, "rcc-decline-button")
        )).click()

        # Go to the contact page
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Contacto")
        )).click()

        # Get the element of the new's title section and move to it
        noticias = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//p[text()='noticias']")
        ))
        self.browser.execute_script("arguments[0].scrollIntoView();", noticias)

        # Wait for the news to be present in the page
        noticias = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='root']/div/div/div[2]/div[2]/div[2]/article")
        ))
        # Get the news dates
        fechas = WebDriverWait(self.browser, 20).until(EC.presence_of_all_elements_located(
            (By.XPATH, "//*[@id='root']/div/div/div[2]/div[2]/div[2]/article/section[*]/div[2]/div[1]/p[2]")
        ))

        # Assert that the news dates are not older than 2 months
        today = datetime.today()
        for fecha in fechas:
            f = datetime.strptime(fecha.text, '%d-%m-%Y')
            self.assertIn((today.year - f.year)*12 + (today.month-f.month),
                          [0, 1, 2])


if __name__ == '__main__':
    unittest.main()
