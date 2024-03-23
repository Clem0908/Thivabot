import discord
from discord.ext import commands
import pickledb

class Memorise_a(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def memorise_a(self,ctx,user: discord.User,id_j: str):

        id_j = id_j.lstrip("#")
        if len(id_j) > 9:
            await ctx.send("Ce tag de joueur est trop long")
            return
        
        db = pickledb.load("./database/id_joueur.db","False")

        if db.exists(str(user)) == True:

            await ctx.send("Attention, tu avais déjà un ID d'enregistré et je vais le remplacer")
            await ctx.send("J'enregistre l'ID suivant : "+id_j)
            db.set(str(user),str(id_j))
            await ctx.send("ID enregistré")

        else:

            await ctx.send("J'enregistre l'ID suivant : "+id_j)
            db.set(str(user),str(id_j))
            await ctx.send("ID enregistré")

async def setup(bot):
    await bot.add_cog(Memorise_a(bot))
