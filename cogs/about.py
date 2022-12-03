import discord
from discord.ext import commands
from discord.commands import slash_command
from datetime import datetime, timedelta
import time
import os
import json
from colorama import Fore



startTime = time.time()   

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(Fore.GREEN + '| about.py loaded')
        
    @slash_command(description="Zeige Infos über den Bot")
    async def about(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - startTime))
        uptime = str(timedelta(seconds=difference))


        embed = discord.Embed(title="**__About__**", color=discord.Color.orange())

        embed.add_field(name='Allgemeine Informationen',
                    value=f"> **Developer: niklas.ksr#6397** \n"
                        f"> **Coding Language:** Python; 3.9.13\n"
                        "> **Libary:** [py-cord](https://docs.pycord.dev/en/stable/)\n"
                        f"> **Uptime:** {uptime}")

        embed.add_field(name="Statistiken",
                    value=f"> **Anzahl der Servers:** {len(self.bot.guilds)}\n"
                        f"> **Anzahl der Users:** {len(self.bot.users)}\n"
                        f"> **Latency:** {round(self.bot.latency * 1000)}\n",
                    inline=False)
        await ctx.respond(embed = embed)
            

     
def setup(bot):
    bot.add_cog(About(bot))