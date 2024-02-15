import discord
import json
from discord.ext import commands
import requests
from constants import *
import tokens

class Class_v(commands.Cog):

    def __init__(self,bot):
        self.bot = bot 

    @commands.command()
    async def class_v(self,ctx):

        APICRTOKEN = tokens.getApiCrToken()
        await ctx.send("Victoires en guerres de tous les joueurs du clan :")
        f = open("./database/clan.json","r",encoding="utf-8")
        database = json.load(f)
        listeJoueurs = []

        PARAMS = {'Authorization': 'Bearer '+APICRTOKEN}

        for i in range(0,len(database['memberList'])):

            obj_i = database['memberList'][i]
            id_j = str(obj_i['tag'])
            id_j = id_j.lstrip('#')
            
            r = requests.get(url = APICRURL+"/players/%23"+id_j, auth=None, params = PARAMS)

            if r.status_code == 200:
                listeJoueurs.append(r.json())

            else:

                channel = self.bot.get_channel(DEBUG_CHAN)
                await channel.send("[!T class_v] Erreur requête")
                return

        string = "```"
        listeJoueursTriee = []

        for i in range(0,len(listeJoueurs)):

            for j in range(0,len(listeJoueurs[i]['badges'])):

                if listeJoueurs[i]['badges'][j]['name'] == "ClanWarWins":

                    listeJoueursTriee.append(str(listeJoueurs[i]['badges'][j]['progress']) +" | "+ str(listeJoueurs[i]['name']) + "\n")
    
        listeJoueursTriee.sort(key = lambda x: int(x.split(" |")[0]),reverse=True)

        for i in range(0,len(listeJoueursTriee)):

            string = string + listeJoueursTriee[i]

        string = string + "```"
        await ctx.send(string)

async def setup(bot):
    await bot.add_cog(Class_v(bot))
