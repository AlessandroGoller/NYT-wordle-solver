from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from app.dependency import get_settings
from app.utils.terminal import open_chrome

settings = get_settings()

def label_letter(row:int, column:int, browser)-> str:
    xpath: str = f'//*[@id="wordle-app-game"]/div[1]/div/div[{row+1}]/div[{column+1}]/div'
    try:
        element = browser.find_element('xpath',xpath)
        while True:
            data_state = element.get_attribute('data-state')
            if data_state!='tbd':
                break
        # data_state = element.get_attribute('aria-label').split(' ')[1]
        aria_label = element.get_attribute('aria-label').split(' ')[0]
        print(f'{aria_label=}, {data_state=}')
        return aria_label,data_state
    except Exception as e:
        print(f'Error retrieve information on letter:\n{e}')

def press_letter(letter: str, browser) -> None:
    try:
        # button = browser.find_element('data-key',letter)
        button = browser.find_element(By.CSS_SELECTOR,f"button[data-key='{letter}']")
        # button = browser.find_element_by_css_selector(f"button[data-key='{letter}']")
        button.click()
    except Exception as e:
        print(f'Error pressing {letter=}, because: {e}')

def prepare_browser():
    open_chrome()
    opt = Options()
    opt.add_experimental_option("debuggerAddress", f"localhost:{settings.PORT}")
    browser=webdriver.Chrome(options=opt)
    browser.get('https://www.nytimes.com/games/wordle/index.html')
    # remove cookies
    id_cookies: str = 'pz-gdpr-btn-closex'
    try:
        button = browser.find_element('id',id_cookies)
        button.click()
    except:
        print('cookies not present')

    # remove tutorial
    x_path_tutorial: str = '/html/body/div[1]/div/dialog/div/button'
    try:
        button = browser.find_element('xpath',x_path_tutorial)
        button.click()
    except:
        print('Tutorial not present')
    return browser

def insert_word(word:str, browser)-> None:
    word = word.lower()
    for letter in word:
        try:
            press_letter(letter, browser)
        except Exception as e:
            print(f'\n\n error {e}')
    try:
        press_letter('↵', browser)
    except Exception as e:
        print(f'\n\n error {e}')

def already_done(browser):
    xpath: str = '/html/body/div[1]/div/dialog/div/button'
    try:
        button = browser.find_element('xpath',xpath)
        button.click()
    except Exception as e:
        print(f'{e}')
