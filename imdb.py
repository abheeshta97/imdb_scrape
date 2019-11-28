
from bs4 import BeautifulSoup
import requests
import sqlite3

conn = sqlite3.connect('imdbList.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS MovieList')

cur.execute('''
CREATE TABLE MovieList (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        MovieName VARCHAR(200),
                        Year YEAR,
                        Rating DEC(2,1))''')

url = "https://www.imdb.com/chart/top"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, features= 'lxml')
tbody = soup.find('tbody', class_='lister-list')

for tr in tbody.find_all('tr'):

    record = tr
    movieName = record.find('td', class_='titleColumn').a.text
    year = record.find('span', class_='secondaryInfo').text.strip('()')
    rating = record.find('td', class_='ratingColumn imdbRating').strong.text

    cur.execute("INSERT INTO MovieList (MovieName, Year, Rating) VALUES (?, ?, ?)", (movieName, year, rating))
    conn.commit()

cur.close()