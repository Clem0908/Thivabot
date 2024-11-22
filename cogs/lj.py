import discord
from discord.ext import commands
import requests
from constants import *
import tokens
import os
import json

class Lj(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def lj(self,ctx):

        # Fonction pour traduire les noms des rôles en Français 
        def trad_role(string):
            trad = ""
            match string:
                case "member":
                    trad += "Membre"
                case "elder":
                    trad += "Aîné"    
                case "coLeader":
                    trad += "Chef adjoint"
                case "leader":
                    trad += "Chef"
            return trad


        if os.path.exists("./database/clan.json") is True:
            
            await ctx.send("Liste des joueurs du clan :")
            f = open("./database/clan.json","r",encoding="utf-8")
            database = json.load(f)
            lj = []
            it = ""

            for i in range(0,len(database['memberList'])):
                it += str(database['memberList'][i]['name']) + " | " + str(database['memberList'][i]['tag']) + " | " + trad_role(str(database['memberList'][i]['role'])) + "\n"
                lj.append(it)
                it = ""

            lj_sorted = sorted(lj, key=lambda s: s.upper())
            message_str = "```"
            
            for i in range(0,len(lj_sorted)):
                message_str += lj_sorted[i]

            message_str += "```"
            await ctx.send(message_str)

        else:

            await ctx.send("Je ne possède pas la base de données des joueurs du clan "+KING_CRY)

            return

        return

async def setup(bot):
    await bot.add_cog(Lj(bot))
