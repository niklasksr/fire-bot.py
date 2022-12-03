import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import time
from cogs.econemy_system import EconemySystem
import aiosqlite
from colorama import Fore
from datetime import datetime


startTime = time.time()   

class Loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = "fire_bot_db.db"
        print(Fore.GREEN + '| logs.py loaded')

        
    async def check_guild(self, guild_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "INSERT OR IGNORE INTO setup (guild_id) VALUES (?)", (guild_id,)
                )
            await db.commit()
    
    async def check_user(self, user_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "INSERT OR IGNORE INTO econemy (user_id) VALUES (?)", (user_id,)
                )
            await db.commit()


    async def get_weclome_id(self, guild_id):
        await self.check_guild(guild_id)
        async with aiosqlite.connect(self.DB) as db:
                async with db.execute("SELECT welcome_id FROM setup WHERE guild_id = ?", (guild_id,)) as cursor:
                    result = await cursor.fetchone()
        
        return result[0]
    
    async def get_log_id(self, guild_id):
        await self.check_guild(guild_id)
        async with aiosqlite.connect(self.DB) as db:
                async with db.execute("SELECT log_id FROM setup WHERE guild_id = ?", (guild_id,)) as cursor:
                    result = await cursor.fetchone()
        
        return result[0]
    
    async def get_role_id(self, guild_id):
        await self.check_guild(guild_id)
        async with aiosqlite.connect(self.DB) as db:
                async with db.execute("SELECT join_rolle_id FROM setup WHERE guild_id = ?", (guild_id,)) as cursor:
                    result = await cursor.fetchone()
        
        return result[0]
    


    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.check_guild(member.guild.id)
        await self.check_user(member.id)
        try:
            async with aiosqlite.connect(self.DB) as db:
                await db.execute(
                    "UPDATE econemy SET flame = flame + 10 WHERE user_id = ?", (member.id,)
                    )
                await db.commit()
            welcome_id = await self.get_weclome_id(member.guild.id)
            channel = await self.bot.fetch_channel(welcome_id, )
            embed=discord.Embed(title=f"__**Willkommen {member}**__", description=f"**Schön das du da bist \n\nHier hast du 10 Flammen! Verbrenne dich nicht!**", color=discord.Color.brand_green())
            await channel.send(embed=embed)
        except:
           return
        try:
            role_id = await self.get_role_id(member.guild.id)
            join_role = member.guild.get_role(role_id)
            await member.add_roles(join_role)
        except:
            return
        try:
            log_id = await self.get_log_id(member.guild.id)
            channel = await self.bot.fetch_channel(log_id, )
            embed=discord.Embed(title=f"__**Member joint {member}**__", description=f"Der Member {member} ist dem Server beigetretten!", color=discord.Color.green(), timestamp = datetime.utcnow())
            await channel.send(embed=embed)
        except:
            return
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.check_guild(member.guild.id)
        try:
            log_id = await self.get_log_id(member.guild.id)
            channel = await self.bot.fetch_channel(log_id, )
            embed=discord.Embed(title=f"__**Member geleavt {member}**__", description=f"Der Member {member} hat den Server verlassen!", color=discord.Color.brand_red(), timestamp = datetime.utcnow())
            await channel.send(embed=embed)
        except:
            return
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await self.check_guild(message.guild.id)
        try:
            log_id = await self.get_log_id(message.guild.id)
            channel = await self.bot.fetch_channel(log_id,)
            embed=discord.Embed(title=f"Die Nachricht von {message.author} wurde gelöscht", description=f"**{message.content}**", color=discord.Color.brand_red())
            embed.set_thumbnail(url=message.author.display_avatar.url)
            
            await channel.send(embed=embed)
        except:
            return
            
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        await self.check_guild(guild.id)
        try:
            log_id = await self.get_log_id(guild.id)
            channel = await self.bot.fetch_channel(log_id,)
            embed=discord.Embed(title=f"Der {user} wurde gebannt", color=discord.Color.brand_red())
            embed.set_thumbnail(url=user.display_avatar.url)
            
            await channel.send(embed=embed)
        except:
            return
        
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        await self.check_guild(guild.id)
        try:
            log_id = await self.get_log_id(guild.id)
            channel = await self.bot.fetch_channel(log_id,)
            embed=discord.Embed(title=f"Der {user} wurde entbannt", color=discord.Color.brand_green())
            embed.set_thumbnail(url=user.display_avatar.url)
            
            await channel.send(embed=embed)
        except:
            return

        



        
     
def setup(bot):
    bot.add_cog(Loops(bot))