import discord
import asyncio
from discord.ext import commands
from discord.commands import slash_command, Option
from colorama import Fore
import aiosqlite

class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = "fire_bot_db.db"
        print(Fore.GREEN + '| premium.py loaded')
        

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS premium (
                        guild_id INTEGER PRIMARY KEY,
                        premium_status TEXT DEFAULT deaktiviert
                        )
                        '''
                        )
            
    async def check_guild(self, guild_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "INSERT OR IGNORE INTO premium (guild_id) VALUES (?)", (guild_id,)
                )
            await db.commit()


    @slash_command(description="Aktiviere oder Deaktiviere Premium")
    @discord.default_permissions(administrator=True)
    @discord.guild_only()
    async def premium(self, ctx, choice: Option(choices=["Aktivieren", "Deaktivieren"])):
        if choice == "Aktivieren":
            await self.check_guild(ctx.guild.id)
            choices = "aktiviert"
            async with aiosqlite.connect(self.DB) as db:
                await db.execute(
                    "UPDATE premium SET premium_status = ? WHERE guild_id = ?", (choices, ctx.guild.id,)
                    )
                await db.commit()
        elif choice == "Deaktivieren":
            await self.check_guild(ctx.guild.id)
            choices = "deaktiviert"
            async with aiosqlite.connect(self.DB) as db:
                await db.execute(
                    "UPDATE premium SET premium_status = ? WHERE guild_id = ?", (choices, ctx.guild.id,)
                    )
                await db.commit()
        else:
            return



     
def setup(bot):
    bot.add_cog(Premium(bot))