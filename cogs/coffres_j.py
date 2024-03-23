import discord
from discord.ext import commands
import asyncio
import requests
from constants import *
import tokens
import time

class Coffres_j(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def coffres_j(self,ctx,id_j: str):

        id_j = id_j.lstrip("#")  

        if len(id_j) > 9:
            await ctx.send("Ce tag de joueur est trop long")
            return

        APICRTOKEN = tokens.getApiCrToken()
        PARAMS = {'Authorization': 'Bearer '+APICRTOKEN} 
        r = requests.get(url = APICRURL+"/players/%23"+id_j+"/upcomingchests", auth=None, params = PARAMS)
        r1 = requests.get(url = APICRURL+"/players/%23"+id_j, auth=None, params = PARAMS)
        
        if r.status_code == 200 and r1.status_code == 200:

            data = r.json()
            data1 = r1.json()

            await ctx.send("Je recherche les prochains coffres de : **"+str(data1['name'])+"**...\n")
            i = 0
            string_answer = ""

            for i in range(i,len(data['items'])):

                obj_i = data['items'][i]

                if obj_i['name'] == "Silver Chest":
                    
                    string_answer += str(str(obj_i['index'])+" | 3h | Coffre en Argent\n")

                if obj_i['name'] == "Golden Chest":
                    
                    string_answer += str(str(obj_i['index'])+" | 8h | Coffre en Or\n")

                if obj_i['name'] == "Magical Chest":
                    
                    string_answer += str(str(obj_i['index'])+" | 12h | Coffre Magique\n")

                if obj_i['name'] == "Overflowing Gold Crate":
                    
                    string_answer += str(str(obj_i['index'])+" | 12h | Cage d'Or Pleine\n")

                if obj_i['name'] == "Plentiful Gold Crate":
                    
                    string_answer += str(str(obj_i['index'])+" | 8h | Cage d'Or Moyenne\n")
                
                if obj_i['name'] == "Gold Crate":

                    string_answer += str(str(obj_i['index'])+" | 3h | Cage d'Or\n")

                if obj_i['name'] == "Legendary Chest":

                    string_answer += str(str(obj_i['index'])+" | 1j | Coffre Légendaire\n")

                if obj_i['name'] == "Mega Lightning Chest":

                    string_answer += str(str(obj_i['index'])+" | 1j | Méga Coffre Foudre\n")
                    
                if obj_i['name'] == "Giant Chest":

                    string_answer += str(str(obj_i['index'])+" | 12h | Coffre Géant\n")

                if obj_i['name'] == "Royal Wild Chest":
                    
                    string_answer += str(str(obj_i['index'])+" | 1j | Coffre Joker Royal\n")

                if obj_i['name'] == "Epic Chest":

                    string_answer += str(str(obj_i['index'])+" | 12h | Coffre Épique\n")

                if obj_i['name'] == "Tower Troop Chest":

                    string_answer += str(str(obj_i['index'])+" | 0h | Coffre de Troupes de Tour\n")

            await ctx.send(string_answer)
            await ctx.send("J'ai terminé de lister les coffres de : **"+str(data1['name'])+"**")

        else:

            channel = self.bot.get_channel(DEBUG_CHAN)
            await channel.send("[!T coffres] Erreur requête/API")

            return

async def setup(bot):
    await bot.add_cog(Coffres_j(bot))
