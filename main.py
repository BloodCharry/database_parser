import selenium
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import Firefox
import os

service = Service(GeckoDriverManager().install())
# '412145'
try:
    federal_number = int(input('Please enter federal number: '))
except:
    print('Wrong number!')

# '08/01/1966'
try:
    date_of_birth = input('Please enter date of birth format(xx/xx/xxxx): ')
except:
    print('Wrong date of birth!')
url = 'https://www.isbapp.be/lid/feddb/f?p=103:19'


def pars_data():
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--headless")
    driver = webdriver.Firefox( options=options, service=service)
    try:
        wait = WebDriverWait(driver, 10)
        driver.get(url)
        input_fd = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#P19_FEDNR')))
        input_fd.send_keys(federal_number)
        input_date = driver.find_element(By.CSS_SELECTOR, '#P19_GEBDAT')
        input_date.send_keys(date_of_birth)
        but_check = driver.find_element(By.CSS_SELECTOR, '#P19_LOGIN')
        but_check.click()

        date_pars = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                               '#wwvFlowForm > table:nth-child(10) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1)')))

        table_html = date_pars.get_attribute('innerHTML')
        soup = BeautifulSoup(table_html, 'html.parser')
        name = soup.find('span', id='P18_NAAM').text
        first_name = soup.find('span', id='P18_VOORNAAM').text
        gender = soup.find('span', id='P18_GESLACHT').text
        home_club = soup.find('span', id='P18_HOMECLUB').text
        whs_idnex = soup.find('span', id='P18_EXACT_HCP').text
        best_idnex = soup.find('span', id='P18_BEST_INDEX').text
        best_index_date = soup.find('span', id='P18_BEST_INDEX_DATE').text
        card_expries = soup.find('span', id='P18_EXPIRATION_DATE').text
        cards = soup.find('span', id='P18_KAARTEN').text
        url_prefix = 'https://www.isbapp.be/lid/feddb/'
        full_url = soup.find('span', id='P18_IMG').find('img')['src']
        photo = url_prefix + full_url
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        filename = os.path.join(dir_path, "data.sql")
        if os.path.isfile(filename):
            with open(filename, "a") as f:
                f.write(
                    f"INSERT INTO Player_Detail (name, first_name, gender, home_club, whs_idnex, best_idnex, best_index_date, card_expries, cards, photo) VALUES ('{name}', '{first_name}', '{gender}', '{home_club}', '{whs_idnex}', '{best_idnex}', '{best_index_date}', '{card_expries}', '{cards}', '{photo}');\n")
                driver.close()
        else:
            with open(filename, "w") as f:
                f.write(
                    "CREATE TABLE Player_Detail (name TEXT, first_name TEXT, gender TEXT, home_club TEXT, whs_idnex TEXT, best_idnex TEXT, best_index_date TEXT, card_expries TEXT, cards TEXT, photo BLOB);\n")
                f.write(
                    f"INSERT INTO Player_Detail (name, first_name, gender, home_club, whs_idnex, best_idnex, best_index_date, card_expries, cards, photo) VALUES ('{name}', '{first_name}', '{gender}', '{home_club}', '{whs_idnex}', '{best_idnex}', '{best_index_date}', '{card_expries}', '{cards}', '{photo}');\n")
        driver.close()
    except Exception:
        driver.close()
    raise Exception

try:
    pars = pars_data()
    print('Successfully!')
except Exception as e:
    print(f'Error: Invalid data. Please check your details and try again')
