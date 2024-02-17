import nextcord as discord
from nextcord.ext import commands
import pymongo
from datetime import datetime

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", aliases=["latency"], description="Shows the bot's latency.")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="Pong! 🏓",
            description=f"I got a ping of {latency}ms.",
            color=0x00e28d,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text="© Binary Bit Lab with Project Light")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utilities(bot))
