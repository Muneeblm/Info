import pandas
import sqlite3
import re

csv = pandas.read_csv("worldcities.csv", sep=';')

world_city = {}

db = sqlite3.connect('plane_crash.db')

cursor = db.cursor()
cursor.execute("DROP TABLE world_cities")
db.commit()

for i in range(len(csv)):
    world_city["city"] = csv["city_ascii"][i]
    world_city["country"] = csv["country"][i]
    world_city["lat"] = re.sub(',', '.', csv["lng"][i])
    world_city["lng"] = re.sub(',', '.', csv["lat"][i])

    cursor = db.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS world_cities(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, city CHAR, country CHAR, lat FLOAT, lng FLOAT)")
    cursor.execute(
        "INSERT INTO world_cities(city, country, lat, lng) VALUES (:city, :country, :lat, :lng)", world_city)

cursor.execute("SELECT * FROM world_cities")
nb_cities = cursor.fetchall()
print(nb_cities)

db.close()

