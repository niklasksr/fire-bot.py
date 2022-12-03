import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from colorama import Fore
import json
import os
from discord import Message, Guild, TextChannel

if os.path.isfile("servers.json"):
    with open('servers.json', encoding='utf-8') as f:
        servers = json.load(f)
else:
    servers = {"servers": []}
    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)


class Global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(Fore.GREEN + '| global.py loaded')
        
    globalchat = discord.SlashCommandGroup("globalchat", "GlobalChat related commands")


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if not message.content.startswith('!'):
            if self.get_globalChat(message.guild.id, message.channel.id):
                if "www" in (message.content).lower():
                    await message.delete()
                    return
                await self.sendAll(message)
        
        

    async def sendAll(self, message: Message):
        embed = discord.Embed(title=f"**Nachricht von {message.author.name}**",description=f"{message.content}\n\n\n[Support](https://discord.gg/TdxrknnK6a) || [Bot Invite](https://discord.com/api/oauth2/authorize?client_id=1040743634531782828&permissions=1514248006102&scope=bot%20applications.commands)", color=discord.Color.orange())
        embed.set_thumbnail(url=message.author.display_avatar.url)
        embed.set_footer(text=f"Gesendet von Server: {message.guild.name}")
        await message.delete()
        for server in servers["servers"]:
            guild: Guild = self.bot.get_guild(int(server["guildid"]))
            if guild:
                channel: TextChannel = guild.get_channel(int(server["channelid"]))
                if channel:
                    await channel.send(embed=embed)
        

    def guild_exists(self, guildid):
        for server in servers['servers']:
            if int(server['guildid'] == int(guildid)):
                return True
        return False


    def get_globalChat(self, guild_id, channelid=None):
        globalChat = None
        for server in servers["servers"]:
            if int(server["guildid"]) == int(guild_id):
                if channelid:
                    if int(server["channelid"]) == int(channelid):
                        globalChat = server
                else:
                    globalChat = server
        return globalChat


    def get_globalChat_id(self, guild_id):
        globalChat = -1
        i = 0
        for server in servers["servers"]:
            if int(server["guildid"]) == int(guild_id):
                globalChat = i
            i += 1
        return globalChat
    
    

    @globalchat.command()
    @discord.guild_only()
    @discord.default_permissions(administrator=True)
    async def addglobal(self, ctx):
        if not self.guild_exists(ctx.guild.id):
            server = {
                    "guildid": ctx.guild.id,
                    "channelid": ctx.channel.id,
                    "invite": f'{(await ctx.channel.create_invite()).url}'
            }
            servers["servers"].append(server)
            with open('servers.json', 'w') as f:
                json.dump(servers, f, indent=4)
            await ctx.respond('Erstellt.')

    @globalchat.command()
    @discord.guild_only()
    @discord.default_permissions(administrator=True)
    async def removeglobal(self, ctx):
        if self.guild_exists(ctx.guild.id):
            globalid = self.get_globalChat_id(ctx.guild.id)
            if globalid != -1:
                servers["servers"].pop(globalid)
                with open('servers.json', 'w') as f:
                    json.dump(servers, f, indent=4)
                await ctx.respond('Entfernt.')

        
        
   
        
    
     
def setup(bot):
    bot.add_cog(Global(bot))