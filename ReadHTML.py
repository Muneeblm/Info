import requests
import re
import sqlite3

months = {}
months["January"] = '01'
months["February"] = '02'
months["March"] = '03'
months["April"] = '04'
months["May"] = '05'
months["June"] = '06'
months["July"] = '07'
months["August"] = '08'
months["September"] = '09'
months["October"] = '10'
months["November"] = '11'
months["December"] = '12'

db = sqlite3.connect('plane_crash.db')
cursor = db.cursor()



years = [i for i in range(1920,2020)]
for year in years:

    r = requests.get("http://www.planecrashinfo.com/"+str(year)+"/"+str(year)+".htm")

    number = len(re.findall("HREF", r.text))
    for i in range(1, number + 1):

        r = requests.get("http://www.planecrashinfo.com/" + str(year) + "/" + str(year) + "-" + str(i) + ".htm")

        dict = {}

        r = re.split("<td width=\"547\" valign=\"top\" align=\"left\"><font face=\"Arial\" size=\"2\">", r.text, 1)
        r = re.split("</td>", r[1], 1)

        dict["crash_date"] = r[0].split(", ")[1] + "-" + months[r[0].split(" ", 1)[0]] + "-" + r[0].split(" ")[1].split(",")[0]

        r = re.split(
            "<td bgcolor=\"dcdcdc\" width=\"547\" valign=\"top\" align=\"left\"><font face=\"Arial\" size=\"2\">", r[1],
            1)
        r = re.split("</td>", r[1], 1)

        if r[0] == "?":
            dict["crash_time"] = ""
        if len(list(r[0])) == 5 and ':' in list(r[0]):
            dict["crash_time"] = r[0]
        if len(list(r[0])) == 5 and ':' not in list(r[0]):
            dict["crash_time"] = list(r[0])[-4 ] + list(r[0])[-3] + ":" + list(r[0])[-2] + list(r[0])[-1]
        if len(list(r[0])) == 4:
            dict["crash_time"] = list(r[0])[0] + list(r[0])[1] + ":" + list(r[0])[2] + list(r[0])[3]
        if len(list(r[0])) > 5:
            if list(r[0])[0] == "c":
                dict["crash_time"] = list(r[0])[-5] + list(r[0])[-4] + list(r[0])[-3] + list(r[0])[-2] + list(r[0])[-1]
            else:
                dict["crash_time"] = list(r[0])[-6] + list(r[0])[-5] + list(r[0])[-4] + list(r[0])[-3] + list(r[0])[-2]
        if dict["crash_time"] != "" and list(dict["crash_time"])[0] == " ":
            dict["crash_time"] = "0" + dict["crash_time"].split(" ")[1]

        try:
            int(list(dict["crash_time"])[0]) and int(list(dict["crash_time"])[1]) and int(list(dict["crash_time"])[3]) and int(list(dict["crash_time"])[4])
        except:
            dict["crash_time"] = ""

        r = re.split("<td width=\"547\" valign=\"top\" align=\"left\"><font face=\"Arial\" size=\"2\">", r[1], 1)
        r = re.split("</td>", r[1], 1)

        if r[0] == "?":
            country = ""
            city = ""
        if len(r[0].split(", ")) == 2 and "," not in list(r[0].split(", ")[0]) and "," not in list(
                r[0].split(", ")[1]) and re.search("off", r[0].split(", ")[0]) is None:

            city = r[0].split(", ")[0]

            m = re.search("Off ", city)
            if m is not None:
                city = city[:m.start()] + city[m.end():]

            m = re.search("Near ", city)
            if m is not None:
                city = city[:m.start()] + city[m.end():]

            country = r[0].split(", ")[1]

        else:
            print(r[0])
            city = input("Enter the city : ")
            country = input("Enter the country : ")

        dict["country"] = country
        dict["city"] = city
        r = re.split(
            "<td bgcolor=\"dcdcdc\" width=\"547\" valign=\"top\" align=\"left\"><font face=\"Arial\" size=\"2\">", r[1],
            1)
        r = re.split("</td>", r[1], 1)

        if r[0] != "?":
            dict["operator"] = r[0]
        else:
            dict["operator"] = ""

        r = re.split("<td  width=\"547\" valign=\"top\" align=\"left\"><font face=\"Arial\" size=\"2\">", r[1], 1)
        r = re.split("</td>", r[1], 1)

        if r[0] != "?":
            dict["flight"] = r[0]
        else:
            dict["flight"] = ""

        r = re.split(
            "<td bgcolor=\"dcdcdc\" width=\"547\" valign=\"top\" align=\"left\"><font face=\"Arial\" size=\"2\">", r[1],
            1)
        r = re.split("</td>", r[1], 1)

        if r[0] != "?":
            dict["route"] = r[0]
        else:
            dict["route"] = ""

        r = re.split("<td width=\"547\" valign=\"top\" align=\"left\"><font face=\"Arial\" size=\"2\">", r[1], 1)
        r = re.split("</td>", r[1], 1)

        if r[0] != "?":
            dict["ac_type"] = r[0]
        else:
            dict["ac_type"] = ""

        r = re.split(
            "<td bgcolor=\"dcdcdc\" width=\"547\" valign=\"top\" align=\"left\"><font face=\"Arial\" size=\"2\">", r[1],
            1)
        r = re.split("</td>", r[1], 1)

        if r[0] != "?":
            dict["registration"] = r[0]
        else:
            dict["registration"] = ""

        r = re.split("<td width=\"547\" valign=\"top\" align=\"left\"><font face=\"Arial\" size=\"2\">", r[1], 1)
        r = re.split("</td>", r[1], 1)

        if r[0] != "?":
            dict["cn_ln"] = r[0]
        else:
            dict["cn_ln"] = ""

        r = re.split(
            "<td bgcolor=\"dcdcdc\"width=\"547\" valign=\"top\" align=\"left\"><font face=\"Arial\" size=\"2\">", r[1],
            1)
        r = re.split("</td>", r[1], 1)

        f = r[0].split("&nbsp;")
        f = f[0] + f[1] + f[2]

        if f.split("  ")[1].split(" ")[0].split("passengers:")[1] != "?":
            dict["passenger_aboard"] = int(f.split("  ")[1].split(" ")[0].split("passengers:")[1])
        else:
            dict["passenger_aboard"] = None

        if f.split("  ")[1].split(" ")[1].split("crew:")[1].split(")")[0] != "?":
            dict["crew_aboard"] = int(f.split("  ")[1].split(" ")[1].split("crew:")[1].split(")")[0])
        else:
            dict["crew_aboard"] = None

        r = re.split("<td width=\"547\" valign=\"top\" align=\"left\"><font face=\"Arial\" size=\"2\">", r[1], 1)
        r = re.split("</td>", r[1], 1)

        f = r[0].split("&nbsp;")
        f = f[0] + f[1] + f[2]

        if f.split("  ")[1].split(" ")[0].split("passengers:")[1] != "?":
            dict["passenger_fatalities"] = int(f.split("  ")[1].split(" ")[0].split("passengers:")[1])
        else:
            dict["passenger_fatalities"] = None

        if f.split("  ")[1].split(" ")[1].split("crew:")[1].split(")")[0] != "?":
            dict["crew_fatalities"] = int(f.split("  ")[1].split(" ")[1].split("crew:")[1].split(")")[0])
        else:
            dict["crew_fatalities"] = None

        r = re.split(
            "<td bgcolor=\"dcdcdc\" width=\"547\" valign=\"top\" align=\"left\"><font face=\"Arial\" size=\"2\">", r[1],
            1)
        r = re.split("</td>", r[1], 1)

        if r[0] != "?":
            dict["ground"] = int(r[0])
        else:
            dict["ground"] = ""

        r = re.split("<td width=\"547\" valign=\"top\" align=\"left\"><font face=\"Arial\" size=\"2\">", r[1], 1)
        r = re.split("</td>", r[1], 1)

        if r[0] != "?":
            dict["summary"] = r[0]
        else:
            dict["summary"] = ""

        print(dict["crash_date"])
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS crash_plane(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,crash_date DATE, crash_time TIME, ground INT, registration CHAR, operator CHAR, crew_aboard INT, passenger_aboard INT, crew_fatalities INT, passenger_fatalities INT, city CHAR, country CHAR, route CHAR, flight CHAR, ac_type CHAR, cn_ln CHAR, summary TEXT)")
        cursor.execute(
            "INSERT INTO crash_plane(crash_date, crash_time, ground, registration, operator, crew_aboard, passenger_aboard, crew_fatalities, passenger_fatalities, city, country, route, flight, ac_type, cn_ln, summary) VALUES (:crash_date, :crash_time, :ground, :registration, :operator, :crew_aboard, :passenger_aboard, :crew_fatalities, :passenger_fatalities, :city, :country, :route, :flight, :ac_type, :cn_ln, :summary)",
            dict)


db.close()
