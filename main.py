import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

def create_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS cinema (id INTEGER PRIMARY KEY, name TEXT, address TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS movie (id INTEGER PRIMARY KEY, name TEXT, year INTEGER, genre TEXT, description TEXT, rating REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS afisha (id INTEGER PRIMARY KEY, movie_id INTEGER, cinema_id INTEGER, price INTEGER, date TEXT, time TEXT, capacity INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS place (id INTEGER PRIMARY KEY, afisha_id INTEGER, room INTEGER, row INTEGER, seat INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS ticket (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, place_id INTEGER, payment_status TEXT)")

create_table()

def select_movie_and_cinema():
    cursor.execute("SELECT id, name FROM movie")
    movies = cursor.fetchall()

    current_page = 0
    page_size = 5

    while True:
        print("\n Выберите фильм:")
        for i in range(current_page * page_size, min((current_page + 1) * page_size, len(movies))):
            movie = movies[i]
            print(f"{movie[0]}. {movie[1]}")

        option = input("Введите 'след' для следующей страницы, 'назад' для предыдущей или номер выбранного фильма: ")

        if option == 'след':
            current_page += 1
        elif option == 'назад' and current_page > 0:
            current_page -= 1
        elif option.isdigit():
            movie_id = int(option)
            if movie_id in [movie[0] for movie in movies]:
                cursor.execute("SELECT id, name FROM cinema")
                cinemas = cursor.fetchall()
                while True:
                    print("\n Выберите кинотеатр:")
                    for cinema in cinemas:
                        print(f"{cinema[0]}. {cinema[1]}")
                    cinema_id = input("Введите номер выбранного кинотеатра: ")
                    if cinema_id.isdigit():
                        cinema_id = int(cinema_id)
                        if cinema_id in [cinema[0] for cinema in cinemas]:
                            return movie_id, cinema_id
                        else:
                            print("Ошибка: Введите корректный номер кинотеатра")
                            continue
                    print("Ошибка: Введите корректный номер кинотеатра")
            else:
                print("Ошибка: Введите корректный номер фильма")
        else:
            print("Ошибка: Введите корректное значение")

def select_showtime(movie_id, cinema_id):
    cursor.execute("SELECT id, data, time FROM afisha WHERE movie_id = ? AND cinema_id = ?", (movie_id, cinema_id))
    showtimes = cursor.fetchall()

    print("\n Выберите время показа:")
    for showtime in showtimes:
        print(f"{showtime[0]}. {showtime[1]} {showtime[2]}")

    showtime_id = int(input("Введите номер выбранного времени показа: "))
    return showtime_id

def select_seats(showtime_id):
    cursor.execute("SELECT room FROM place WHERE afisha_id = ?", (showtime_id,))
    room_number = cursor.fetchone()[0]

    cursor.execute("SELECT row, seat FROM place WHERE afisha_id = ?", (showtime_id,))
    seats = cursor.fetchall()

    print("\n Схема зала:")
    for row in range(1, room_number + 1):
        row_seats = [seat for seat in seats if seat[0] == row]
        row_display = " ".join([f"[{seat[1]}]" if seat[1] in [s[1] for s in row_seats] else f"{seat[1]}" for seat in seats])
        print(f"Ряд {row}: {row_display}")

    chosen_seats = input("Введите номера выбранных мест через запятую (например, '1,2...'): ")
    chosen_seats = [int(seat) for seat in chosen_seats.split(',')]

    chosen_seats = input("Введите номера выбранных мест через запятую (например, '1,2...'): ")
    chosen_seats = [int(seat) for seat in chosen_seats.split(',')]

    print("\n Выбранные места:")
    for seat in chosen_seats:
        cursor.execute("SELECT row, seat FROM place WHERE afisha_id = ? AND seat = ?", (showtime_id, seat))
        result = cursor.fetchone()
        if result is not None:
            row, seat = result
            print(f"Ряд {row}, Место {seat}")
        else:
            print(f"Место {seat} не найдено для данного сеанса.")


def process_payment():
    card_number = input("Введите имя: ")
    expiration_date = input("Введите номер карты: ")
    cvv = input("Введите CVV код: ")

    print("Обработка платежа...")

    return True

selected_movie_id, selected_cinema_id = select_movie_and_cinema()
selected_showtime_id = select_showtime(selected_movie_id, selected_cinema_id)
selected_seats = select_seats(selected_showtime_id)

if process_payment():
    print("Платеж успешно обработан.")
else:
    print("Ошибка обработки платежа. Пожалуйста, попробуйте снова.")
