import pandas as pd
import sqlite3
import logging
logger = logging.getLogger(__name__)
import os
import requests

con = sqlite3.connect('imdb_Top_250_TV_Shows.db')

df = pd.read_csv('imdb_Top_250_TV_Shows.csv', index_col=False)

df.info()

selected_columns = ['Shows Name', 'Rating']

new_df = df[selected_columns]

new_df.to_sql('imdb_Top_250_TV_Shows', con, if_exists='replace', index=False)

log_file_path = os.path.join(r"C:\Users\maxro\Documents\Skola\DM24H\Data Science\Projekt1", "logfile.log")

os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

logging.basicConfig(
    filename=log_file_path,
    format="[%(asctime)s][%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

csv_file_path = 'imdb_Top_250_TV_Shows.csv'
download_url = 'https://hd.se'

try:
    df = pd.read_csv(csv_file_path, index_col=False)
    logger.info("CSV-filen '%s' lästes in korrekt.", csv_file_path)

    print(new_df)

except FileNotFoundError:
    logger.warning("CSV-filen '%s' hittades inte. Försöker hämta från internet...", csv_file_path)
    try:
        response = requests.get(download_url)
        response.raise_for_status()

        if 'text/csv' not in response.headers.get('Content-Type', ''):
            raise ValueError("Nedladdat innehåll är inte en CSV-fil.")

        with open(csv_file_path, 'w') as f:
            f.write(response.text)
        logger.info("CSV-filen hämtades och sparades som '%s'.", csv_file_path)

        df = pd.read_csv(csv_file_path, index_col=False)

    except requests.RequestException as e:
        logger.error("Kunde inte hämta filen från internet: %s", e)
        print("Kunde inte hämta filen från internet.")

except Exception as e:
    logger.error("Ett oväntat fel inträffade: %s", e, exc_info=True)
    print("Ett oväntat fel inträffade.")
    
finally:
    logger.info("Scriptet är klart.")