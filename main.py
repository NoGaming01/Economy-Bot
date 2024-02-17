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

def load_cogs():
    for filename in os.listdir("./Cogs"):
        if filename.endswith(".py"):
            name = filename[:-3]
            try:
                bot.load_extension(f"Cogs.{name}")
                print(f"Loaded {name} cog.")
            except Exception as e:
                print(f"Failed to load {name} cog. {e}")

load_cogs()

bot.run(token)
