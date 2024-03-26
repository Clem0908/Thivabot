import discord
from discord.ext import commands
from constants import *

class Changer_fuseau(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def changer_fuseau(self,ctx,plus: int):

        f = open("FUSEAU.py","w")
        content = ""
        content = content + "FUSEAU=" + str(plus) + "\n"
        f.write(content)
        f.close()
        await ctx.send("```Fuseau horaire modifié : UTC+"+str(plus)+"\n"+"Redémarrage nécessaire pour application des changements...```")
        command = self.bot.get_command("bye")
        channel = self.bot.get_channel(DEBUG_CHAN)
        await command.__call__(channel)
       
async def setup(bot):
    await bot.add_cog(Changer_fuseau(bot))
