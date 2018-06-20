from discord.ext import commands
import random
import discord

class highfive:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def highfive(self, context, member: discord.Member):
        """Give someone a highfive with a gif :)"""
        author = context.message.author.mention
        mention = member.mention
        
        hug = "**{0} gave {1} a highfive!**"
        
        choices = ['https://i.gifer.com/B0aW.gif', 'http://gifimage.net/wp-content/uploads/2017/09/anime-high-five-gif.gif', 'https://i.gifer.com/QEIo.gif', 'https://78.media.tumblr.com/85b0f366d1c596a7e54ea1496f303ae6/tumblr_nqcba47l1Q1qdl4hco4_500.gif', 'https://i.pinimg.com/originals/fc/b1/44/fcb1446b74166b0860ace50ed8b33686.gif', 'https://data.whicdn.com/images/216194566/original.gif', 'http://1.bp.blogspot.com/-lXQRidJkUSc/UfpI5ZG81_I/AAAAAAAAB_0/MHw4jp6-REU/s1600/high+five.gif']
        
        image = random.choice(choices)
        
        embed = discord.Embed(description=hug.format(author, mention), colour=discord.Colour(0xba4b5b))
        embed.set_image(url=image)

        await self.bot.say(embed=embed)

def setup(bot):
    n = highfive(bot)
    bot.add_cog(n)
