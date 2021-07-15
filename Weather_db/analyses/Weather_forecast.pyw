
import sqlite3



db = "Weather_db.db"

'''This script records your device's orientation (accelerometer data) for 5 seconds, and then renders a simple plot of the gravity vector, using matplotlib.'''

import matplotlib.pyplot as plt
from time import sleep
import math

def readDB():
    global conn, cursor, results
    conn = sqlite3.connect(db)    # všude je potřeba testovat exceptions
    conn.row_factory = sqlite3.Row          # abych mohl používat názvy sloupců místo indexů
    cursor = conn.cursor()
    cursor.execute("SELECT t.day, t.low, t.high" \
                   " FROM forecast t" \
                   " WHERE t._id = (SELECT max(t2._id) FROM forecast t2 WHERE t2.date= t.date and t.creatat >= date('now'))")
                   #" WHERE t._id = (SELECT max(t2._id) FROM forecast t2 WHERE t2.date= t.date and t.creatat >= date('now','-1 day'))")
    results = cursor.fetchall()         # načte všechnyřádky ze selectu
  
    conn.close()  # toto by se mělo vždy udělat, při update načíst dtb znovu
    # pro jednoduchost zakomentováno


            
def main():

    readDB()

    for r in results:
        print(r["day"], r["low"], r["high"])

    #console.alert('Motion Plot', 'When you tap Continue, accelerometer (motion) data will be recorded for 5 seconds.', 'Continue')
    #motion.start_updates()
    sleep(0.2)
    print('Capturing motion data...')
    num_samples = 628
    data = []
    #for i in range(num_samples):
    #	sleep(0.05)
    #	g = motion.get_gravity()
    #	data.append(g)
    #motion.stop_updates()

    #print(len(data))
    #print(data[0])

    a = lambda i: ((i % 2 -0.5)*2)
    b = lambda i: (i % 2)
    for i in range(10):
            #print(a(i))
            pass

    for i in range(1,629):
            data.append((i/629*a(i),-i/(629*2),math.sin(i/100)*b(i)))

    print('Capture finished, plotting...')

    print(list(zip(['low','high'], 'gb', ['low','high'])))

    tmin = min(r["low"] for r in results) - 1
    tmax = max(r["high"] for r in results) + 1
    
    #x_values = [x for x in range(10)]
    x_values = [str(i)+"_"+results[i]["day"] for i in range(len(results))]
    
    for i, color, label in zip(['high','low'], 'rb', ['high','low']):
            plt.plot(x_values, [r[i] for r in results], color, label=label, lw=2)
    plt.grid(True)
    plt.xlabel('date')
    plt.ylabel('temp °C')
    plt.gca().set_ylim([tmin, tmax])
    plt.legend()
    plt.show()
    
##    x_values = [x/100 for x in range(num_samples)]
##    for i, color, label in zip(range(3), 'rgb', ['první','druhá','sinus']):
##            plt.plot(x_values, [g[i] for g in data], color, label=label, lw=2)
##    plt.grid(True)
##    plt.xlabel('pi')
##    plt.ylabel('value')
##    plt.gca().set_ylim([-1.0, 1.0])
##    plt.legend()
##    plt.show()

if __name__ == '__main__':
	main()
