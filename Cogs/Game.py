import nextcord as discord
from nextcord.ext import commands
import pymongo
import os
import dotenv
import random
from datetime import datetime

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
                "coins": 1000,
                "level": 1,
                "xp": 0,
            })

            embed = discord.Embed(
                title="Welcome to the game!",
                description="You have been added to the game.\nYou have received 1000 coins.\nUse `tdaily` to claim your daily reward.\nUse `tcf <coins>` to flip a coin.",
                color=0x00e28d
            )
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
            embed.set_thumbnail(url=self.bot.user.avatar)
            embed.set_footer(text="© Binary Bit Lab with Project Light")

            await ctx.send(embed=embed)
            self.setup_complete.add(ctx.author.id)
        else:
            await ctx.send("You are already in the game.")

    @commands.command(name="daily", description="Gives you your daily reward.")
    @commands.cooldown(1, 60 * 60 * 24, commands.BucketType.user)
    async def daily(self, ctx):
        collection = db["Players"]
        player = collection.find_one({"_id": ctx.author.id})

        if not player:
            await ctx.send("You are not in the game. User `tstart` to start the game.")
            return
        
        reward = random.randint(100, 1000)

        balance = player.get("coins", 0) + reward
        collection.update_one(
            {"_id": ctx.author.id},
            {"$set": {"coins": balance}}
        )

        await ctx.send(f"You have received {reward} coins.")

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            retry_after_timestamp = int(datetime.utcnow().timestamp() + error.retry_after)
            await ctx.send(f"Nuh uh. Please try again in <t:{retry_after_timestamp}:R>.")
        else:
            await ctx.send(f"An error occurred: {error}")

    @commands.command(name="coinflip", description="Flips a coin and you can win or lose coins.", aliases=["cf"])
    async def coinflip(self, ctx, coins: int, heads_or_tails: str = "heads"):

        if not isinstance(coins, int):
            await ctx.send("Please enter only numbers.")
            return

        if coins <= 0:
            await ctx.send("Please enter a positive number of coins to flip.")
            return
        
        collection = db["Players"]
        player = collection.find_one({"_id": ctx.author.id})
        
        if not player:
            await ctx.send("You are not in the game. Use `tstart` to start.")
            return
        
        balance = player.get("coins", 0)
        
        if balance < coins:
            await ctx.send(f"You do not have enough coins. You have {balance} coins.")
            return
        
        if heads_or_tails not in ["heads", "tails"]:
            await ctx.send("Please specify 'heads' or 'tails' for the coin flip.")
            return

        result = random.choice(["heads", "tails"])

        if result == heads_or_tails:
            balance += coins
            collection.update_one(
                {"_id": ctx.author.id},
                {"$set": {"coins": balance}}
            )
            await ctx.send(f"You flipped {heads_or_tails} and won. You now have {balance} coins.")
        else:
            balance -= coins
            collection.update_one(
                {"_id": ctx.author.id},
                {"$set": {"coins": balance}}
            )
            await ctx.send(f"You flipped {heads_or_tails} and lost. You now have {balance} coins.")

def setup(bot):
    bot.add_cog(Game(bot))
