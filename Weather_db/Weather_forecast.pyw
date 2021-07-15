import sqlite3

import datetime, math

import os

script_directory = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(script_directory, "Weather_db.db")

'''This script records your device's orientation (accelerometer data) for 5 seconds, and then renders a simple plot of the gravity vector, using matplotlib.'''

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.gridspec import GridSpec

img_sunny = mpimg.imread('sunny.png')
img_pcloudy = mpimg.imread('partly_cloudy.png')
img_mcloudy = mpimg.imread('mostly_cloudy.png')
img_breezy = mpimg.imread('breezy.png')
img_rainy = mpimg.imread('rainy.png')

def readDB():
    global conn, cursor, results, conds
    conn = sqlite3.connect(db)    # všude je potřeba testovat exceptions
    conn.row_factory = sqlite3.Row          # abych mohl používat názvy sloupců místo indexů
    cursor = conn.cursor()
    cursor.execute("SELECT t.date, t.day, t.low, t.high, t.text" \
                   " FROM forecast t" \
                   " WHERE t._id = (SELECT max(t2._id) FROM forecast t2 WHERE t2.date= t.date and t.creatat >= date('now'))")
                   #" WHERE t._id = (SELECT max(t2._id) FROM forecast t2 WHERE t2.date= t.date and t.creatat >= date('now','-1 day'))")
    results = cursor.fetchall()         # načte všechnyřádky ze selectu

    cursor.execute("SELECT date, sunrise, sunset, speed, direction, temp, pressure, text FROM condition")
                   #" WHERE t._id = (SELECT max(t2._id) FROM forecast t2 WHERE t2.date= t.date and t.creatat >= date('now','-1 day'))")
    conds = cursor.fetchall()         # načte všechnyřádky ze selectu
    
    conn.close()  # toto by se mělo vždy udělat, při update načíst dtb znovu
    # pro jednoduchost zakomentováno
            
