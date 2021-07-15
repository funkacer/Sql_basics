
import sqlite3

import datetime
import time

import json

import urllib.request, urllib.error, urllib.parse

import os

script_directory = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(script_directory, "Weather_db.db")

def updateALL():

    global lastbuilddate, city, country, region, chill, \
    direction, speed, sunrise, sunset, humidity, pressure, \
    rising, visibility, title, pubdate, code, date, temp, text, \
    creatat, changeat, fcode, fdate, fday, fhigh, flow, ftext, fcreatat, fchangeat

    now = str(datetime.datetime.now())
    now = now[:now.find(".")]
    
    try:
        query = urllib.parse.quote("select * from weather.forecast where u='c' and woeid in (select woeid from geo.places(1) where text='Praha')")
        host = 'https://query.yahooapis.com/v1/public/yql?q=%s&format=json' % (query)
        #print(host)
        html = urllib.request.urlopen(host).read()
        #print(html)

    except (urllib.error.URLError) as err:
        print (err)

    try:
        data = json.loads(html)
        #print(data)
        print()
        lastbuilddate = data["query"]["results"]["channel"]["lastBuildDate"]
        print("lastbuilddate:", lastbuilddate)
        city = data["query"]["results"]["channel"]["location"]["city"]
        print("city:", city)
        country = data["query"]["results"]["channel"]["location"]["country"]
        print("country:", country)
        region = data["query"]["results"]["channel"]["location"]["region"]
        print("region:", region)
        chill = data["query"]["results"]["channel"]["wind"]["chill"]
        print("chill:", chill)
        direction = data["query"]["results"]["channel"]["wind"]["direction"]
        print("direction:", direction)
        speed = data["query"]["results"]["channel"]["wind"]["speed"]
        print("speed:", speed)
        sunrise = data["query"]["results"]["channel"]["astronomy"]["sunrise"]
        print("sunrise:", sunrise)
        sunset = data["query"]["results"]["channel"]["astronomy"]["sunset"]
        print("sunset:", sunset)
        humidity = data["query"]["results"]["channel"]["atmosphere"]["humidity"]
        print("humidity:", humidity)
        pressure = data["query"]["results"]["channel"]["atmosphere"]["pressure"]
        print("pressure:", pressure)
        rising = data["query"]["results"]["channel"]["atmosphere"]["rising"]
        print("rising:", rising)
        visibility = data["query"]["results"]["channel"]["atmosphere"]["visibility"]
        print("visibility:", visibility)
        title = data["query"]["results"]["channel"]["item"]["title"]
        print("title:", title)
        pubdate = data["query"]["results"]["channel"]["item"]["pubDate"]
        print("pubDate:", pubdate)
        code = data["query"]["results"]["channel"]["item"]["condition"]["code"]
        print("code:", code)    
        date = data["query"]["results"]["channel"]["item"]["condition"]["date"]
        print("date:", date)
        temp = data["query"]["results"]["channel"]["item"]["condition"]["temp"]
        print("temp:", temp)  
        text = data["query"]["results"]["channel"]["item"]["condition"]["text"]
        print("text:", text)  
        creatat = now
        print()
        fcode = []
        fdate = []
        fday = []
        fhigh = []
        flow = []
        ftext = []
        fcreatat = []
        forecast = data["query"]["results"]["channel"]["item"]["forecast"]
        for f in forecast:
            fcode.append(f["code"])
            fdate.append(f["date"])
            fday.append(f["day"])
            fhigh.append(f["high"])
            flow.append(f["low"])
            ftext.append(f["text"])
            fcreatat.append(now)
        for i in range(0, len(forecast)):
            print(i, "fcode:", fcode[i], "fdate:", fdate[i], "fday:", fday[i], "fhigh:", fhigh[i], "flow:", flow[i], "ftext:", ftext[i], "fcreatat:", fcreatat[i])

        readDB()
        #když existuje => upadte, jinak insert

        update_cond = 0
        for condition in conditions:
            if condition["date"] == date:
                update_cond = condition["_id"]
        print("Zpráva:", update_cond)
        if update_cond > 0:
            updateCondDB(update_cond)
        else:
            insertCondDB()
            pass

        for i in range (0, len(fdate)):
            update_fore = 0
            for forecast in forecasts:
                if forecast["condate"] == date and forecast["date"] == fdate[i]:
                    update_fore = forecast["_id"]
            if update_fore > 0:
                updateForeDB(update_fore, i)
            else:
                insertForeDB(i)
                pass

        print(len(conditions))
        print(len(forecasts))
    
    except Exception as e:
        print(e)

    conn.close()
    
    print()
    print("Waiting for 5 seconds...")
    time.sleep(1)

