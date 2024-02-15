import discord
from discord.ext import commands
import pickledb
import asyncio
import requests
from constants import *
import tokens

class Coffres(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def coffres(self,ctx):

        APICRTOKEN = tokens.getApiCrToken()
        db = pickledb.load("./database/id_joueur.db","False")
        id_j = db.get(str(ctx.author))
        
        if db.exists(str(ctx.author)) == False:

            await ctx.send("Tu n'as pas d'ID enregistré, je t'invite à le faire avec : ```!T memorise [ID]```")
            return

        PARAMS = {'Authorization': 'Bearer '+APICRTOKEN} 
        r = requests.get(url = APICRURL+"/players/%23"+id_j+"/upcomingchests", auth=None, params = PARAMS)
        r1 = requests.get(url = APICRURL+"/players/%23"+id_j, auth=None, params = PARAMS)
        
        if r.status_code == 200 and r1.status_code == 200:

            data = r.json()
            data1 = r1.json()

            await ctx.send("Je recherche les prochains coffres de : **"+str(data1['name'])+"**...\n")
            i = 0

            for i in range(i,len(data['items'])):

                obj_i = data['items'][i]

                if obj_i['name'] == "Silver Chest":
                    await ctx.send(str(obj_i['index'])+" | 3h")
                    await ctx.send(IMG+"chest-silver.png")
                if obj_i['name'] == "Golden Chest":
                    await ctx.send(str(obj_i['index'])+" | 8h")
                    await ctx.send(IMG+"chest-gold.png")
                if obj_i['name'] == "Magical Chest":
                    await ctx.send(str(obj_i['index'])+" | 12h")
                    await ctx.send(IMG+"chest-magical.png")
                if obj_i['name'] == "Overflowing Gold Crate":
                    await ctx.send(str(obj_i['index'])+" | 12h")
                    await ctx.send(IMG+"chest-overflowgoldcrate.png")
                if obj_i['name'] == "Plentiful Gold Crate":
                    await ctx.send(str(obj_i['index'])+" | 8h")
                    await ctx.send(IMG+"chest-plentifulgoldcrate.png")
                if obj_i['name'] == "Gold Crate":
                    await ctx.send(str(obj_i['index'])+" | 3h")
                    await ctx.send(IMG+"chest-goldcrate.png")
                if obj_i['name'] == "Legendary Chest":
                    await ctx.send(str(obj_i['index'])+" | 1j")
                    await ctx.send(IMG+"chest-legendary.png")
                if obj_i['name'] == "Mega Lightning Chest":
                    await ctx.send(str(obj_i['index'])+" | 1j")
                    await ctx.send(IMG+"chest-megalightning.png")
                if obj_i['name'] == "Giant Chest":
                    await ctx.send(str(obj_i['index'])+" | 12h")
                    await ctx.send(IMG+"chest-giant.png")
                if obj_i['name'] == "Royal Wild Chest":
                    await ctx.send(str(obj_i['index'])+" | 1j")
                    await ctx.send(IMG+"chest-royalwild.png")
                if obj_i['name'] == "Epic Chest":
                    await ctx.send(str(obj_i['index'])+" | 12h")
                    await ctx.send(IMG+"chest-epic.png")

            await ctx.send("J'ai terminé de lister les coffres de : **"+str(data1['name'])+"**")

        else:

            channel = self.bot.get_channel(DEBUG_CHAN)
            await channel.send("[!T coffres] Erreur requête/API")

            return

async def setup(bot):
    await bot.add_cog(Coffres(bot))
