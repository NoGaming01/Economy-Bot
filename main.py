import nextcord as discord
from nextcord.ext import commands
import os
import dotenv

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

intents = discord.Intents.all()
prefix = "t"
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix, prefix.upper()), intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")

bot.run(token)
