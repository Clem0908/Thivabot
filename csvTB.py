import os
import requests
import tokens
import json
from constants import *
import discord
import datetime

PATH = "./database/inactifs-"
EXT = ".csv"
MONTH = str(datetime.datetime.today().month)
YEAR = str(datetime.datetime.today().year)

def request():
    APICRTOKEN = tokens.getApiCrToken()
    id_c = "LPRYYG"
    PARAMS = {'Authorization': 'Bearer '+APICRTOKEN}
    r = requests.get(url = APICRURL+"/clans/%23"+id_c+"/currentriverrace", auth=None, params = PARAMS)

    if r.status_code == 200:
        data = r.json()
        return data
    return None

def insert_csv():

    fd = open(PATH+MONTH+YEAR+EXT,"w")
    data = request()
    f = open("./database/clan.json","r")
    data1 = json.load(f)
    l = []

    for i in range(0,len(data1['memberList'])):
        l.append(str(data1['memberList'][i]['tag']))

    for i in range(0,len(data['clan']['participants'])): 
        p = data['clan']['participants'][i]
        
        # Joueur dans le clan
        if str(p['tag']) in l:
            unusedDecks = 4 - int(str(p['decksUsedToday']))
            percentage = (unusedDecks * 100) / 64
            INSERT = str(p['name'])+","+str(p['tag'])+","+str(unusedDecks)+","+str(percentage)+"\n"
            fd.write(INSERT)

    fd.close()
    f.close()
    return

def read_csv():

    fd = open(PATH+MONTH+YEAR+EXT,"r")
    string = fd.read()

    i = 0
    j = 0
    p_list = []
    valuesCsv = ""
    cpt = 0
    for c in string:
        if c != '\n':
            if c != ',':
                valuesCsv += c
            else:
                if cpt == 2:
                    oldDecksUnused = int(valuesCsv)
                    valuesCsv = ""
                cpt = cpt + 1
                valuesCsv = ""
        else:
            cpt = 0
            valuesCsv = ""


    fd.close()
    return p_list

def csvTB():

    if os.path.exists(PATH+MONTH+YEAR+EXT) == False:

        os.system("touch "+PATH+MONTH+YEAR+EXT)
        fd = open(PATH+MONTH+YEAR+EXT,"w")
        fd.write("Joueur,ID,Combats manqués,Pourcentage d'inactivité\n")
        fd.close()
        insert_csv()
        return
    
    else:

        p_list = read_csv()
        print(p_list)

    return

csvTB()
