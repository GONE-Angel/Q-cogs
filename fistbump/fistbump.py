from discord.ext import commands
import random
import discord

class fistbump:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def fistbump(self, context, member: discord.Member):
        """Give someone a fistbump with a gif :)"""
        author = context.message.author.mention
        mention = member.mention
        
        hug = "**{0} gave {1} a fistbump!**"
        
        choices = ['https://i.gifer.com/UPQ.gif', 'https://data.whicdn.com/images/279989055/original.gif', 'https://i.gifer.com/3QdW.gif', 'https://i.pinimg.com/originals/d3/94/6e/d3946e0fc719b6aaaffbb784f693663a.gif', 'https://media1.tenor.com/images/0bfae47add0180fd93b52ebb8bf89dd4/tenor.gif?itemid=5047789', 'https://vignette.wikia.nocookie.net/degrassi/images/f/f1/Gray_and_Natsu_fist_bump.gif/revision/latest?cb=20141021214843', 'https://i.gifer.com/OJ5.gif']
        
        image = random.choice(choices)
        
        embed = discord.Embed(description=hug.format(author, mention), colour=discord.Colour(0xba4b5b))
        embed.set_image(url=image)

        await self.bot.say(embed=embed)

def setup(bot):
    n = fistbump(bot)
    bot.add_cog(n)
