import discord
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


status = discord.Status.dnd


bot = discord.Bot(intents=intents,
                owner_id=[528487422254645283],
                status=status
                )

@bot.event
async def on_ready():
    print(f"{bot.user} ist online!")

if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
    
     