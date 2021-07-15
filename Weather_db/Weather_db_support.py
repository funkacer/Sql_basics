#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.17
# In conjunction with Tcl version 8.6
#    Oct 08, 2018 02:10:19 PM CEST  platform: Windows NT

import sys, sqlite3, time, weather_update

import os

script_directory = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(script_directory, "Weather_db.db")

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def set_Tk_var():
    global dateTxtVar
    dateTxtVar = StringVar()
    global textTxtVar
    textTxtVar = StringVar()
    global windTxt1Var
    windTxt1Var = StringVar()
    global windTxt2Var
    windTxt2Var = StringVar()
    global pressTxt1Var
    pressTxt1Var = StringVar()
    global pressTxt2Var
    pressTxt2Var = StringVar()
    global tempTxt1Var
    tempTxt1Var = StringVar()
    global tempTxt2Var
    tempTxt2Var = StringVar()
    global forecastTxt1Var
    forecastTxt1Var = StringVar()
    global forecastTxt2Var
    forecastTxt2Var = StringVar()
    global forecastTxt3Var
    forecastTxt3Var = StringVar()
    global forecastTxt4Var
    forecastTxt4Var = StringVar()
    global forecastTxt5Var
    forecastTxt5Var = StringVar()
    global forecastTxt6Var
    forecastTxt6Var = StringVar()
    global forecastTxt7Var
    forecastTxt7Var = StringVar()
    global forecastTxt8Var
    forecastTxt8Var = StringVar()
    global forecastTxt9Var
    forecastTxt9Var = StringVar()
    global forecastTxt10Var
    forecastTxt10Var = StringVar()
    global creatatTxtVar
    creatatTxtVar = StringVar()
    global changeatTxtVar
    changeatTxtVar = StringVar()
    global updateLblVar
    updateLblVar = StringVar()
    global visTxtVar
    visTxtVar = StringVar()
    global humTxtVar
    humTxtVar = StringVar()
    global sunTxt1Var
    sunTxt1Var = StringVar()
    global sunTxt2Var
    sunTxt2Var = StringVar()

def btnFirst_Click(p1):
##    print('Weather_db_support.btnFirst_Click')
##    print('p1 = {0}'.format(p1))
##    sys.stdout.flush()
    global currentCondition
    currentCondition = 0
    fillForm(currentCondition)

def btnLast_Click(p1):
##    print('Weather_db_support.btnLast_Click')
##    print('p1 = {0}'.format(p1))
##    sys.stdout.flush()
    global currentCondition
    currentCondition = len(conditions)-1
    fillForm(currentCondition)

def btnNext_Click(p1):
##    print('Weather_db_support.btnNext_Click')
##    print('p1 = {0}'.format(p1))
##    sys.stdout.flush()
    global currentCondition
    if currentCondition < len(conditions)-1: currentCondition += 1
    fillForm(currentCondition)

def btnPrev_Click(p1):
##    print('Weather_db_support.btnPrev_Click')
##    print('p1 = {0}'.format(p1))
##    sys.stdout.flush()
    global currentCondition
    if currentCondition > 0: currentCondition -= 1
    fillForm(currentCondition)

def btnUpdate_Click(p1):
##    print('Weather_db_support.btnUpdate_Click')
##    print('p1 = {0}'.format(p1))
##    sys.stdout.flush()
    global currentCondition
    weather_update.updateALL()
    readDB()
    fillForm(currentCondition)
    updateLblVar.set("Update OK")

def readDB():
    global conn, cursor, records, conditions, currentCondition, forecasts, currentForecast
    conn = sqlite3.connect(db)    # všude je potřeba testovat exceptions
    conn.row_factory = sqlite3.Row          # abych mohl používat názvy sloupců místo indexů
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM condition")
    conditions = cursor.fetchall()         # načte všechnyřádky ze selectu
    #currentCondition = 0                   # index aktuálního rekordu, předp. alespoň 1
    currentCondition = len(conditions)-1
    cursor.execute("SELECT * FROM forecast")
    forecasts = cursor.fetchall()         # načte všechnyřádky ze selectu
    currentForecast = 0                   # index aktuálního rekordu, předp. alespoň 1
  
    conn.close()  # toto by se mělo vždy udělat, při update načíst dtb znovu
    # pro jednoduchost zakomentováno

