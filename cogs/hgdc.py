import discord
from discord.ext import commands
from constants import *

class Hgdc(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def hgdc(self,ctx,heure: int, minute: int):

        f = open("HH_MM.py","w")
        content = ""
        content = content + "HEURE=" + str(heure) + "\n"
        content = content + "MINUTE=" + str(minute) + "\n"
        f.write(content)
        f.close()
        await ctx.send("```Nouvelle heure de fin de GDC enregistrée.\nRedémarrage nécessaire pour application des changements...```")
        command = self.bot.get_command("bye")
        channel = self.bot.get_channel(DEBUG_CHAN)
        await command.__call__(channel)
        
async def setup(bot):
    await bot.add_cog(Hgdc(bot))
