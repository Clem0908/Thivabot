import discord
from discord.ext import commands
import pickledb

class Supprime(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def supprime(self,ctx):

        db = pickledb.load("./database/id_joueur.db","False")

        if db.exists(str(ctx.author)) == True:
            
            await ctx.send("Je supprime l'ID enregistré précedemment")
            db.rem(str(ctx.author))

        else:

            await ctx.send("Tu n'as pas d'ID enregistré")

async def setup(bot):
    await bot.add_cog(Supprime(bot))
