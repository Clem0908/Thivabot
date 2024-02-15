import discord
import requests
import json
from discord.ext import commands
from constants import *
import tokens

class Topfr(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def topfr(self,ctx):

        APICRTOKEN = tokens.getApiCrToken()
        id_c = "LPRYYG"
        PARAMS = {'Authorization': 'Bearer '+APICRTOKEN}
        r = requests.get(url = APICRURL+"/locations/57000087/rankings/clanwars", auth=None, params = PARAMS)
    
        if r.status_code == 200:

            r1 = requests.get(url = APICRURL+"/clans/%23"+id_c, auth=None, params = PARAMS)

            if r1.status_code == 200:

                data = r.json()
                data1 = r1.json()
                await ctx.send("Trophées du clan : "+ str(data1['clanWarTrophies']))
                await ctx.send("Classement local FR du clan :")

                for i in range(0,len(data['items'])):

                    obj_i = data['items'][i]

                    if obj_i['tag'] == "#LPRYYG":

                        if obj_i['previousRank'] < obj_i['rank']:
                        
                            await ctx.send("Le clan a perdu en rang <:king_cry:966424394681425990>")
                    
                        else:

                            await ctx.send("Le clan a gagné en rang <:princess_glasses:1100023542977925151>")

                        await ctx.send("Ancien rang = **"+str(obj_i['previousRank'])+"** -> nouveau rang = **"+str(obj_i['rank'])+"**")
                        return

                else:
                    channel = self.bot.get_channel(DEBUG_CHAN)
                    await channel.send("[!T topfr] Erreur requête/API")

                    return

        else:

            channel = self.bot.get_channel(DEBUG_CHAN)
            await channel.send("[!T topfr] Erreur requête/API")

            return


async def setup(bot):
    await bot.add_cog(Topfr(bot))
