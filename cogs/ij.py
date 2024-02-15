import discord
from discord.ext import commands
import requests
import asyncio
from constants import *
import tokens

class Ij(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def ij(self,ctx,id_j: str):
        
        APICRTOKEN = tokens.getApiCrToken()

        id_j = id_j.lstrip('#')
        id_j = id_j.upper()

        if len(id_j) > 10:
            await ctx.send("L'ID du joueur entré est trop long :cry:")
            return

        PARAMS = {'Authorization': 'Bearer '+APICRTOKEN} 
        r = requests.get(url = APICRURL+"/players/%23"+id_j, auth=None, params = PARAMS) 

        if r.status_code == 200: 
            
            await ctx.send(ROYALEAPI + "player/"  + id_j)
            data = r.json()
            war_badge = ""
            i = 0
            nb_jours = 0
            
            for j in range(0,len(data['badges'])):
                if data['badges'][j]['name'] == "YearsPlayed":
                    nb_jours = data['badges'][j]['progress']

            annees = nb_jours // 365
            mois = (nb_jours - (annees * 365)) // 30
            jours = nb_jours - (annees * 365) - (mois * 30)

            while war_badge != "ClanWarWins" and i < len(data['badges']):
                
                war_badge = data['badges'][i]['name']
                i = i + 1

            if data['badges'][i-1]['name'] == "ClanWarWins":
                
                nb = data['badges'][i-1]['progress']
                name = data['name']
                await ctx.send(":star: Niveau : "+str(data['expLevel']))

                if nb_jours < 365:
                    await ctx.send(":video_game: Joueur depuis moins d'1 an")
                else:
                    await ctx.send(":video_game: Joueur depuis : "+str(annees)+" an(s), "+str(mois)+" mois et "+str(jours)+" jour(s)")
                
                new_msg = await ctx.send("\n<:gdc:966422842621194320> Nombre de victoires en guerre de "+str(name)+ " : **"+str(nb)+"**") 
                await asyncio.sleep(2)
                await new_msg.add_reaction("🟩")
                await new_msg.add_reaction("🟥")
            
            else:

                await ctx.send(":star: Niveau : "+str(data['expLevel']))

                if nb_jours < 365:
                    await ctx.send(":video_game: Joueur depuis moins d'1 an") 
                else:
                    await ctx.send(":video_game: Joueur depuis : "+str(annees)+" an(s), "+str(mois)+" mois et "+str(jours)+" jour(s)")

                new_msg = await ctx.send("<:gdc:966422842621194320> Nombre de victoires en guerre : **0 ou < 10**")
                await asyncio.sleep(2)
                await new_msg.add_reaction("🟩")
                await new_msg.add_reaction("🟥")
                
                return
        else:

            channel = self.bot.get_channel(DEBUG_CHAN)
            await channel.send("[!T ij] Erreur requête/jeton API")
            
            return

async def setup(bot):
    await bot.add_cog(Ij(bot))
