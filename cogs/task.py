import discord
import asyncio
from discord.ext import commands
from colorama import Fore

class Task(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(Fore.GREEN + '| task.py loaded')


    @commands.Cog.listener()
    async def status_task(self):
        while True:
            await self.bot.change_presence(activity=discord.Game('mit /help'), status=discord.Status.online)
            await asyncio.sleep(60)
            await self.bot.change_presence(activity=discord.Game(f"mit {len(self.bot.users)} Usern"), status=discord.Status.online)
            await asyncio.sleep(60)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"auf {len(self.bot.guilds)} Server"), status=discord.Status.online)
            await asyncio.sleep(60)
            await self.bot.change_presence(activity=discord.Game("mit dem BannHammer!"), status=discord.Status.online)
            await asyncio.sleep(60)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.status_task()
        
     
def setup(bot):
    bot.add_cog(Task(bot))