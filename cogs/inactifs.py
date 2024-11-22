import discord
from discord.ext import commands
import requests
from constants import *
import tokens

class Inactifs(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def inactifs(self,ctx):

        APICRTOKEN = tokens.getApiCrToken()
        id_c = "LPRYYG"
        PARAMS = {'Authorization': 'Bearer '+APICRTOKEN}
        r = requests.get(url = APICRURL+"/clans/%23"+id_c+"/currentriverrace", auth=None, params = PARAMS)
        r1 = requests.get(url = APICRURL+"/clans/%23"+id_c+"/members", auth=None, params = PARAMS)

        if r.status_code == 200 and r1.status_code == 200:

            await ctx.send("Je liste les inactifs :")
            data = r.json()
            data1 = r1.json()

            #Bigs : 0/4 et 1/4; Ptits : 2/4 et 3/4
            big_ina = list()
            ptit_ina = list()

            string_big_ina = "```"
            string_ptit_ina = "```"
            for i in range(0,len(data1['items'])):

                for j in range(0,len(data['clan']['participants'])):

                    name = data['clan']['participants'][j]['name']
                    decks = data['clan']['participants'][j]['decksUsedToday']
                
                    if data['clan']['participants'][j]['tag'] == data1['items'][i]['tag']:

                        #Bigs
                        if decks < 2:
                            big_ina.append(str(name)+" "+str(decks)+"/4")
                    
                        #Ptits
                        if decks > 1 and decks < 4:
                            ptit_ina.append(str(name)+" "+str(decks)+"/4")

            big_ina_sorted = sorted(big_ina, key=lambda s: s.upper())
            ptit_ina_sorted = sorted(ptit_ina, key=lambda s: s.upper())

            #Conversion en string
            for i in range(0,len(big_ina)):
                string_big_ina = string_big_ina + str(big_ina_sorted[i])+"\n"
            string_big_ina = string_big_ina + "```"
            
            await ctx.send("Bigs inactifs (0 ou 1 deck/4 utilisés) :\n"+string_big_ina)
            
            #Conversion en string
            for i in range(0,len(ptit_ina)):
                string_ptit_ina = string_ptit_ina + str(ptit_ina_sorted[i])+"\n"
            string_ptit_ina = string_ptit_ina + "```"
            await ctx.send("Ptits inactifs (2 ou 3 decks/4 utilisés) :\n"+string_ptit_ina)
            await ctx.send("J'ai fini de lister")

        else:

            channel = self.bot.get_channel(DEBUG_CHAN)
            await channel.send("[!T inactifs] Erreur requête/API")

            return

async def setup(bot):
    await bot.add_cog(Inactifs(bot))
