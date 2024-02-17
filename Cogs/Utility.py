import nextcord as discord
from nextcord.ext import commands
from datetime import datetime

class Utility(commands.Cog):
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

    @commands.command(name="info", description="Gives information about the bot.")
    async def info(self, ctx):
        embed = discord.Embed(
            title="Bot Information!",
            description="I am a bot made by no_gaming_01.",
            color=0x00e28d,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text="Made with ❤️ by no_gaming_01.\n© Binary Bit Lab with Project Light")

        await ctx.send(embed=embed)

    @commands.command(name="support", description="Gives the support server of the bot.")
    async def support(self, ctx):
        embed = discord.Embed(
            title="Support Server!",
            description="Join the support server for the bot.",
            color=0x00e28d,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text="© Binary Bit Lab with Project Light")
        embed.add_field(name="Link:", value="https://dsc.gg/binaybitlab", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="github", description="Gives the github repository of the bot.")
    async def github(self, ctx):
        embed = discord.Embed(
            title="Github Repository!",
            description="Check out out GitHub Organization.",
            color=0x00e28d,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text="© Binary Bit Lab with Project Light")
        embed.add_field(name="Link:", value="https://github.com/binary-bit-lab", inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))
