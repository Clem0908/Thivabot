import discord
from discord.ext import commands
import pickledb

class Memorise(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def memorise(self,ctx,id_j: str):

        id_j = id_j.lstrip("#")
        db = pickledb.load("./database/id_joueur.db","False")

        if db.exists(str(ctx.author)) == True:

            await ctx.send("Attention, tu avais déjà un ID d'enregistré et je vais le remplacer")
            await ctx.send("J'enregistre l'ID suivant : "+id_j)
            db.set(str(ctx.author),str(id_j))
            await ctx.send("ID enregistré")

        else:

            await ctx.send("J'enregistre l'ID suivant : "+id_j)
            db.set(str(ctx.author),str(id_j))
            await ctx.send("ID enregistré")

async def setup(bot):
    await bot.add_cog(Memorise(bot))
