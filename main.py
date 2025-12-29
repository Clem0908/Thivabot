import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
import discord
from discord.ext import tasks
from discord.ext import commands
from discord.utils import get
import json
import logging
from logging.handlers import RotatingFileHandler
import os
import pickledb
import requests

from constants import *
from HH_MM import *
import tokens

scheduler = AsyncIOScheduler()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!T ",intents=intents)

# Logs
handler = RotatingFileHandler(
    'logs/main.log',
    maxBytes=5000,
    backupCount=1
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
# Logs

# Fonction pour traduire les noms des rôles en Français 
async def trad_role(string):
    trad = ""
    match string:
        case "member":
            trad += "Membre"
        case "elder":
            trad += "Aîné"    
        case "coLeader":
            trad += "Chef adjoint"
        case "leader":
            trad += "Chef"
    return trad

@bot.event
async def on_ready():

    logger.info("Le bot est connecté sous : {0.user}".format(bot))

    if DEBUG is False:
        print("c la prod")
        """        
        channel = bot.get_channel(DEBUG_CHAN)
        await channel.send("Lancée :green_circle:")

        log_du_clan.start()
        scheduler.start()
        """

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Pour en savoir plus, tape : `!T aide`")

    if isinstance(error, commands.errors.BadArgument):
        await ctx.send("Mauvais arguments : pour en savoir plus, tape : `!T aide`")

async def main():

    BOTTOKEN = tokens.getBotToken()

    async with bot:
        await bot.load_extension("cogs.aide")
        await bot.load_extension("cogs.course")
        await bot.load_extension("cogs.effacer")
        await bot.load_extension("cogs.envoyer_amour")
        await bot.load_extension("cogs.ij")
        await bot.load_extension("cogs.info_clan")
        await bot.load_extension("cogs.inactifs")
        await bot.load_extension("cogs.lj")
        await bot.load_extension("cogs.connexion")
        await bot.load_extension("cogs.memorise")
        await bot.load_extension("cogs.supprime")
        await bot.load_extension("cogs.cherche_id")
        await bot.load_extension("cogs.igdc")
        await bot.load_extension("cogs.memorise_a")
        await bot.load_extension("cogs.class_v")
        await bot.load_extension("cogs.bateau")
        await bot.load_extension("cogs.topfr")
        await bot.load_extension("cogs.emote")
        await bot.load_extension("cogs.hgdc")
        await bot.load_extension("cogs.class_jour_gdc")
        await bot.load_extension("cogs.get_hgdc")
        await bot.load_extension("cogs.changer_fuseau")

        await bot.start(BOTTOKEN)

@bot.command()
@commands.has_permissions(administrator=True)
async def bye(ctx):
    
    logger.info("!T bye")
    channel = bot.get_channel(DEBUG_CHAN)
    await channel.send("Arrêtée :red_circle:")
    await bot.close()

@bot.command()
@commands.has_permissions(administrator=True)
async def cloner(ctx, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel
    await channel.clone(name=channel.name+"-clone")

@bot.command()
@commands.has_permissions(administrator=True)
async def cloner_et_supprimer(ctx, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel
    await channel.clone(name=channel.name+"-clone")
    await channel.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def supprimer(ctx, channel: discord.TextChannel = None):
    
    if channel is None:
        channel = ctx.channel

    await ctx.send("Tu es sûr(e) de vouloir supprimer ce salon ? (oui/non)")

    def verif(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        choix = await bot.wait_for('message', check=verif, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("Opération annulée")
        return

    if choix.content.lower() not in "oui":
        await ctx.send("Opération annulée")
        return
    
    if choix.content.lower() in "oui":
        await channel.delete()

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def changer_pseudo(ctx, membre: discord.Member, pseudo):
    await membre.edit(nick=pseudo)

async def gdc(channel_id, message):
    
    logger.info("gdc")
    today = datetime.date.today()
    dt = datetime.datetime.today()

    channel = bot.get_channel(channel_id)
    command = bot.get_command("bateau")

    if today.weekday() != 3:
        await command(channel)
        await channel.send(message)

    elif today.weekday() == 3 and dt.hour > 12:
        await command(channel)
        await channel.send(message)
    
    ina_chan = bot.get_channel(INA_CHAN)
    command = bot.get_command("inactifs")

    # Jeudi exclu, juste avant le début de la guerre
    if dt.hour == HEURE and dt.minute == MINUTE and today.weekday() != 3:
        await command(ina_chan)

async def autoclass_jour_gdc(channel_id):
    
    logger.info("autoclass_jour_gdc")
    channel = bot.get_channel(channel_id)

    command = bot.get_command("class_jour_gdc")
    await command(channel)

# class_jour_gdc au dernier jour
scheduler.add_job(autoclass_jour_gdc,'cron',day_of_week='mon',hour=HEURE,minute=MINUTE,args=[TOP20_CHAN],misfire_grace_time=180)

scheduler.add_job(gdc,'cron',day_of_week='mon',hour=8,minute=0,args=[GDC_CHAN,GDC_EMOJI+GDC_MSG+"4 va se terminer\n"+GDC_MENTION],misfire_grace_time=180)
scheduler.add_job(gdc,'cron',day_of_week='mon',hour=HEURE,minute=MINUTE,args=[GDC_CHAN,GDC_EMOJI+GDC_MSG+"4 va se terminer\n"+GDC_MENTION],misfire_grace_time=180)

scheduler.add_job(gdc,'cron',day_of_week='thu',hour=HEURE,minute=MINUTE,args=[GDC_CHAN,GDC_EMOJI+GDC_MSG+"1 vient de débuter\n"+GDC_MENTION],misfire_grace_time=180)
scheduler.add_job(gdc,'cron',day_of_week='thu',hour=20,minute=0,args=[GDC_CHAN,GDC_EMOJI+GDC_MSG+"1 est en cours\n"+GDC_MENTION],misfire_grace_time=180)
scheduler.add_job(gdc,'cron',day_of_week='fri',hour=8,minute=0,args=[GDC_CHAN,GDC_EMOJI+GDC_MSG+"1 va se terminer\n"+GDC_MENTION],misfire_grace_time=180)
scheduler.add_job(gdc,'cron',day_of_week='fri',hour=HEURE,minute=MINUTE,args=[GDC_CHAN,GDC_EMOJI+GDC_MSG+"2 vient de débuter\n"+GDC_MENTION],misfire_grace_time=180)
scheduler.add_job(gdc,'cron',day_of_week='fri',hour=20,minute=0,args=[GDC_CHAN,GDC_EMOJI+GDC_MSG+"2 est en cours\n"+GDC_MENTION],misfire_grace_time=180)
scheduler.add_job(gdc,'cron',day_of_week='sat',hour=8,minute=0,args=[GDC_CHAN,GDC_EMOJI+GDC_MSG+"2 va se terminer\n"+GDC_MENTION],misfire_grace_time=180)
scheduler.add_job(gdc,'cron',day_of_week='sat',hour=HEURE,minute=MINUTE,args=[GDC_CHAN,GDC_EMOJI+GDC_MSG+"3 vient de débuter\n"+GDC_MENTION],misfire_grace_time=180)
scheduler.add_job(gdc,'cron',day_of_week='sat',hour=20,minute=0,args=[GDC_CHAN,GDC_EMOJI+GDC_MSG+"3 est en cours\n"+GDC_MENTION],misfire_grace_time=180)
scheduler.add_job(gdc,'cron',day_of_week='sun',hour=8,minute=0,args=[GDC_CHAN,GDC_EMOJI+GDC_MSG+"3 va se terminer\n"+GDC_MENTION],misfire_grace_time=180)
scheduler.add_job(gdc,'cron',day_of_week='sun',hour=HEURE,minute=MINUTE,args=[GDC_CHAN, GDC_EMOJI+GDC_MSG+"4 vient de débuter\n"+GDC_MENTION],misfire_grace_time=180)
scheduler.add_job(gdc,'cron',day_of_week='sun',hour=20,minute=0,args=[GDC_CHAN,GDC_EMOJI+GDC_MSG+"4 est en cours\n"+GDC_MENTION],misfire_grace_time=180)

async def autotopfr(channel_id):
    
    logger.info("autotopfr")
    channel = bot.get_channel(channel_id)
    command = bot.get_command("topfr")
    await command(channel)

scheduler.add_job(autotopfr,'cron',day_of_week='mon',hour=12,minute=0,args=[LOG_CHAN],misfire_grace_time=180)

@tasks.loop(minutes=1)
async def log_du_clan():

    APICRTOKEN = tokens.getApiCrToken()

    id_c = "LPRYYG"
    PARAMS = {'Authorization': 'Bearer '+APICRTOKEN}
    r = requests.get(url = APICRURL+"/clans/%23"+id_c, auth=None, params = PARAMS)
    channel = bot.get_channel(LOG_CHAN)

    if r.status_code == 200 and os.path.exists("./database/clan.json") is False:
        data = r.json()
        with open("./database/clan.json","w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=4)

    if r.status_code == 200 and os.path.exists("./database/clan.json") is True:

        data = r.json()

        f = open("./database/clan.json","r",encoding="utf-8")
        database = json.load(f)

        
        if database['members'] > data['members']:
            
            cpt = database['members'] - data['members']
            await channel.send(str(cpt)+" membre(s) parti(s)")
            listePartis = []
            listeDatabase = []
            listeData = []

            for i in range(0,len(database['memberList'])):
                obj_i = database['memberList'][i]
                listeDatabase.append(str(obj_i['name']) + " | "+str(obj_i['tag']))

            for i in range(0,len(data['memberList'])):
                obj_i = data['memberList'][i]
                listeData.append(str(obj_i['name']) + " | "+str(obj_i['tag']))

            for member in listeDatabase:
                if member not in listeData:
                    listePartis.append(member)

            for i in range(0,len(listePartis)):

                await channel.send(listePartis[i])

        if database['members'] < data['members']:

            cpt = data['members'] - database['members']
            await channel.send(str(cpt)+" membre(s) arrivé(s)")
            listeArrives = []
            listeDatabase = []
            listeData =[]

            for i in range(0,len(database['memberList'])):
                obj_i = database['memberList'][i]
                listeDatabase.append(str(obj_i['name']) + " | "+str(obj_i['tag']))

            for i in range(0,len(data['memberList'])):
                obj_i = data['memberList'][i]
                listeData.append(str(obj_i['name']) + " | "+str(obj_i['tag']))

            for member in listeData:
                if member not in listeDatabase:
                    
                    listeArrives.append(member)
                    n_string = ""
                    
                    for i in range(0,len(member)):
                        if member[i] != '|':
                           i = i + 1
                        else:
                            break

                    n_string = member[i+2:len(member)]
                    if n_string == "#UUPRGQL9R" or n_string == "#UR99YRUYY" or n_string == "#V2V8PPYVJ" or n_string == "#U22YR02C8" or n_string == "#CVG80L0GY" or n_string == "#2CYY0RPV":
                        
                        await channel.send("Renforts de GDC")

                    else:

                        nv_channel = bot.get_channel(NOUVEAUX_CHAN)
                        ij = bot.get_command("ij")
                        await ij.__call__(nv_channel,id_j=str(n_string))

            for i in range(0,len(listeArrives)):

                await channel.send(listeArrives[i])

        if database['type'] != data['type']:

            await channel.send("Nouveau statut du clan : "+str(data['type']))

        if database['description'] != data['description']:

            await channel.send("Nouvelle description du clan : "+str(data['description']))

        if database['clanWarTrophies'] != data['clanWarTrophies']:

            await channel.send("Trophées du clan : "+str(database['clanWarTrophies'])+" -> "+str(data['clanWarTrophies']))

        if database['requiredTrophies'] != data['requiredTrophies']:

            await channel.send("Trophées requis : "+str(database['requiredTrophies'])+" -> "+str(data['requiredTrophies']))

        nb_m1 = database['members']
        nb_m2 = data['members']

        if nb_m1 >= nb_m2:

            for i in range(0,len(database['memberList'])):

                obj_i = database['memberList'][i]

                for j in range(0,len(data['memberList'])):

                    obj_j = data['memberList'][j]

                    if (obj_i['tag'] == obj_j['tag']) and (obj_i['role'] != obj_j['role']):

                        a_role = ""
                        a_role = await trad_role(str(obj_i['role']))
                        n_role = ""
                        n_role = await trad_role(str(obj_j['role']))
                        await channel.send("Changement de rôle : "+str(obj_i['name'])+" | "+a_role+" -> "+n_role)

        else:

            for i in range(0,len(data['memberList'])):

                obj_i = data['memberList'][i]

                for j in range(0,len(database['memberList'])):

                    obj_j = database['memberList'][j]

                    if (obj_i['tag'] == obj_j['tag']) and (obj_i['role'] != obj_j['role']):

                        a_role = ""
                        a_role = await trad_role(str(obj_j['role']))
                        n_role = ""
                        n_role = await trad_role(str(obj_i['role']))
                        await channel.send("Changement de rôle : "+str(obj_j['name'])+" | "+a_role+" -> "+n_role)


        with open("./database/clan.json","w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=4)

    if r.status_code != 200:
        
        logger.warning("log_du_clan : "+str(r.status_code))
        channel = bot.get_channel(DEBUG_CHAN)
        await channel.send("log_du_clan : "+str(r.status_code)+", "+str(r.reason)+", "+str(r.message))
        return

if __name__ == "__main__":

    asyncio.run(main())
