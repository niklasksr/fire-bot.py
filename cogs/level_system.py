import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import aiosqlite
import random
from colorama import Fore


class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(Fore.GREEN + '| level_system.py loaded')
        self.DB = "fire_bot_db.db"
    level = discord.SlashCommandGroup("level", "LevelSystem related commands")

    
            
        
    @staticmethod
    def get_level(xp):
        lvl = 1
        amount = 100
            
        while True:
            xp -= amount
            if xp < 0:
                return lvl
            lvl += 1
            amount += 100
        
    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                '''
                CREATE TABLE IF NOT EXISTS level (
                user_id INTEGER PRIMARY KEY,
                msg_count INTEGER DEFAULT 0,
                xp INTIGER DEFAULT 0
                )
                '''
                )
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                '''
                CREATE TABLE IF NOT EXISTS levelsystemsettings (
                guild_id INTEGER PRIMARY KEY,
                levelsystem_status TEXT DEFAULT aktiviert
                )                    
                '''
                )
            
    async def check_guild(self, guild_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "INSERT OR IGNORE INTO levelsystemsettings (guild_id) VALUES (?)", (guild_id,)
                )
            
            await db.commit()
    async def check_user(self, user_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "INSERT OR IGNORE INTO level (user_id) VALUES (?)", (user_id,)
                )
            await db.commit()
    
    async def get_xp(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
                async with db.execute("SELECT msg_count, xp FROM level WHERE user_id = ?", (user_id,)) as cursor:
                    result = await cursor.fetchone()
        
        return result[0]
    
    async def get_levelsystem_status(self, guild_id):
        await self.check_guild(guild_id)
        async with aiosqlite.connect(self.DB) as db:
                async with db.execute("SELECT levelsystem_status FROM levelsystemsettings WHERE guild_id = ?", (guild_id,)) as cursor:
                    result = await cursor.fetchone()
        
        return result[0]
        
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.guild:
            return
        lvlsys_stat = await self.get_levelsystem_status(message.guild.id)
        if lvlsys_stat == "deaktiviert":
            return
        
        xp = random.randint(10, 20)
        
        await self.check_user(message.author.id)
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "UPDATE level SET msg_count = msg_count + 1, xp = xp + ? WHERE user_id = ?", (xp, message.author.id,)
                )
            await db.commit()
            
        new_xp = await self.get_xp(message.author.id)
        
        old_level = self.get_level(new_xp - xp)
        new_level = self.get_level(new_xp)
            
        if old_level == new_level:
            return
        
    @level.command(description="Zeigt dein Level an")
    async def rank(self, ctx):
        lvlsys_stat = await self.get_levelsystem_status(ctx.guild.id)
        if lvlsys_stat == "deaktiviert":
            embed=discord.Embed(title="Das Levelsystem ist auf diesem Server deaktiviert", color=discord.Color.brand_red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        xp = await self.get_xp(ctx.author.id)
        lvl = self.get_level(xp)

        embed = discord.Embed(
            title="Dein Level",
            description=f"**{ctx.author.mention}** du hast **{xp}** XP und du bist Level **{lvl}**.",
            color=discord.Color.orange()
        )
                
        await ctx.respond(embed=embed, ephemeral=True)
                
    @level.command(description="Zeige das Level Leaderboard an")
    async def leaderboard(self, ctx):
        lvlsys_stat = await self.get_levelsystem_status(ctx.guild.id)
        if lvlsys_stat == "deaktiviert":
            embed=discord.Embed(title="Das Levelsystem ist auf diesem Server deaktiviert", color=discord.Color.brand_red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        desc = ""
        counter = 1
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute(
                "SELECT user_id, xp FROM level WHERE msg_count > 0 ORDER BY xp DESC LIMIT 10"
                ) as cursor:
                async for user_id, xp in cursor:
                    desc += f"{counter}. <@{user_id}> - {xp} XP\n"
                    counter += 1
        
        embed = discord.Embed(
            title="Rangliste",
            description=desc,
            color=discord.Color.yellow()
            )
        embed.set_thumbnail(url = self.bot.user.avatar.url)
        await ctx.respond(embed=embed)

    @level.command()
    @discord.default_permissions(administrator=True)
    async def change_xp(self, ctx,
     member: Option(discord.Member, "Wähle einen Member"),
     xp: Option(int, "Die Xp die du verändern möchtest")):
        lvlsys_stat = await self.get_levelsystem_status(ctx.guild.id)
        if lvlsys_stat == "deaktiviert":
            embed=discord.Embed(title="Das Levelsystem ist auf diesem Server deaktiviert", color=discord.Color.brand_red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        async with aiosqlite.connect(self.DB) as db:
                await db.execute(
                    "UPDATE level SET xp = xp + ? WHERE user_id = ?", (xp, member.id,)
                    )
                await db.commit()
    @slash_command()
    @discord.guild_only()
    async def message(self, ctx):
        lvlsys_stat = await self.get_levelsystem_status(ctx.guild.id)
        if lvlsys_stat == "deaktiviert":
            embed=discord.Embed(title="Das Levelsystem ist auf diesem Server deaktiviert", color=discord.Color.brand_red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
        msg_count = await self.get_xp(ctx.author.id)
        embed = discord.Embed(title=f"Du hast {msg_count} Nachrichten gesendet")
        await ctx.respond(embed=embed)

    @level.command(description="Aktiviere oder Deaktiviere das Levelsystem")
    @discord.default_permissions(administrator=True)
    @discord.guild_only()
    async def levelsystem(self, ctx, choice: Option(choices=["Aktivieren", "Deaktivieren"])):
        if choice == "Aktivieren":
            await self.check_guild(ctx.guild.id)
            choices = "aktiviert"
            embed=discord.Embed(title="Das Levelsystem wurde auf diesem Server aktiviert", color=discord.Color.brand_green())
            await ctx.respond(embed=embed)
            async with aiosqlite.connect(self.DB) as db:
                await db.execute(
                    "UPDATE levelsystemsettings SET levelsystem_status = ? WHERE guild_id = ?", (choices, ctx.guild.id,)
                    )
                await db.commit()
        elif choice == "Deaktivieren":
            await self.check_guild(ctx.guild.id)
            choices = "deaktiviert"
            embed=discord.Embed(title="Das Levelsystem wurde auf diesem Server deaktiviert", color=discord.Color.brand_red())
            await ctx.respond(embed=embed)
            async with aiosqlite.connect(self.DB) as db:
                await db.execute(
                    "UPDATE levelsystemsettings SET levelsystem_status = ? WHERE guild_id = ?", (choices, ctx.guild.id,)
                    )
                await db.commit()
        else:
            return
        
     
def setup(bot):
    bot.add_cog(LevelSystem(bot))
