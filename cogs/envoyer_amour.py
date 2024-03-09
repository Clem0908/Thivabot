import discord
from discord.ext import commands

class EnvoyerAmour(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def envoyer_amour(self,ctx):

        await ctx.send(HEAL_SPIRIT_LOVE)
        await ctx.send("<@684095550496309252>")
        await ctx.send("Je t'aime :heart:")

async def setup(bot):
    await bot.add_cog(EnvoyerAmour(bot))
