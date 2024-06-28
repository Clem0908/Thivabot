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
    print("csvTB.request() : endpoint currentriverrace failed")
    return None

def insert_csv():

    fd = open(PATH+MONTH+YEAR+EXT,"w")
    fd.write("Joueur,ID,Combats manqués,Pourcentage d'inactivité\n")
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
    fd.close()

    tupleList = []
    tupleStr = ""

    for c in string:
        if c != '\n':
            tupleStr += c
        else:
            tupleStr += '\n'
            tupleList.append(tupleStr)
            tupleStr = ""
    nameStr = ""
    IDStr = ""
    unusedDecksStr = ""
    missedPercentage = ""

    data = request()
    f = open("./database/clan.json","r")
    data1 = json.load(f)
    l = []

    for i in range(0,len(data1['memberList'])):
        l.append(str(data1['memberList'][i]['tag']))
    
    fd = open(PATH+MONTH+YEAR+EXT,"w")
    fd.write("Joueur,ID,Combats manqués,Pourcentage d'inactivité\n")
    
    for s in tupleList:
        s = s.split(',') 
        nameStr = s[0]
        IDStr = s[1]
        unusedDecksStr = s[2]
        missedPercentage = s[3]
        # Joueur dans le clan
        for i in range(0,len(data['clan']['participants'])):
            p = data['clan']['participants'][i]
            if str(p['tag']) == IDStr and str(p['tag']) in l:
                unusedDecks = 4 - int(str(p['decksUsedToday']))
                unusedDecks = unusedDecks + int(unusedDecksStr)
                percentage = (unusedDecks * 100) / 64
                INSERT = nameStr+","+IDStr+","+str(unusedDecks)+","+str(percentage)+"\n"
                fd.write(INSERT)

    fd.close()
    f.close()
    return 

def csvTB():

    if os.path.exists(PATH+MONTH+YEAR+EXT) == False:
        
        print("csvTB.csvTB() : file inactifs-"+MONTH+YEAR+EXT+" does not exist, creation...")
        os.system("touch "+PATH+MONTH+YEAR+EXT)
        fd = open(PATH+MONTH+YEAR+EXT,"w")
        fd.write("Joueur,ID,Combats manqués,Pourcentage d'inactivité\n")
        fd.close()
        insert_csv()
        return
    
    else:
        
        print("csvTB.csvTB() : updating csv file...")
        read_csv()

    return
