import time

from app.utils.algorithms import analyze, check_inserted_word
from app.utils.website_controller import insert_word, prepare_browser


def controller():
    browser = prepare_browser()
    time.sleep(2)
    while True:
        word = analyze(browser=browser)
        if word is True:
            input('Word founded')
            break
        print(word)
        time.sleep(1)
        insert_word(word=word, browser=browser)
        time.sleep(1.5)
        check_inserted_word(browser=browser)
        # input('Wait')

def test():
    None

if __name__ == "__main__":
    controller()
