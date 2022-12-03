import discord
from discord.ext import commands
from discord.ext.pages import Paginator, Page
from discord.commands import slash_command, Option
from colorama import Fore

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(Fore.GREEN + '| help.py loaded')


    @slash_command(description="Zeige eine Liste aller Befehle")
    async def help(self, ctx):

        embed1 = discord.Embed(
                    title="**__ALLGEMEINE HILFE__**",
                    color=discord.Color.blue()
                )
        embed1.add_field(name="/ping", value="Zeigt dir den Ping vom Bot", inline=False)
        embed1.add_field(name="/about", value="Zeigt dir Infos über den Bot", inline=False)
        embed1.set_footer(text="Seite 1")

        embed2 = discord.Embed(
                title="**__LEVEL SYSTEM HILFE__**", 
                color=discord.Color.green())
        embed2.add_field(name="/level", value="Zeige dein Level an", inline=False)
        embed2.add_field(name="/lvl_leaderboard", value="Zeige das Level Leaderboard an", inline=False)
        embed2.add_field(name="/change_xp", value="Verändere die Xp eines Users (nur für Admins)", inline=False)
        embed2.set_footer(text="Seite 2")

        embed3 = discord.Embed(
                title="**__ECONEMY SYSTEM HILFE__**", 
                color=discord.Color.gold())
        embed3.add_field(name="/daily", value="Hole dir deine Tägliche Belohnung", inline=False)
        embed3.add_field(name="/event", value="Führe ein Event durch", inline=False)
        embed3.add_field(name="/flammen", value="Zeige deine Flammen an", inline=False)
        embed3.add_field(name="/eco_leaderboard", value="Zeige das Econemy Leaderboard an", inline=False)
        embed3.add_field(name="/change_flame", value="Verändere die Flammen eines Users (nur für Admins)")
        embed3.set_footer(text="Seite 3")

        embed4 = discord.Embed(
                title="**__Admin Hilfe__**", 
                color=0xDF0101)
        embed4.add_field(name="/kick", value="Kicke einen User", inline=False)
        embed4.add_field(name="/ban", value="Banne einen User", inline=False)
        embed4.add_field(name="/timeout", value="TimeOute einen User", inline=False)
        embed4.add_field(name="/setup", value="Stelle deinen Server ein")
        embed4.set_footer(text="Seite 4")
            
        pages = [
            Page(embeds=[embed1]),
            Page(embeds=[embed2]),
            Page(embeds=[embed3]),
            Page(embeds=[embed4])
        ]
        paginator = Paginator(pages=pages, author_check=True, disable_on_timeout=True)
        
        await paginator.respond(ctx.interaction, ephemeral=True)        

     
def setup(bot):
    bot.add_cog(Help(bot))