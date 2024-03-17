import discord
import requests
import json
from discord.ext import commands
import tokens
from constants import *

class Get_hgdc(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def get_hgdc(self,ctx):
        
        APICRTOKEN = tokens.getApiCrToken()
       
        id_c = "LPRYYG"
        PARAMS = {'Authorization': 'Bearer '+APICRTOKEN}
        r = requests.get(url = APICRURL+"/clans/%23"+id_c+"/riverracelog?limit=1", auth=None, params = PARAMS)
        
        if r.status_code == 200:

            data = r.json()
            str_date = str(data['items'][0]['createdDate'])

            if 'Z' in str_date:
                
                hgdc = ""
                hgdc += str_date[9:11]+":"+str_date[11:13]+":"+str_date[13:15]+" UTC"
                await ctx.send(hgdc)

            else:
                channel = self.bot.get_channel(DEBUG_CHAN)
                await channel.send("[!T get_hgdc] Le temps reçu dans la requête n'est pas en UTC")
                return

        else:

            channel = self.bot.get_channel(DEBUG_CHAN)
            await channel.send("[!T get_hgdc] Erreur requête")
            return

async def setup(bot):
    await bot.add_cog(Get_hgdc(bot))
