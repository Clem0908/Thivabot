import discord
from discord.ext import commands
import requests
from constants import *
import tokens

class Igdc(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def igdc(self,ctx):

        APICRTOKEN = tokens.getApiCrToken()
        id_c = "LPRYYG"
        PARAMS = {'Authorization': 'Bearer '+APICRTOKEN}
        r = requests.get(url = APICRURL+"/clans/%23"+id_c+"/currentriverrace", auth=None, params = PARAMS)

        if r.status_code == 200:

            data = r.json()
            cpt = 0

            for i in range(0,len(data['clan']['participants'])):
    
                obj_i = data['clan']['participants'][i]

                if obj_i['decksUsedToday'] > 0:

                    cpt = cpt + 1

            await ctx.send(str(GDC_EMOJI)+" Nombre de participants à la guerre : "+str(cpt))

        else:
            channel = self.bot.get_channel(DEBUG_CHAN)
            await channel.send("[!T igdc] Erreur requête/API")

            return

async def setup(bot):
    await bot.add_cog(Igdc(bot))
