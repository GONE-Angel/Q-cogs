from discord.ext import commands
import random
import discord

class poke:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def poke(self, context, member: discord.Member):
        """poke someone!"""
        author = context.message.author.mention
        mention = member.mention
        
        poke = "**{0} poked {1}!**"
        
        choices = ['https://pa1.narvii.com/6021/b50b8078fa1d8e8f6d2ebfb085f106c642141723_hq.gif', 'https://media1.tenor.com/images/8fe23ec8e2c5e44964e5c11983ff6f41/tenor.gif', 'https://media.giphy.com/media/WvVzZ9mCyMjsc/giphy.gif', 'https://media.giphy.com/media/pWd3gD577gOqs/giphy.gif', 'http://gifimage.net/wp-content/uploads/2017/09/anime-poke-gif-12.gif', 'https://i.gifer.com/S00v.gif', 'https://i.imgur.com/1NMqz0i.gif']
        
        image = random.choice(choices)
        
        embed = discord.Embed(description=poke.format(author, mention), colour=discord.Colour(0xba4b5b))
        embed.set_image(url=image)

        await self.bot.say(embed=embed)

def setup(bot):
    n = poke(bot)
    bot.add_cog(n)
