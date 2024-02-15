import discord
from discord.ext import commands

class Effacer(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def effacer(self,ctx,numarg: int):

        if(numarg <= 0):
            
            await ctx.send("Je dois supprimer au minimum 1 message")
            return 

        if(numarg > 100):
            
            await ctx.send("Je ne peux pas supprimer plus de 100 messages")
            return
        
        await ctx.channel.purge(limit=numarg)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def effacer_contient(self,ctx,expression: str):

        messages = await ctx.channel.history(limit=100).flatten()
        list_messages = [] 
        
        for i in messages:
            
            if expression in i.content: 
                list_messages.append(i)

        await ctx.channel.delete_messages(list_messages)

async def setup(bot):
    await bot.add_cog(Effacer(bot))
