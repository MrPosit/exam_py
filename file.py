import sqlite3
import datetime
import random
import requests

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

def fetch_movies():
    url = "https://imdb-top-100-movies.p.rapidapi.com/"
    headers = {
        "X-RapidAPI-Key": "33e10f2c54mshe9cb064bfaeb7d2p1d7d81jsndcf9894b64be",
        "X-RapidAPI-Host": "imdb-top-100-movies.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    movies = response.json()
    for movie in movies:
        name = movie.get('title', 'Unknown')
        genre = movie.get('genre', 'Unknown')[0]
        year = movie.get('year', 'Unknown')
        description = movie.get('description', 'Unknown')
        rating = float(movie.get('rating', 'Unknown'))

        name = name.replace('"', "'")
        genre = genre.replace('"', "'")
        description = description.replace('"', "'")

        cursor.execute(f'INSERT INTO movie (name, genre, year, description, rating) VALUES ("{name}", "{genre}", {year}, "{description}", {rating})')
        connection.commit()

def add_cinemas():
    cinemas = [
        {'name': 'Арман', 'adress': 'Проспект Кабанбай батыра, 21'},
        {'name': 'Chaplin cinemas', 'adress': 'проспект Туран, 37'},
        {'name': 'Kinopark ', 'adress': 'проспект Туран, 24'},
        {'name': 'Евразия Cinema7 ', 'adress': 'Евразия-3, улица Алексея Петрова, 24а/1'},
        {'name': 'Keruen Cinema ', 'adress': 'Улица Достык, 16'}
    ]
    for cinema in cinemas:
        name = cinema.get('name', 'Unknown')
        adress = cinema.get('adress', 'Unknown')

        name = name.replace('"', "'")
        adress = adress.replace('"', "'")

        cursor.execute(f'INSERT INTO cinema (name, adress) VALUES ("{name}", "{adress}")')
        connection.commit()

def add_sessions():
    start_date = datetime.date.today()
    end_date = datetime.date(2024, 5, 30)
    start_time = datetime.time(16, 0, 0)
    end_time = datetime.time(0, 0, 0)

    moves_id = [random.randint(1, 100) for i in range(50)]
    cinemas_id = [random.randint(1, 5) for i in range(50)]
    price = [random.randint(1000, 5000) for i in range(50)]

    gap = int((end_date - start_date).total_seconds())

    dates = [start_date + datetime.timedelta(seconds=random.randint(0, gap)) for i in range(50)]

    times = [f'{random.randint(16, 23)}:{random.randint(0, 5)}0:00' for i in range(50)]

    capacitys = [random.randint(50, 100) for i in range(50)]

    for i in range(50):
        cursor.execute(f"INSERT INTO afisha (movie_id, cinema_id, price, data, time, capacity) VALUES ({moves_id[i]}, {cinemas_id[i]}, {price[i]}, '{dates[i]}', '{times[i]}', {capacitys[i]})")
        connection.commit()

def add_places():
    afishas = [i for i in range(1, 51)]
    rooms = [random.randint(1, 6) for _ in range(50)]
    rows = [random.randint(1, 16) for _ in range(50)]
    seats = [random.randint(1, 16) for _ in range(50)]

    for i in range(50):
        cursor.execute(f"INSERT INTO place (afisha_id, room, row, seat) VALUES ({afishas[i]}, {rooms[i]}, {rows[i]}, {seats[i]})")
        connection.commit()

fetch_movies()
add_cinemas()
add_sessions()
add_places()