import requests
import datetime
import discord
from discord.ext import commands
from constants import *
import tokens

class Connexion(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def connexion(self,ctx):

        APICRTOKEN = tokens.getApiCrToken()
        id_c = "LPRYYG"
        PARAMS = {'Authorization': 'Bearer '+APICRTOKEN} 
        r = requests.get(url = APICRURL+"/clans/%23"+id_c, auth=None, params = PARAMS)
        
        if r.status_code == 200: 

            await ctx.send("Liste des connexions des Initiés :")
            data = r.json()
            string = ""
            tab_trie = []


            for i in range(0,len(data['memberList'])):
                temps = datetime.datetime.strptime(data['memberList'][i]['lastSeen'], "%Y%m%dT%H%M%S.000Z")
                temps = temps + datetime.timedelta(hours=2)
                nom = data['memberList'][i]['name']
                tab_trie.append(str(temps)+" | "+nom+"\n")

            tab_trie.sort(reverse=True)

            for i in range(0,len(tab_trie)):
                string = string+tab_trie[i]

            await ctx.send(string)

        else:
            channel = self.bot.get_channel(DEBUG_CHAN)
            await channel.send("[!T connexion] Erreur requête/API")

            return
    
    @commands.command()
    async def connexion_j(self,ctx,id_j: str):
        
        APICRTOKEN = tokens.getApiCrToken()
        id_j = id_j.lstrip('#')
        id_c = "LPRYYG"
        PARAMS = {'Authorization': 'Bearer '+APICRTOKEN} 
        r = requests.get(url = APICRURL+"/clans/%23"+id_c, auth=None, params = PARAMS)
        
        if r.status_code == 200: 

            data = r.json()
            await ctx.send("Dernière connexion de :\n")
            string = ""

            for i in range(0,len(data['memberList'])):

                if id_j == data['memberList'][i]['tag'].lstrip('#'):
                    temps = datetime.datetime.strptime(data['memberList'][i]['lastSeen'], "%Y%m%dT%H%M%S.000Z")
                    temps = temps + datetime.timedelta(hours=2)
                    nom = data['memberList'][i]['name']
                    string = string+str(temps)+" | "+nom+"\n"

            await ctx.send(string)

        else:
            channel = self.bot.get_channel(DEBUG_CHAN)
            await channel.send("[!T connexion] Erreur requête/API")

            return
    
async def setup(bot):
    await bot.add_cog(Connexion(bot))