def fillForm(index):
    #txtIDVar.set(records[index][0])     # takto při používání indexů sloupců
    dateTxtVar.set(conditions[index]["date"])
    textTxtVar.set(conditions[index]["text"])
    tempTxt1Var.set(conditions[index]["temp"])
    diff = 0
    if index >= 1: diff = conditions[index]["temp"] - conditions[index-1]["temp"]
    difs = str(diff)
    if diff >= 0: difs = "nárůst " + difs
    tempTxt2Var.set(difs)
    visTxtVar.set(conditions[index]["visibility"])
    humTxtVar.set(conditions[index]["humidity"])
    pressTxt1Var.set(conditions[index]["pressure"])
    pressTxt2Var.set(conditions[index]["rising"])
    windTxt1Var.set(conditions[index]["speed"])
    windTxt2Var.set(conditions[index]["direction"])
    sunTxt1Var.set(conditions[index]["sunrise"])
    sunTxt2Var.set(conditions[index]["sunset"])
    creatatTxtVar.set(conditions[index]["creatat"])
    changeatTxtVar.set(conditions[index]["changeat"])
    forecast = []
    for f in forecasts:
        if f ["condate"] == conditions[index]["date"]: forecast.append(f)
    forecast1 = forecast[-10]["day"] + " lo:" + str(forecast[-10]["low"]) + " hi:" + str(forecast[-10]["high"]) + " " + forecast[-10]["text"]
    forecast2 = forecast[-9]["day"] + " lo:" + str(forecast[-9]["low"]) + " hi:" + str(forecast[-9]["high"]) + " " + forecast[-9]["text"]
    forecast3 = forecast[-8]["day"] + " lo:" + str(forecast[-8]["low"]) + " hi:" + str(forecast[-8]["high"]) + " " + forecast[-8]["text"]
    forecast4 = forecast[-7]["day"] + " lo:" + str(forecast[-7]["low"]) + " hi:" + str(forecast[-7]["high"]) + " " + forecast[-7]["text"]
    forecast5 = forecast[-6]["day"] + " lo:" + str(forecast[-6]["low"]) + " hi:" + str(forecast[-6]["high"]) + " " + forecast[-6]["text"]
    forecast6 = forecast[-5]["day"] + " lo:" + str(forecast[-5]["low"]) + " hi:" + str(forecast[-5]["high"]) + " " + forecast[-5]["text"]
    forecast7 = forecast[-4]["day"] + " lo:" + str(forecast[-4]["low"]) + " hi:" + str(forecast[-4]["high"]) + " " + forecast[-4]["text"]
    forecast8 = forecast[-3]["day"] + " lo:" + str(forecast[-3]["low"]) + " hi:" + str(forecast[-3]["high"]) + " " + forecast[-3]["text"]
    forecast9 = forecast[-2]["day"] + " lo:" + str(forecast[-2]["low"]) + " hi:" + str(forecast[-2]["high"]) + " " + forecast[-2]["text"]
    forecast10 = forecast[-1]["day"] + " lo:" + str(forecast[-1]["low"]) + " hi:" + str(forecast[-1]["high"]) + " " + forecast[-1]["text"]
    forecastTxt1Var.set(forecast1)
    forecastTxt2Var.set(forecast2)
    forecastTxt3Var.set(forecast3)
    forecastTxt4Var.set(forecast4)
    forecastTxt5Var.set(forecast5)
    forecastTxt6Var.set(forecast6)
    forecastTxt7Var.set(forecast7)
    forecastTxt8Var.set(forecast8)
    forecastTxt9Var.set(forecast9)
    forecastTxt10Var.set(forecast10)
    updateLblVar.set("")

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

    readDB()
    fillForm(currentCondition)

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None
    
if __name__ == '__main__':
    import Weather_db
    Weather_db.vp_start_gui()


