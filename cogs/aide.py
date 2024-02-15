import discord
from discord.ext import commands

class Aide(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def aide(self,ctx):
        with open("./aide.txt", "r") as aide:
            await ctx.send(aide.read())

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def aide_admin(self,ctx):
        with open("./aide_admin.txt", "r") as aide_admin:
            await ctx.send(aide_admin.read())

async def setup(bot):
    await bot.add_cog(Aide(bot))
