
import sqlite3

import time

import os

script_directory = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(script_directory, "Weather_db.db")
db_zaloha = os.path.join(script_directory,"analyses","Weather_db.db")

def readALL():

    global lastbuilddate, city, country, region, chill, \
    direction, speed, sunrise, sunset, humidity, pressure, \
    rising, visibility, title, pubdate, code, date, temp, text, creatat, changeat, \
    fcondate, fcode, fdate, fday, fhigh, flow, ftext, fcreatat, fchangeat

    lastbuilddate = []
    city = []
    country = []
    region = []
    chill = []
    direction = []
    speed = []
    sunrise = []
    sunset = []
    humidity = []
    pressure = []
    rising = []
    visibility = []
    title = []
    pubdate = []
    code = []
    date = []
    temp = []
    text = []
    creatat = []
    changeat = []
    fcondate = []
    fcode = []
    fdate = []
    fday = []
    fhigh = []
    flow = []
    ftext = []
    fcreatat = []
    fchangeat = []
    
    readDB()

    for c in conditions:
        lastbuilddate.append(c["lastbuilddate"])
        city.append(c["city"])
        country.append(c["country"])
        region.append(c["region"])
        chill.append(c["chill"])
        direction.append(c["direction"])
        speed.append(c["speed"])
        sunrise.append(c["sunrise"])
        sunset.append(c["sunset"])
        humidity.append(c["humidity"])
        pressure.append(c["pressure"])
        rising.append(c["rising"])
        visibility.append(c["visibility"])
        title.append(c["title"])
        pubdate.append(c["pubdate"])
        code.append(c["code"])
        date.append(c["date"])
        temp.append(c["temp"])
        text.append(c["text"])
        creatat.append(c["creatat"])
        changeat.append(c["changeat"])

    for i in range(0, len(lastbuilddate)):
        print(i, "lastbuilddate:", lastbuilddate[i])
    
    for f in forecasts:
        fcondate.append(f["condate"])
        fcode.append(f["code"])
        fdate.append(f["date"])
        fday.append(f["day"])
        fhigh.append(f["high"])
        flow.append(f["low"])
        ftext.append(f["text"])
        fcreatat.append(f["creatat"])
        fchangeat.append(f["changeat"])
    for i in range(0, len(fcondate)):
        #print(i, "fcondate:", fcondate[i], "fcode:", fcode[i], "fdate:", fdate[i], "fday:", fday[i], "fhigh:", fhigh[i], "flow:", flow[i], "ftext:", ftext[i], "fcreatat:", fcreatat[i], "fchangeat:", fchangeat[i])
        print(i, "fcondate:", fcondate[i], "fdate:", fdate[i])

    initDB_zaloha()

    for i in range(0, len(lastbuilddate)):
        insertCondDB(i)

    for i in range(0, len(fcondate)):
        insertForeDB(i)
        
    conn.close()
    
    print()
    print("Waiting for 1 second...")
    time.sleep(1)

def readDB():
    global conn, cursor, conditions, forecasts
    conn = sqlite3.connect(db)    # všude je potřeba testovat exceptions
    conn.row_factory = sqlite3.Row          # abych mohl používat názvy sloupců místo indexů
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM condition")
    conditions = cursor.fetchall()         # načte všechnyřádky ze selectu

    cursor.execute("SELECT * FROM forecast")
    forecasts = cursor.fetchall()         # načte všechnyřádky ze selectu
  
    conn.close()  # toto by se mělo vždy udělat, při update načíst dtb znovu
    # pro jednoduchost zakomentováno

def initDB_zaloha():
    global conn, cursor
    conn = sqlite3.connect(db_zaloha)    # všude je potřeba testovat exceptions
    conn.row_factory = sqlite3.Row          # abych mohl používat názvy sloupců místo indexů
    cursor = conn.cursor()
    cursor.execute("DROP TABLE condition")
    cursor.execute("CREATE TABLE condition ("+
        "_id INTEGER PRIMARY KEY AUTOINCREMENT,"+
        "lastbuilddate DATETIME,"+
        "city TEXT,"+
        "country TEXT,"+
        "region TEXT,"+
        "chill INTEGER,"+
        "direction INTEGER,"+
        "speed REAL,"+
        "sunrise TIME,"+
        "sunset TIME,"+
        "humidity INTEGER,"+
        "pressure REAL,"+
        "rising INTEGER,"+
        "visibility REAL,"+
        "title TEXT,"+
        "pubdate TEXT,"+
        "code INTEGER,"+
        "date DATE,"+
        "temp INTEGER,"+
        "text TEXT,"+
        "creatat TEXT,"+
        "changeat TEXT)")

    cursor.execute("DROP TABLE forecast")
    cursor.execute("CREATE TABLE forecast ("+
        "_id INTEGER PRIMARY KEY AUTOINCREMENT,"+
        "condate INTEGER,"+
        "code INTEGER,"+
        "date DATE,"+
        "day TEXT,"+
        "high INTEGER,"+
        "low INTEGER,"+
        "text TEXT,"+
        "creatat TEXT,"+
        "changeat TEXT)")

    #conn.close()  # toto by se mělo vždy udělat, při update načíst dtb znovu
    # pro jednoduchost zakomentováno
    
def insertCondDB(i):
    cursor.execute("INSERT INTO condition (lastbuilddate, city, country, region, chill,"+
                   "direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, title, "+
                   "pubdate, code, date, temp, text, creatat, changeat) VALUES ('" +
                   lastbuilddate[i] + "', '" + city[i] + "', '" + country[i] + "', '" + region[i] + "', "  + str(chill[i]) + ", " +
                   str(direction[i]) + ", " + str(speed[i]) + ", '" + sunrise[i] + "', '" + sunset[i] + "', " +
                   str(humidity[i]) + ", " + str(pressure[i]) + ", " + str(rising[i]) + ", " + str(visibility[i]) + ", '" + title[i] + "', '" +
                   pubdate[i] + "', " + str(code[i]) + ", '" + date[i] + "', " + str(temp[i]) + ", '" + text[i] + "', '" + creatat[i] + "', '" + changeat[i] + "')")
    conn.commit()

def insertForeDB(i):
    cursor.execute("INSERT INTO forecast (condate, code, date, day, high, low, text, creatat, changeat) VALUES ('" +
                   fcondate[i] + "', " + str(fcode[i]) + ", '" + fdate[i] + "', '" + fday[i] + "', " + str(fhigh[i]) + ", "  +
                   str(flow[i]) + ", '" + ftext[i] + "', '" + fcreatat[i] + "', '" + fchangeat[i] + "')")
    conn.commit()

readALL()
