import discord
import requests
import json
from discord.ext import commands
from constants import *
import tokens

class Bateau(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def bateau(self,ctx):

        APICRTOKEN = tokens.getApiCrToken()
       
        id_c = "LPRYYG"
        PARAMS = {'Authorization': 'Bearer '+APICRTOKEN}
        r = requests.get(url = APICRURL+"/clans/%23"+id_c+"/currentriverrace", auth=None, params = PARAMS)
    
        if r.status_code == 200:
            
            await ctx.send("Classement des clans, jour actuel :")

            data = r.json()
            listeClans = []
            decks = 0
            string = "```"

            if str(data['periodType']) == "warDay":

                for i in range(0,len(data['clans'])):

                    obj_i = data['clans'][i]
                    for j in range(0,len(obj_i['participants'])):

                        obj_j = obj_i['participants'][j]
                        decks = decks + int(obj_j['decksUsedToday'])
                    
                    listeClans.append(str(data['clans'][i]['periodPoints'])+" | "+str(data['clans'][i]['name'])+" | "+str(decks)+" decks utilisés"+"\n")
                    decks = 0

                listeClans.sort(key = lambda x: int(x.split(" |")[0]),reverse=True)

                for i in range(0,len(listeClans)):

                    string = string + listeClans[i]

                string = string + "```"
                await ctx.send(string)

            elif str(data['periodType']) == "colosseum":

                for i in range(0,len(data['clans'])):

                    obj_i = data['clans'][i]
                    for j in range(0,len(obj_i['participants'])):

                        obj_j = obj_i['participants'][j]
                        decks = decks + int(obj_j['decksUsedToday'])

                    listeClans.append(str(data['clans'][i]['fame'])+" | "+str(data['clans'][i]['name'])+" | "+str(decks)+" decks utilisés"+"\n")
                    decks = 0

                listeClans.sort(key = lambda x: int(x.split(" |")[0]),reverse=True)

                for i in range(0,len(listeClans)):

                    string = string + listeClans[i]

                string = string + "```"
                await ctx.send(string)

            else:

                await ctx.send("Nous sommes en jour d'entraînement")
                return

            if "Les Initiés" in listeClans[0]:
                await ctx.send("Nous sommes 1er, merci à vous "+PRINCESS_GLASSES)

            if "Les Initiés" in listeClans[1]:
                await ctx.send("Nous sommes 2e "+KING_CRY)

            if "Les Initiés" in listeClans[2]:
                await ctx.send("Nous sommes 3e "+GOBLIN_STUCKED)

            if "Les Initiés" in listeClans[3]:
                await ctx.send("Nous sommes 4e "+PRINCESS_ANGRY)

            if "Les Initiés" in listeClans[4]:
                await ctx.send("Nous sommes derniers, c koi sa :rage:")

        else:

            channel = self.bot.get_channel(DEBUG_CHAN)
            await channel.send("[!T bateau] Erreur requête")
            return

async def setup(bot):
    await bot.add_cog(Bateau(bot))
