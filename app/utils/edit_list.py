import pandas as pd

letter_in_word = 5

def read_words_from_txt(name:str) -> list[str]:
    with open(f'{name}.txt', 'r') as file:
        file_content: str = file.read()
        word: str = file_content
    list_word: list[str] = word.split('\n')
    return list_word

def count_letter(df_word:pd.DataFrame)->pd.DataFrame:
    """
    Create a dataframe contains the number of letter in the x position
    """
    df_letter: pd.DataFrame = pd.concat([pd.crosstab(index=df_word[column], columns=column, normalize='columns') for column in df_word.columns], axis=1).fillna(0) # noqa
    df_letter = df_letter.sort_index()
    return df_letter

def order_df(df_words: pd.DataFrame, df_letter: pd.DataFrame) ->pd.DataFrame:
    global letter_in_word

    # add column with probability
    """
    for i in range(letter_in_word):
        print(i)
        df_order_word[f'value_letter_{i+1}'] = df_order_word[f'letter_{i+1}'].apply(lambda x: df_letter.loc[x, f'letter_{i+1}']) """ # noqa

    df_valori = df_words.apply(lambda x: pd.Series([df_letter.loc[x[i], f'letter_{i+1}'] for i in range(5)], index=[f'value_letter_{i+1}' for i in range(letter_in_word)]), axis=1) # noqa
    df_order_word: pd.DataFrame = pd.concat([df_words, df_valori], axis=1)
    # add columns with the mean probability
    df_order_word['mean'] = df_order_word.iloc[:, 6:].mean(axis=1)
    # order it
    df_order_word = df_order_word.sort_values(by='mean', ascending=False)
    return df_order_word

def analyze_words(name:str) -> None:
    list_word: list[str] = read_words_from_txt(name)
    # Create a Pandas Dataframe
    df_words: pd.DataFrame = pd.DataFrame(list_word, columns=['word'])
    # each column a letter
    df_words = pd.concat([df_words['word'].str[i].rename(f'letter_{i+1}') for i in range(5)], axis=1)
    df_letter: pd.DataFrame = count_letter(df_words)

    # Doesn't change 
    df_words = order_df(df_words,df_letter)
    df_words.to_csv('df_words.csv', index=False)

if __name__ == "__main__":
    name:str = 'wordle-nyt-answers-alphabetical'
    analyze_words(name)
