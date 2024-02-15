import discord
from discord.ext import commands
import pickledb

class Cherche_id(commands.Cog):

    def __init__(self,bot):
        self.bot = bot


    @commands.command()
    async def cherche_id(self,ctx,utilisateur: discord.User):

        db = pickledb.load("./database/id_joueur.db","False")
        
        if db.exists(str(utilisateur)) == True:

            await ctx.send("J'ai trouvé l'ID de : "+str(utilisateur))
            await ctx.send(db.get(str(utilisateur)))

        else:

            await ctx.send("Je ne connais pas l'ID de cet utilisateur")

async def setup(bot):
    await bot.add_cog(Cherche_id(bot))
