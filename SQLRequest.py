import sqlite3
import matplotlib.pyplot as plt

db = sqlite3.connect('plane_crash.db')
d = []
cursor = db.cursor()

#cursor.execute("SELECT city,country FROM crash_plane WHERE country = 'United Kingdom'")

#cursor.execute("SELECT DISTINCT city,country FROM crash_plane WHERE country = 'Mexicoo'")
#cursor.execute("UPDATE crash_plane SET country = 'Czechia' WHERE country = 'Czechoslovakia'")
cursor.execute("SELECT crash_plane.city, crash_plane.country, world_cities.lat, world_cities.lng, crash_plane.crash_date, crash_plane.crash_time lng "
               "FROM crash_plane JOIN world_cities ON crash_plane.country = world_cities.country AND crash_plane.city = world_cities.city ORDER BY crash_plane.crash_date")
#cursor.execute("SELECT COUNT(*) FROM crash_plane WHERE crash_plane.country NOT IN (SELECT country FROM world_cities) AND crash_plane.city !=''")

request = cursor.fetchall()
matchs = []
matchs.append(request[0])
for i in range(len(request)-1):
    if request[i+1][5] != matchs[-1][5] or request[i+1][4] != matchs[-1][4]:
        matchs.append(request[i+1])
        print(matchs[-1])


cursor.execute("SELECT strftime('%w',crash_date) FROM crash_plane WHERE crash_date != ''")
date = cursor.fetchall()
print(date)

""""
for i in range(1908, 2020):
    cursor.execute("SELECT COUNT(*) FROM crash_plane WHERE crash_date LIKE ?", ((str(i)+'%'),))
    nb_crash_by_year = cursor.fetchall()
    nb_crash.append(nb_crash_by_year[0][0])
    print(nb_crash_by_year[0][0])


color = []

years = [i for i in range(1908, 2020)]

plt.bar(years, nb_crash)
plt.show()
"""


db.commit()
