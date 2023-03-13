from functools import lru_cache
from typing import Union

import pandas as pd

from app.utils.edit_list import letter_in_word
from app.utils.website_controller import label_letter

row:int = 0

temp_absent_letter : list[str] = []
list_possbile_word:list[str]= []

df: pd.DataFrame = None
csv_path:str = 'df_words.csv'

def restart():
    global df, row,list_possbile_word
    df = read_words()
    list_possbile_word = []
    row = 0

    # Theory
    # Not plural words
    df = df.loc[~df[f'letter_{5}'].str.contains('s')]

@lru_cache(maxsize=1)  
def read_words()->pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df.iloc[:, :5]
    return df

def check_inserted_letter(letter:str,state:str, col:int):
    global df, list_possbile_word, temp_absent_letter
    if state == 'correct':
        df = df.loc[df[f'letter_{col+1}'] == letter]
        list_possbile_word.append(letter)
    elif state == 'present':
        df = df.loc[~df[f'letter_{col+1}'].str.contains(letter)]
        df = df[df.apply(lambda x: x.str.contains(letter)).any(axis=1)]
    elif state == 'absent' and letter not in list_possbile_word:
        temp_absent_letter.append(letter)

def check_inserted_word(browser):
    global df, row, temp_absent_letter
    for col in range(letter_in_word):
        letter,state = label_letter(row,col,browser)
        check_inserted_letter(letter, state, col)
    for letter in temp_absent_letter:
        df = df[~df.apply(lambda x: x.str.contains(letter)).any(axis=1)]
    row = row+1

def analyze(browser)-> Union[bool,str]:
    global df
    if label_letter(0,0,browser)[1]=='empty':
        restart()
        return 'salet'
        return ''.join([str(elem) for elem in df.iloc[0][:5]])
    return ''.join([str(elem) for elem in df.iloc[0][:5]])
