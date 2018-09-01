from discord.ext import commands
import random
import discord

class lick:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def lick(self, context, member: discord.Member):
		author = context.message.author.mention
		mention = member.mention
		lick = "**{0} licks {1}!**"
		choices = ['https://media.giphy.com/media/12MEJ2ArZc23cY/source.gif', 'http://gifimage.net/wp-content/uploads/2017/09/anime-lick-gif-12.gif', 'https://i.pinimg.com/originals/e6/1d/a7/e61da774938e4f209818edcbc0d4a671.gif', 'https://68.media.tumblr.com/b80cda919b3309f2cb974635e429db57/tumblr_osuazevFcj1qcsnnso1_500.gif']
		image = random.choice(choices)
		embed = discord.Embed(description=lick.format(author, mention), colour=discord.Colour(0xba4b5b))
		embed.set_image(url=image)
		await self.bot.say(embed=embed)

def setup(bot):
	n = lick(bot)
	bot.add_cog(n)
