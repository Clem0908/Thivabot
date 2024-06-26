import discord
from discord.ext import commands

class Get_csv(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def get_csv(self,ctx,month: str, year: str):
        await ctx.send(file=discord.File("./database/inactifs-"+month+year+".csv"))

async def setup(bot):
    await bot.add_cog(Get_csv(bot))