def initDB():
    conn = sqlite3.connect(db)    # všude je potřeba testovat exceptions
    conn.row_factory = sqlite3.Row          # abych mohl používat názvy sloupců místo indexů
    cursor = conn.cursor()
    #cursor.execute("DROP TABLE condition")
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

    #cursor.execute("DROP TABLE forecast")
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

    conn.close()  # toto by se mělo vždy udělat, při update načíst dtb znovu
    # pro jednoduchost zakomentováno  

def readDB():
    global conn, cursor, records, conditions, currentCondition, forecasts, currentForecast
    conn = sqlite3.connect(db)    # všude je potřeba testovat exceptions
    conn.row_factory = sqlite3.Row          # abych mohl používat názvy sloupců místo indexů
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM condition")
    conditions = cursor.fetchall()         # načte všechnyřádky ze selectu
    currentCondition = 0                   # index aktuálního rekordu, předp. alespoň 1

    cursor.execute("SELECT * FROM forecast")
    forecasts = cursor.fetchall()         # načte všechnyřádky ze selectu
    currentForecast = 0                   # index aktuálního rekordu, předp. alespoň 1
  
    #conn.close()  # toto by se mělo vždy udělat, při update načíst dtb znovu
    # pro jednoduchost zakomentováno


def updateCondDB(update_cond):
    cursor.execute("UPDATE condition SET lastbuilddate='" + lastbuilddate + "', city='" + city + "', country='" + country +
                   "', region='" + region + "', chill=" + str(chill) + ", direction=" + str(direction) +
                   ", speed=" + str(speed) + ", sunrise='" + sunrise + "', sunset='" + sunset + "', humidity=" + str(humidity) +
                   ", pressure=" + str(pressure) + ", rising=" + str(rising) + ", visibility=" + str(visibility) + ", title='" + title +
                   "', pubdate='" + pubdate + "', code=" + str(code) + ", date='" + date + "', temp=" + str(temp) +
                   ", text='" + text + "', changeat='" + creatat + "' WHERE _id = " + str(update_cond))
    conn.commit()

def insertCondDB():
    cursor.execute("INSERT INTO condition (lastbuilddate, city, country, region, chill,"+
                   "direction, speed, sunrise, sunset, humidity, pressure, rising, visibility, title, "+
                   "pubdate, code, date, temp, text, creatat, changeat) VALUES ('" +
                   lastbuilddate + "', '" + city + "', '" + country + "', '" + region + "', "  + str(chill) + ", " +
                   str(direction) + ", " + str(speed) + ", '" + sunrise + "', '" + sunset + "', " +
                   str(humidity) + ", " + str(pressure) + ", " + str(rising) + ", " + str(visibility) + ", '" + title + "', '" +
                   pubdate + "', " + str(code) + ", '" + date + "', " + str(temp) + ", '" + text + "', '" + creatat + "', '" + creatat + "')")
    conn.commit()


def updateForeDB(update_fore, i):
    cursor.execute("UPDATE forecast SET condate='" + date + "', code=" + str(fcode[i]) + ", date='" + fdate[i] + "', day='" + fday[i] +
                   "', high=" + str(fhigh[i]) + ", low=" + str(flow[i]) + ", text='" + ftext[i] +
                   "', changeat='" + fcreatat[i] + "' WHERE _id = " + str(update_fore))
    conn.commit()

def insertForeDB(i):
    cursor.execute("INSERT INTO forecast (condate, code, date, day, high, low, text, creatat, changeat) VALUES ('" +
                   date + "', " + str(fcode[i]) + ", '" + fdate[i] + "', '" + fday[i] + "', " + str(fhigh[i]) + ", "  +
                   str(flow[i]) + ", '" + ftext[i] + "', '" + fcreatat[i] + "', '" + fcreatat[i] + "')")
    conn.commit()


# toto odkřížkovat pro init:
#initDB()

#updateALL()

#a = input()

