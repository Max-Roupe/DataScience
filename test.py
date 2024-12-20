import pandas as pd
import sqlite3
import logging
logger = logging.getLogger()
import os

con = sqlite3.connect('imdb_Top_250_TV_Shows.db')

df = pd.read_csv('imdb_Top_250_TV_Shows.csv', index_col=False)

selected_columns = ['Shows Name', 'Rating']

new_df = df[selected_columns]

new_df.to_sql('imdb_Top_250_TV_Shows', con, if_exists='replace', index=False)

def check_series_in_df(df, show_name, rating):
    """
    Kontrollera om en viss serie med rätt namn och rating finns i DataFrame.

    Example:
        >>> test_df = pd.DataFrame({"Shows Name": ["Breaking Bad", "Planet Earth II"], "Rating": [9.5, 9.5]})
        >>> check_series_in_df(test_df, ["Breaking Bad", "Planet Earth II"], [9.5, 9.5])
        True
        >>> check_series_in_df(test_df, "Arcane", 9.5)
        False
    """
    return not df[(df['Shows Name'] == show_name) & (df['Rating'] == rating)].empty

print(check_series_in_df(new_df, "Breaking Bad", 9.5))
print(check_series_in_df(new_df, "Planet Earth II", 9.5))
print(check_series_in_df(new_df, "Arcane", 9.5))

if __name__ == "__main__":
    import doctest
    doctest.testmod()