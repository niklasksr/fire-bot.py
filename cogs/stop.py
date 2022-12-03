import os
import sys

import discord
from discord import slash_command
from discord.ext import commands
from colorama import Fore


class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(Fore.GREEN + '| stop.py loaded')

  
    @slash_command(description="Stoppe den Bot", guild_ids=[972272888654733393])
    async def stop(self, ctx):
            transparent = discord.Color.from_rgb(47, 49, 54)
            if ctx.author.id == 528487422254645283: #owner id
                embed = discord.Embed(title="**Restartet**", description=f"Der Bot wurde erfolgreich gestoppt",
                                    color=transparent)
                await ctx.respond(embed=embed)

                os.execv(sys.executable, ['python'] + sys.argv)


            else:
                embed = discord.Embed(title="Error", description="Du bist nicht der Owner, der diesen Command auszuführen kann.",
                                        color=0xff6600)
                await ctx.respond(embed=embed)
            
def setup(bot):
    bot.add_cog(Stop(bot))