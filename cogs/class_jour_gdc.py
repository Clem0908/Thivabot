import discord
from discord.ext import commands
import requests
import asyncio
import json
from constants import *
import tokens

class Classjourgdc(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def class_jour_gdc(self,ctx):
        
        APICRTOKEN = tokens.getApiCrToken()
        
        id_c = "LPRYYG"
        PARAMS = {'Authorization': 'Bearer '+APICRTOKEN}
        r = requests.get(url = APICRURL+"/clans/%23"+id_c+"/currentriverrace", auth=None, params = PARAMS)
    
        if r.status_code == 200:
           
            f = open("./database/clan.json","r",encoding="utf-8")
            dbLog = json.load(f)
            f.close()

            await ctx.send("Classement de GDC du jour:")
            data = r.json()

            if str(data['periodType']) == "training":

                await ctx.send("Nous sommes en jour d'entraînement")
                return


            string = "```"
            listeJoueurs = []

            joueursPresents = ""
            for i in range(0,len(dbLog['memberList'])):
                joueursPresents = joueursPresents+str(dbLog['memberList'][i]['tag'])+";"

            for i in range(0,len(data['clan']['participants'])):

                obj_i = data['clan']['participants'][i]
                # Le joueur est dans le clan
                if obj_i['tag'] in joueursPresents:
                    listeJoueurs.append(str(obj_i['fame']) + " | "+str(obj_i['name']))

            listeJoueurs.sort(key = lambda x: int(x.split(" |")[0]),reverse=True)

            for i in range(0,len(listeJoueurs)):

                string = string + str(listeJoueurs[i]) + "\n"
                if len(string) > 1000:
                    string = string + "```"
                    await ctx.send(string)
                    string = ""
                    string = "```"

            string = string + "```"
            await ctx.send(string)
            
            await ctx.send("TOP 20:")
            string = "```"

            for i in range(0,20):

                string = string + str(listeJoueurs[i]) + "\n"

            string = string + "```"
            await ctx.send(string)

        elif r.status_code == 503:

            channel = self.bot.get_channel(DEBUG_CHAN)
            await channel.send("[!T class_jour_gdc] Erreur 503 : service indisponible")
            return

        else:

            channel = self.bot.get_channel(DEBUG_CHAN)
            await channel.send("[!T class_jour_gdc] Erreur requête")
            return

async def setup(bot):
    await bot.add_cog(Classjourgdc(bot))
