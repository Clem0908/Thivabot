from datetime import datetime
import discord
import requests
import json
from discord.ext import commands
from constants import *
import tokens

class Course(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def course(self,ctx):

        APICRTOKEN = tokens.getApiCrToken()
       
        id_c = "LPRYYG"
        PARAMS = {'Authorization': 'Bearer '+APICRTOKEN}
        r = requests.get(url = APICRURL+"/clans/%23"+id_c+"/currentriverrace", auth=None, params = PARAMS)
    
        if r.status_code == 200:
            
            await ctx.send("Classement des clans en course, jour actuel :")

            data = r.json()
            listeClans = []
            string = "```"

            if str(data['periodType']) == "colosseum":
                 await ctx.send("Nous sommes en jour de colisée, il n'y a pas de course de bateaux")
                 return

            if str(data['periodType']) == "warDay":

                if int(str(data.get("clan", {}).get("fame", -1))) >= 10000:
                    await ctx.send("Notre bateau est arrivé à destination "+PRINCESS_GLASSES)

                if datetime.today().weekday() == 3 and int(str(data.get("clan", {}).get("fame", -1))) == 0:
                    await ctx.send("Nous sommes le jour de guerre n°1, donc 0 points pour l'instant")

                for i in range(0,len(data['clans'])):

                    obj_i = data['clans'][i]
                    
                    listeClans.append(str(data['clans'][i]['fame'])+" | "+str(data['clans'][i]['name'])+"\n")

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
            await channel.send("[!T course] Erreur requête")
            return

async def setup(bot):
    await bot.add_cog(Course(bot))
