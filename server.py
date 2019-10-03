from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import json
import album
import datetime

# Функция для GET запросов, выводящая список альбомов указанного исполнителя, 
# в скобках указано количество альбомов 
@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Список альбомов ({}) {}:\n".format(len(albums_list),artist)
        result += ",\n".join(album_names)
    return result

# Функция проверки года, проверяет входит ли в указанный год в промежуток с 1600 года,
# а также количество символов должно быть равно 4
def check_year(year_str):
    year_range = range(1600, datetime.date.today().year)
    if not year_str.isdigit():
        print("При указании года испльзуйте цифры. Укажите в формате: ГГГГ")
        return False
    if not len(year_str) == 4 or int(year_str) not in year_range:
        print("Укажите год от 1600 до {} в формате: ГГГГ".format(datetime.date.today().year))
        return False
    print("Проверка года успешно пройдена!")
    return True

# Функция сохранения данных альбома в json документ
def save_album(album_data):
    year = album_data["year"]
    artist = album_data["artist"]
    genre = album_data["genre"]
    album = album_data["album"]
    filename = "{}-{}.json".format(album, artist)

    with open(filename, "w") as fd:
        json.dump(album_data, fd)
    return filename

# Функция проверки всех данных альбома, испльзует также ф-ии из модуля album.py
def check_album(album_data):
    if not album.find_genre(album_data["genre"]):
        print("Ошибка при вводе жанра")
        print("попробуйте Psychedelic rock, Jazz, Rock and roll, Rhythm and blues, Art rock, Progressive rock")
        return False
    elif album.find_album(album_data["album"]) and album.find(album_data["artist"]):
        print("Такой альбом уже есть в базе")
        return False
    elif album.find_album(album_data["album"]) and album.find(album_data["artist"]):
        print("Такой альбом уже есть в базе")
        return False
    elif not check_year(album_data["year"]):
        print("Ошибка при вводе года")
        return False
    return True
    
 # Функция для POST запросов
@route("/albums", method="POST")
def new_album():
    album_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    
    if check_album(album_data):
        resource_path = save_album(album_data)
        print("Альбом сохранен в: ", resource_path)
        message = "Данные успешно сохранены"
        return message
    else:
        message = "Ошибка при вводе данных"
        return HTTPError(409, message)

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)