from discord.ext import commands
import random
import discord

class Slap:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def slap(self, context, member: discord.Member):
        """Slap a bully!"""
        author = context.message.author.mention
        mention = member.mention
        
        slap = "**{0} slapped {1}!**"
        
        choices = ['http://i.imgur.com/6mOFy3v.gif', 'http://i.imgur.com/jb50TEF.gif', 'http://i.imgur.com/mDSjXer.gif', 'http://i.imgur.com/b8cytk1.gif', 'http://i.imgur.com/Ub8fT3G.gif', 'http://i.imgur.com/jNaAaxn.gif']
        
        image = random.choice(choices)
        
        embed = discord.Embed(description=slap.format(author, mention), colour=discord.Colour(0xba4b5b))
        embed.set_image(url=image)

        await self.bot.say(embed=embed)

def setup(bot):
    n = Slap(bot)
    bot.add_cog(n)
