import discord
from discord.ext import commands

class Emote(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def emote(self,ctx, nom: str):
        
        if nom == "amour":

            await ctx.send(file=discord.File("./gifs/amour.gif"))

        elif nom == "cochonne":

            await ctx.send(file=discord.File("./gifs/cochonne.gif"))

        elif nom == "dab":

            await ctx.send(file=discord.File("./gifs/dab.gif"))

        elif nom == "force":

            await ctx.send(file=discord.File("./gifs/force.gif"))

        elif nom == "golem_casse":

            await ctx.send(file=discord.File("./gifs/golem_casse.gif"))

        elif nom == "ouaiiis":

            await ctx.send(file=discord.File("./gifs/ouaiiis.gif"))

        elif nom == "prince_pleure":

            await ctx.send(file=discord.File("./gifs/prince_pleure.gif"))

        elif nom == "princesse_yeah":

            await ctx.send(file=discord.File("./gifs/princesse_yeah.gif"))

        elif nom == "reine":

            await ctx.send(file=discord.File("./gifs/reine.gif"))

        else:

            await ctx.send("J'ai besoin qu'on me précise quelle emote envoyer <:king_cry:966424394681425990>")
            await ctx.send("```Emotes disponibles :\namour\ncochonne\ndab\nforce\ngolem_casse\nouaiiis\nprince_pleure\nprincesse_yeah\nreine```")

async def setup(bot):
    await bot.add_cog(Emote(bot))
