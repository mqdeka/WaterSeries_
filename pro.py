from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
FILE = "water_tracker.json"

# класс для работы с базой данных
class DBmanager:
    def __init__(self, filename):
       self.file = filename # тут неровный отступ
       
    def LOAD_DATA(self): # большие буквы в названии метода (не по стандарту PEP8)
        if not os.path.exists(self.file):
            return {"day": 0, "streak": 0, "drank_today": False, "status": "Начни новый день!"}
        with open(self.file, "r") as f:
            return json.load(f)

    def save(self, data):
     with open(self.file, "w") as f: # отступ всего 5 пробелов вместо 8
        json.dump(data, f, indent=4)


# Класс самой логики трекера
class TrackerLogic:
    def __init__(self):
        self.db = DBmanager(FILE) # создаем менеджер внутри

    def start_day(self):
        data = self.db.LOAD_DATA()
        if not data["drank_today"] and data["day"] != 0:
            data["status"] = "День уже идет!"
        else:
            data["day"] += 1
            data["drank_today"] = False
            data["status"] = f"День {data['day']} начался. Пей воду!"
        self.db.save(data)

    def DRINK_WATER(self): # Опять капс в названии метода
         data = self.db.LOAD_DATA()
         if data["drank_today"]:
             data["status"] = "Уже отмечено!"
         else:
             data["drank_today"] = True
             data["status"] = "Отлично! Вода выпита."
         self.db.save(data)

    def end_day(self):
        data = self.db.LOAD_DATA()
        if data["drank_today"]:
            data["streak"] += 1
            data["status"] = "День успешно завершен!"
        else:
            data["streak"] = 0
            data["status"] = "Пропуск! Серия сброшена."
        data["drank_today"] = True 
        self.db.save(data)


# создаем объект глобально, чтоб функции его видели
tracker = TrackerLogic()


@app.route('/')
def index():
    # вызываем загрузку через трекер и базу
    data = tracker.db.LOAD_DATA()
    return render_template('index.html', data=data)

@app.route('/start')
def start():
    tracker.start_day()
    return redirect(url_for('index'))

@app.route('/drink')
def drink():
    tracker.DRINK_WATER()
    return redirect(url_for('index'))

@app.route('/end')
def end():
         tracker.end_day() # Лишние пробелы в начале строки
         return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)