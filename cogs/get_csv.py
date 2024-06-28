import discord
from discord.ext import commands
import datetime

class Get_csv(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def get_csv(self,ctx,*args):

        if len(args) == 2:
            await ctx.send(file=discord.File("./database/inactifs-"+str(args[0])+str(args[1])+".csv"))
            return
        if len(args) == 0:
            dt = datetime.datetime.today()
            await ctx.send(file=discord.File("./database/inactifs-"+str(dt.month)+str(dt.year)+".csv"))
            return

        await ctx.send("Erreur de syntaxe : !T get_csv | !T get_csv 6 2024")
        return

async def setup(bot):
    await bot.add_cog(Get_csv(bot))
