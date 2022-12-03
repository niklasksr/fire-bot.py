import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import time
import aiosqlite
from colorama import Fore


import traceback

startTime = time.time()   

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = "fire_bot_db.db"
        print(Fore.GREEN + '| setup.py loaded')

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                '''
                CREATE TABLE IF NOT EXISTS setup(
                guild_id INTEGER PRIMARY KEY,
                welcome_id INTIGER DEFAULT 0,
                join_rolle_id INTIGER DEFAULT 0,
                log_id INTIGER DEFAULT 0,
                ticket_channel_id INTIGER DEFAULT 0,
                ticket_kategorie_id INTIGER DEFAULT 0
                )
                '''
                )
            
    async def check_guild(self, guild_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "INSERT OR IGNORE INTO setup (guild_id) VALUES (?)", (guild_id,)
                )
            await db.commit()

            
    @slash_command()
    @discord.default_permissions(administrator=True)
    @discord.guild_only()
    async def setup(self, ctx, welcome_channel: Option(discord.TextChannel, required=False, default=0), join_rolle: Option(discord.Role, required=False, default=0), log_channel: Option(discord.TextChannel, required=False, default=0), ticket_channel: Option(discord.TextChannel, required=False, default=0), ticket_kategorie: Option(discord.CategoryChannel, required=False, default=0)):
        embed=discord.Embed(title="Setup",description="Zeigt die eingestellten Sachen an")
        await self.check_guild(ctx.guild.id)
        try:
            embed.add_field(name="Wellcome_channel", value=welcome_channel, inline=False)
            async with aiosqlite.connect(self.DB) as db:
                await db.execute(
                    "UPDATE setup SET welcome_id = ? WHERE guild_id = ?", (welcome_channel.id, ctx.guild.id,)
                    )
                await db.commit()
        except Exception:
            traceback.print_exc()
        try:
            embed.add_field(name="Join_Rolle", value=join_rolle, inline=False)
            async with aiosqlite.connect(self.DB) as db:
                await db.execute(
                    "UPDATE setup SET log_id = ? WHERE guild_id = ?", (log_channel.id, ctx.guild.id,)
                    )
                await db.commit()
        except Exception:
            traceback.print_exc()
        try:
            embed.add_field(name="Log_channel", value=log_channel, inline=False)
            async with aiosqlite.connect(self.DB) as db:
                await db.execute(
                    "UPDATE setup SET join_rolle_id = ? WHERE guild_id = ?", (join_rolle.id, ctx.guild.id,)
                    )
                await db.commit()
        except Exception:
            traceback.print_exc()
        await ctx.respond(embed=embed)

     
def setup(bot):
    bot.add_cog(Setup(bot))