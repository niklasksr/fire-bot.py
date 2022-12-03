import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from datetime import timedelta
from colorama import Fore

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = "level.db"
        print(Fore.GREEN + '| admin.py loaded')
    admin = discord.SlashCommandGroup("admin", "Admin related commands")
        
    @admin.command(description="Kicke einen Member")
    @discord.default_permissions(kick_members=True)
    @discord.guild_only()
    async def kick(self, ctx, member: Option(discord.Member, "Wähle einen Member"), reason: Option(str, default=None)):
        try:
            await member.kick(reason=reason)
        except discord.Forbidden:
            await ctx.respond("Ich haben keine Berechtigung, um diesen Member zu kicken")
            return
        await ctx.respond(f"{member.mention} wurde gekickt")


    @admin.command(name = 'timeout', description = "Timeoute einen Member")
    @discord.default_permissions(kick_members=True)
    @discord.guild_only()
    async def timeout(self, ctx, 
    member: Option(discord.Member, "Wähle einen Memeber"), 
    reason: Option(str, required = False), 
    days: Option(int, max_value = 27, default = 0, required = False), 
    hours: Option(int, default = 0, required = False), 
    minutes: Option(int, default = 0, required = False), 
    seconds: Option(int, default = 0, required = False)):
        if member.id == ctx.author.id:
            await ctx.respond("Du kannst dich nicht selbst timeouten!")
            return
        if member.guild_permissions.moderate_members:
            await ctx.respond("Du kannst das nicht tun, die Person ist ein Moderrator")
            return
        duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
        if duration >= timedelta(days = 28): 
            await ctx.respond("Ich kann nicht jemanden mehr als 28 Tage timeouten", ephemeral = True) 
            return
        if reason == None:
            await member.timeout_for(duration)
            embed = discord.Embed(
                title="Timeout",
                description=f"{member.mention} wurde für {days} Tage, {hours} Stunden, {minutes} Minuten, und {seconds} Sekunden getimeoutet von {ctx.author.mention}.",
                color=0xDF0101
            )
            await ctx.respond(embed=embed)
        else:
            await member.timeout_for(duration, reason = reason)
            embed = discord.Embed(
                title="Timeout",
                description=f"{member.mention} wurde für {days} Tage, {hours} Stunden, {minutes} Minuten, und {seconds} Sekunden getimeoutet von {ctx.author.mention} für '{reason}'.",
                color=0xDF0101
            )
            
            await ctx.respond(embed=embed)


    @admin.command(description="Banne einen Member")
    @discord.default_permissions(ban_members=True)
    @discord.guild_only()
    async def ban(self, ctx, member: Option(discord.Member, "Wähle einen Member"), reason: Option(str, required=False)):
        try:
            await member.ban(reason=reason)
        except discord.Forbidden:
            await ctx.respond("Ich haben keine Berechtigung, um diesen Member zu bannen")
            return
        await ctx.respond(f"{member.mention} wurde gebannt")
    
    '''@slash_command(description="Aktiviere oder Deaktiviere das Levelsystem")
    @discord.default_permissions(administrator=True)
    @discord.guild_only()
    async def levelsystem(self, ctx, choice: Option(choices=["Aktivieren", "Deaktivieren"])):
        if choice == "Aktivieren":
            async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "UPDATE users SET msg_count = msg_count + 1, xp = xp + ? WHERE user_id = ?", (xp, message.author.id,)
                )
            await db.commit()
        elif choice == "Deaktivieren":
        else:
            return'''

        
     
def setup(bot):
    bot.add_cog(Admin(bot))