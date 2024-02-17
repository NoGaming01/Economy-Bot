import nextcord as discord
from nextcord.ext import commands
import pymongo
import os
import dotenv

dotenv.load_dotenv()
uri = str(os.getenv("MONGO"))

client = pymongo.MongoClient(uri)
db = client["Main"]

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.setup_complete = set()

    @commands.command(name="start", hidden=True)
    async def start(self, ctx):
        if ctx.author.id in self.setup_complete:
            await ctx.send("You have already started the game.")
            return

        collection = db["Players"]
        player = collection.find_one({"_id": ctx.author.id})

        if not player:
            collection.insert_one({
                "_id": ctx.author.id,
                "name": ctx.author.name,
                "wallet": 1000,
                "bank": 500,
                "level": 1,
                "xp": 0,
                "inventory": ["wooden sword"],
                "equipped": []
            })

            embed = discord.Embed(
                title="Welcome to the game!",
                description="You have been added to the game.\nYou have received 1000 coins in your wallet and 500 coins in the bank.\nYou have also received a wooden sword in your inventory.\nYou can equip the sword by typing `tequip <id>` in the chat.\nYou can start playing by typing `thunt`, `tbattle` or `tcollect <name>`.",
                color=0x00e28d
            )
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
            embed.set_thumbnail(url=self.bot.user.avatar)
            embed.set_footer(text="© Binary Bit Lab with Project Light")

            await ctx.send(embed=embed)
            self.setup_complete.add(ctx.author.id)
        else:
            await ctx.send("You are already in the game.")

def setup(bot):
    bot.add_cog(Game(bot))
