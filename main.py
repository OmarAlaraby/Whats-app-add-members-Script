import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from colorama import Fore, Back, Style

def createDriver():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")

    args = ["--disable-dev-shm-usage" , "--no-sandbox" , "--disable-notifications" , "--disable-popup-blocking"]
    for i in args :
        chrome_options.add_argument(i)

    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options = chrome_options, service = chrome_service)
    return driver


def openWhatsApp(driver) :
    driver.get('https://web.whatsapp.com/')
    driver.maximize_window()

    # to scan QR code
    time.sleep(30)

def addContact(driver , contact) :

    try :
        driver.find_element(By.XPATH, '//*[@data-testid="add-user"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@title="Search input textbox"]').send_keys(contact)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@title="{}"]'.format(contact)).click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@data-testid="checkmark-medium"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@data-testid="popup-controls-ok"]').click()
        time.sleep(1.4)

        try :
            driver.find_element(By.XPATH, '//*[@data-testid="popup-controls-cancel"]').click()
            time.sleep(1)

        except :
            print(f"{contact} has been {Back.GREEN}added succesfully{Style.RESET_ALL}")
            return

        print(f"{contact} need to be {Fore.BLACK}{Back.RED}invited{Style.RESET_ALL}")
    except :
        driver.find_element(By.XPATH, '//*[@data-testid="x"]').click()
        print(f"{Back.RED}{Fore.BLACK}ERROR WHILE FINDING ELEMENT{Style.RESET_ALL} , {contact} is already in the group , check {contact}'name or number")

def fixed(contact) :
    ret = ""

    for i in contact :
        if i == ' ' or i == '\n':
            break

        ret = ret + i

    return ret

def main() :
    groupName = input("Enter the group's name :  ")

    driver = createDriver()
    openWhatsApp(driver)

    driver.find_element(By.XPATH, '//*[@title="Search input textbox"]').send_keys(groupName)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@title="{}"]'.format(groupName)).click()
    time.sleep(1)
    driver.find_elements(By.XPATH, '//*[@data-testid="menu"]')[1].click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@aria-label="Group info"]').click()
    time.sleep(1)

    with open("Contacts.txt" , 'r') as contactFile :
        data = contactFile.readlines()

        for contact in data:
            time.sleep(1)
            addContact(driver , fixed(contact))

if __name__ == "__main__":
    main()