def main():

    readDB()

    res = []
    for r in results:
        print(r["day"], r["low"], r["high"])
        res.append(dict(day=r["day"],low=r["low"],high=r["high"],mid=(r["high"]+r["low"])/2))

    sun = conds[-1]["sunrise"]
    #sun = "12:8 am"
    pos = sun.find(':')
    if pos == 1:
        sunr = str(int(sun[:1]))
        if sun[-2:] == "pm" and int(sun[:1]) < 12: sunr = str(int(sun[:1]) + 12)
        if int(sun[2:4]) < 10:
            sunr += ":0" + str(int(sun[2:4]))
        else:
            sunr += ":" + str(int(sun[2:4]))
    elif pos == 2:
        sunr = str(int(sun[:2]))
        if int(sun[3:5]) < 10:
            sunr += ":0" + str(int(sun[3:5]))
        else:
            sunr += ":" + str(int(sun[3:5]))  
    else:
        sunr = "#"


    sun = conds[-1]["sunset"]
    #sun = "12:8 pm"
    pos = sun.find(':')
    if pos == 1:
        suns = str(int(sun[:1]))
        if sun[-2:] == "pm" and int(sun[:1]) < 12: suns = str(int(sun[:1]) + 12)
        if int(sun[2:4]) < 10:
            suns += ":0" + str(int(sun[2:4]))
        else:
            suns += ":" + str(int(sun[2:4]))
    elif pos == 2:
        suns = str(int(sun[:2]))
        if int(sun[3:5]) < 10:
            suns += ":0" + str(int(sun[3:5]))
        else:
            suns += ":" + str(int(sun[3:5]))  
    else:
        suns = "#"
    
    speed=str(round(conds[-1]["speed"], 1))
    direct=str(conds[-1]["direction"])
    temp=str(conds[-1]["temp"])

    tmin = min(r["low"] for r in results) - 1
    tmax = max(r["high"] for r in results) + 1

    mes = []
    mes.append(dict(months="Jan",monthn="01"))
    mes.append(dict(months="Feb",monthn="02"))
    mes.append(dict(months="Mar",monthn="03"))
    mes.append(dict(months="Apr",monthn="04"))
    mes.append(dict(months="May",monthn="05"))
    mes.append(dict(months="Jun",monthn="06"))
    mes.append(dict(months="Jul",monthn="07"))
    mes.append(dict(months="Aug",monthn="08"))
    mes.append(dict(months="Sep",monthn="09"))
    mes.append(dict(months="Oct",monthn="10"))
    mes.append(dict(months="Nov",monthn="11"))
    mes.append(dict(months="Dec",monthn="12"))

    cons = []
    i = 0
    for c in conds:
        #print(c["date"], c["temp"], c["pressure"])
        i += 1
        cons.append(dict(date=c["date"],temp=c["temp"],pressure=c["pressure"]))

    x_values = []
    cons_fin = []
    for i in range(len(cons)):
        #print (cons[i]["date"][23:25])
        dat = cons[i]["date"]
        for m in mes:
            if dat[8:11] == m["months"] and (dat[23:25] == "AM" and dat[17:19] != '12' or dat[23:25] == "PM" and dat[17:19] == '12'):
                dat =  dat[12:16] + "-" + m["monthn"] + "-" + dat[5:8] + dat[17:22]
            elif dat[8:11] == m["months"] and dat[23:25] == "PM":
                dat =  dat[12:16] + "-" + m["monthn"] + "-" + dat[5:8] + str(int(dat[17:19])+12) + ":" + dat[20:22]
            elif dat[8:11] == m["months"] and (dat[23:25] == "AM" and dat[17:19] == '12'):
                dat =  dat[12:16] + "-" + m["monthn"] + "-" + "00:" + dat[17:22]
        b = datetime.datetime.now()
        f = "%Y-%m-%d %H:%M"
        a = b - datetime.datetime.strptime(dat, f)
        if math.floor(a.total_seconds() / 3600) <= 12:
            x_values.append(str(-1*(math.floor(a.total_seconds() / 3600))))
            cons_fin.append(dict(date=dat,temp=cons[i]["temp"],pressure=cons[i]["pressure"]))
            #dat = str((math.floor((a.seconds) / 3600)))
            print(str(math.floor(a.total_seconds()/3600)), dat, cons[i]["temp"], cons[i]["pressure"])

    # úprava tlaku cons[i]["pressure"])/10-3330)
    mt = 0
    mp = 0
    for cf in cons_fin:
        mt += cf["temp"]
        mp += cf["pressure"]/10
    mt = mt / len(cons_fin)
    mp = mp / len(cons_fin)
    konst = mp - mt
    print(konst)
    for cf in cons_fin:
        cf["pressure"] = cf["pressure"]/10 - konst
    

    # match on arbitrary function
    def myfunc(x):
        return hasattr(x, 'set_color') and not hasattr(x, 'set_facecolor')

    def format_axes(fig):
        for i, ax in enumerate(fig.axes):
            #ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
            if i == 0: ax.tick_params(labelbottom=True, labelleft=True)
            if i == 2: ax.tick_params(labelbottom=True, labelleft=True)
            if i == 1 or i > 2: ax.tick_params(labelbottom=False, labelleft=False)
            pass

    fig = plt.figure(constrained_layout=True)
    gs = GridSpec(5, 10, figure=fig)

    plt.subplot(gs.new_subplotspec((0, 0), rowspan=2, colspan=6))
    for i, color, label in zip(['temp','pressure'], ['r','o-'], ['temp','pressure']):
            plt.plot(x_values, [c[i] for c in cons_fin], color, label=label, lw=2)
    plt.grid(True)
    #plt.gca().set_ylim([-40, 40])
    plt.legend()
    plt.title('Temp: ' + temp + '°C, Wind: ' + speed + ' (' + direct + '°)'+'\n')
    plt.ylabel('press +' + str(round(konst)) + ' mb/10')

    text = conds[-1]["text"]
    #text = "Rainy"
    img = img_rainy
    if "breezy" in text.lower(): img = img_breezy
    elif "partly cloudy" in text.lower(): img = img_pcloudy
    elif "cloudy" in text.lower(): img = img_mcloudy
    elif "sunny" in text.lower() or "clear" in text.lower(): img = img_sunny
    else: img = img_rainy

    a = plt.subplot(gs.new_subplotspec((0, 6), rowspan=2, colspan=5))
    a.set_title('Sun: ' + sunr + ' - ' + suns+'\n')
    a.set_axis_off()
    a.imshow(img)
    a.text(520,0,str('Now'),
    ha='center', va='center',style='italic').set_color('blue')

    plt.subplot(gs.new_subplotspec((2, 0), rowspan=2, colspan=10))
    x_values = [res[i]["day"] for i in range(len(res))]
    for i in range(len(x_values)):
        if i >= 7: x_values[i]= " " + x_values[i]
    for i, color, label in zip(['high','mid','low'], ['r','g^','b--'], ['high','mid','low']):
            plt.plot(x_values, [r[i] for r in res], color, label=label, lw=2)
    plt.grid(True)
    plt.xlabel('Forecast')
    plt.ylabel('temp °C')
    plt.gca().set_ylim([tmin, tmax])
    plt.legend()

    for i in range(10):
        text = results[i]["text"]
        print(results[i]["date"], text)
        img = img_rainy
        if "breezy" in text.lower(): img = img_breezy
        elif "partly cloudy" in text.lower(): img = img_pcloudy
        elif "cloudy" in text.lower(): img = img_mcloudy
        elif "sunny" in text.lower() or "clear" in text.lower(): img = img_sunny
        else: img = img_rainy
        a = plt.subplot(gs.new_subplotspec((4, i)))
        a.set_axis_off()
        a.imshow(img)

    dat = cons[-1]["date"]
    print(dat)
    for m in mes:
        if dat[8:11] == m["months"] and (dat[23:25] == "AM" and dat[17:19] != '12' or dat[23:25] == "PM" and dat[17:19] == '12'):
            datum =  dat[12:16] + "-" + m["monthn"] + "-" + dat[5:7]
            cas = str(int(dat[17:19])) + ":" + dat[20:22]
        elif dat[8:11] == m["months"] and dat[23:25] == "PM":
            datum =  dat[12:16] + "-" + m["monthn"] + "-" + dat[5:7]
            cas = str(int(dat[17:19])+12) + ":" + dat[20:22]
        elif dat[8:11] == m["months"] and (dat[23:25] == "AM" and dat[17:19] == '12'):
            datum =  dat[12:16] + "-" + m["monthn"] + "-" + dat[5:]
            cas = '0' + ":" + dat[20:22]
    print(datum, cas)
    
    fig.suptitle('Date: ' + datum + ', Time: ' + cas + '\n').set_color('blue')
    format_axes(fig)

    plt.show()

if __name__ == '__main__':
	main()
