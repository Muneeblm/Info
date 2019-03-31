# import libraries
import numpy
import folium
import pandas as pd
import sqlite3
import re

db = sqlite3.connect('plane_crash.db')
cursor = db.cursor()
cursor.execute("SELECT crash_plane.city, crash_plane.country, world_cities.lat, world_cities.lng, crash_plane.crash_date, crash_plane.crash_time lng "
               "FROM crash_plane JOIN world_cities ON crash_plane.country = world_cities.country AND crash_plane.city = world_cities.city ORDER BY crash_plane.crash_date")

request = cursor.fetchall()
matchs = []
matchs.append(request[0])
for i in range(len(request)-1):
    if request[i+1][5] != matchs[-1][5] or request[i+1][4] != matchs[-1][4]:
        matchs.append(request[i+1])



#Make a data frame with dots to show on the map
data = pd.DataFrame({
    'lat': [float(x[2]) for x in matchs if re.search("1953", x[4])],
    'lon': [float(x[3]) for x in matchs if re.search("1953", x[4])],
    'name': [x[0]+", "+x[1]+", "+x[4]+" "+x[5] for x in matchs if re.search("1953", x[4])]
})


# Make an empty map
m = folium.Map(location=[20, 0], tiles="Mapbox Bright", zoom_start=2)

# I can add marker one by one on the map
for i in range(0, len(data)):
    folium.Marker([data.iloc[i]['lon'], data.iloc[i]['lat']], popup=data.iloc[i]['name']).add_to(m)

m.save("test.html")