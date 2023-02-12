from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import unittest
from datetime import datetime


class AutoWebTests(unittest.TestCase):
    browser = None
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        self.browser = webdriver.Chrome(options=options)
        self.addCleanup(self.browser.quit)

    def test1(self):
        self.browser.get('https://www.innocv.com')
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.ID, "rcc-decline-button")
        )).click()

        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Contacto")
        )).click()

        num_telephone = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.XPATH,'/html/body/div/div/div/div[1]/div/div[1]/div/div/div/div/p[2]/span/span[2]')
        )).text[6:]

        aviso = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((
            By.LINK_TEXT, "AVISO LEGAL")))
        self.browser.execute_script("arguments[0].scrollIntoView();", aviso)
        sleep(1)
        aviso = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//a[.//li[text()='AVISO LEGAL']]")
        ))
        self.browser.execute_script("arguments[0].click();", aviso)

        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.ID, "rcc-decline-button")
        )).click()
        num_telephone2 = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((
            By.XPATH, f"//*[contains(text(),'Teléfono')]"))).text.split('Teléfono ')[1]\
                .split('.')[0]
        self.assertEqual(num_telephone, num_telephone2)

    def test2(self):
        word = 'Faraday'
        self.browser.get('https://www.innocv.com')
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.ID, "rcc-decline-button")
        )).click()

        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Contacto")
        )).click()

        faraday = WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located((
            By.XPATH, f"//*[contains(text(),'{word}')]")))
        print(f'Numero de veces que aparece {word}: {len(faraday)}')


    def test3(self):
        self.browser.get('https://www.innocv.com')
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.ID, "rcc-decline-button")
        )).click()

        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Contacto")
        )).click()

        enviar = WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "p.MuiTypography-root jss197 MuiTypography-body1".replace(' ', '.'))
        ))
        self.browser.execute_script("arguments[0].scrollIntoView();", enviar)
        enviar = WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.MuiButtonBase-root MuiButton-root MuiButton-contained jss200 MuiButton-containedPrimary".replace(' ', '.'))
        ))
        self.browser.execute_script("arguments[0].click();", enviar)
        error = self.browser.find_element(By.CSS_SELECTOR, 'p.MuiFormHelperText-root jss206 Mui-error'.replace(' ', '.'))
        error = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((
            By.XPATH, "//p[text()='Campo requerido']")))
        self.assertIsNotNone(error)


    def test4(self):
        self.browser.get('https://www.innocv.com')
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.ID, "rcc-decline-button")
        )).click()

        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Contacto")
        )).click()

        noticias = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//p[text()='noticias']")
        ))
        self.browser.execute_script("arguments[0].scrollIntoView();", noticias)

        noticias = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='root']/div/div/div[2]/div[2]/div[2]/article")
        ))
        fechas = WebDriverWait(self.browser, 20).until(EC.presence_of_all_elements_located((
            By.XPATH, "//*[@id='root']/div/div/div[2]/div[2]/div[2]/article/section[*]/div[2]/div[1]/p[2]")))

        today = datetime.today()
        for fecha in fechas:
            f = datetime.strptime(fecha.text,'%d-%m-%Y')
            self.assertIn((today.year - f.year)*12 + (today.month  - f.month ), [0,1,2])


if __name__ == '__main__':
    unittest.main()