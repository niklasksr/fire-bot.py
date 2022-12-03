import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import aiosqlite
import random
from colorama import Fore

class EconemySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(Fore.GREEN + '| econemy_system.py loaded')
        self.DB = "fire_bot_db.db"
    econemy = discord.SlashCommandGroup("econemy", "EconemySystem related commands")
        
        
    @staticmethod
    def convert_time(seconds: int) -> str:
        if seconds < 60:
            return f"{round(seconds)} Sekunden"
        minutes = seconds / 60
        if minutes < 60:
            return f"{round(minutes)} Minuten"
        hours = minutes / 60
        return f"{round(hours)} Stunden"


    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                '''
                CREATE TABLE IF NOT EXISTS econemy (
                user_id INTEGER PRIMARY KEY,
                flame INTIGER DEFAULT 0,
                dailystreak INTIGER DEFAULT 0
                )
                '''
                )
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                '''
                CREATE TABLE IF NOT EXISTS econemysystemsettings (
                guild_id INTEGER PRIMARY KEY,
                levelsystem_status TEXT DEFAULT aktiviert
                )                    
                '''
                )
        
    async def check_user(self, user_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,)
                )
            await db.commit()
    
    async def get_flame(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
                async with db.execute("SELECT flame FROM users WHERE user_id = ?", (user_id,)) as cursor:
                    result = await cursor.fetchone()
        
        return result[0]

    async def get_dailystrak(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
                async with db.execute("SELECT dailystreak FROM users WHERE user_id = ?", (user_id,)) as cursor:
                    result = await cursor.fetchone()
        
        return result[0]
    
    async def get_bonusflammen(self, user_id):
        ds = await self.get_dailystrak(user_id)
        if ds < 42 or ds == 42:
            rbo = random.randint(10, 20)
            bonusflammen = ds * 2 + rbo
            return bonusflammen
        else: 
            bonusflammen = 104
            return bonusflammen

        
        
    @econemy.command(description="Hole dir deine Täglichen Flammen")
    @discord.guild_only()
    @commands.cooldown(1, 24 * 60 * 60, commands.BucketType.member)
    async def daily(self, ctx):

        flame = random.randint(30, 50)
        
        await self.check_user(ctx.author.id)
        daistrak = await self.get_dailystrak(ctx.author.id)
        bonusflammen = await self.get_bonusflammen(ctx.author.id)
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "UPDATE econemy SET flame = flame + ? WHERE user_id = ?", (flame, ctx.author.id,)
                )
            await db.commit()
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "UPDATE econemy SET flame = flame + ? WHERE user_id = ?", (bonusflammen, ctx.author.id,)
                )
            await db.commit()
            
            
        

        ges_flame = await self.get_flame(ctx.author.id)
        
        embed=discord.Embed(
            title="Tägliche Flammen",
            description=f"Du hast dir {flame} Flammen abgeholt! Sehr Heiß \n\n Streak: {daistrak} - BomusFlammen: {bonusflammen} \n\n Du hast jetzt {ges_flame} Flammen!",
            color=0xd06c2c)
    
        await ctx.respond(embed=embed)   

    @econemy.command(description="Führe ein Event durch")
    @discord.guild_only()
    @commands.cooldown(1, 8 * 60 * 60, commands.BucketType.member)
    async def event(self, ctx):
        zufalleins = random.randint(1,3)
        if zufalleins == 3:
            badevent = random.randint(1,1)
            if badevent == 1:
                async with aiosqlite.connect(self.DB) as db:
                    await db.execute(
                        "UPDATE econemy SET flame = flame - 4 WHERE user_id = ?", (ctx.author.id,)
                        )
                    await db.commit()
                    flame = await self.get_flame(ctx.author.id)
                embed = discord.Embed(title="**Event**",
                    description=f"Du hast versucht ein Feuer zumachen! \n\n Leider sind alle Flammen erloschen! \n\n Aus Frust löschst du **4** Flammen. \n\n Du hast jetzt {flame} Flammen", color=0xd06c2c)
                await ctx.respond(embed=embed)

            else:
                return

        else:
            goodevent = random.randint(1,1)
            if goodevent == 1:
                async with aiosqlite.connect(self.DB) as db:
                    await db.execute(
                        "UPDATE econemy SET flame = flame + 10 WHERE user_id = ?", (ctx.author.id,)
                        )
                    await db.commit()
                    flame = await self.get_flame(ctx.author.id)
                embed = discord.Embed(title="**Event**",
                    description=f"Du bist krank. Der überaus nette fire-bot schenkt dir **10** Flammen, damit es dir bald wieder besser geht.\n\n Du hast jetzt {flame} Flammen", color=0xd06c2c)
                await ctx.respond(embed=embed)
                



    @econemy.command(description="Zeigt deine Flammen an")
    async def flammen(self, ctx):
        flame = await self.get_flame(ctx.author.id)
        

        embed = discord.Embed(
            title="Deine Flammen",
            description=f"**{ctx.author.mention}** du hast **{flame}** Flammen.",
            color=discord.Color.orange()
        )
                
        await ctx.respond(embed=embed, ephemeral=True)
                
    @econemy.command(description="Zeige das Leaderboard an")
    async def eco_leaderboard(self, ctx):
        desc = ""
        counter = 1
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute(
                "SELECT user_id, flame FROM econemy > 0 ORDER BY flame DESC LIMIT 10"
                ) as cursor:
                async for user_id, flame in cursor:
                    desc += f"{counter}. <@{user_id}> - {flame} Flammen\n"
                    counter += 1
        
        embed = discord.Embed(
            title="Rangliste",
            description=desc,
            color=discord.Color.yellow()
            )
        embed.set_thumbnail(url = self.bot.user.avatar.url)
        await ctx.respond(embed=embed)

    @econemy.command()
    @discord.default_permissions(administrator=True)
    async def change_flame(self, ctx,
     member: Option(discord.Member, "Wähle einen Member"),
     flame: Option(int, "Die Flammen die du verändern möchtest")):
        async with aiosqlite.connect(self.DB) as db:
                await db.execute(
                    "UPDATE econemy SET flame = flame + ? WHERE user_id = ?", (flame, member.id,)
                    )
                await db.commit()
                flamen = await self.get_flame(ctx.author.id)
        embed=discord.Embed(title="Give_Flame",description=f"Du hast {member.mention} {flame} Flammen gegeben.\n\n {member.mention} hat jetzt {flamen} Flammen.")
        await ctx.respond(embed=embed, ephemeral=True)

    
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = ctx.command.get_cooldown_retry_after(ctx)
            final_time = self.convert_time(seconds)

            await ctx.respond(f"Du musst noch {final_time} warten.", ephemeral=True)
        
     
def setup(bot):
    bot.add_cog(EconemySystem(bot))
