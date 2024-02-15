import discord
from discord.ext import commands
from constants import *

class Info_clan(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def info_clan(self,ctx,id_c: str):

        id_c = id_c.lstrip('#')
        await ctx.send(ROYALEAPI + "clan/"  + id_c)

async def setup(bot):
    await bot.add_cog(Info_clan(bot))
