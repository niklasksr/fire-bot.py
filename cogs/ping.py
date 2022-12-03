import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from colorama import Fore

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(Fore.GREEN + '| ping.py loaded')
        
        
        
    @slash_command(description="Pingen")
    async def ping(self, ctx):
        transparent = discord.Color.from_rgb(47, 49, 54)
        embed = discord.Embed(
            color=transparent,
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(
            name="⚡ __**Pong**__",
            value=f"Latenz: {round(self.bot.latency * 1000)}ms",
            inline=False
        )
        embed.set_footer(text=f"{ctx.guild.name}", icon_url=self.bot.user.avatar.url)
        await ctx.respond(embed=embed, ephemeral=True)
        
    
     
def setup(bot):
    bot.add_cog(Ping(bot))