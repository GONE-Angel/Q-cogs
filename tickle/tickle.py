from discord.ext import commands
import random
import discord

class tickle:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def tickle(self, context, member: discord.Member):
		author = context.message.author.mention
		mention = member.mention
		tickle = "**{0} tickles {1}!**"
		choices = ['https://i.imgur.com/6IrniKg.gif', 'https://i.imgur.com/KKjawkx.gif', 'https://i.imgur.com/2h7F6yo.gif', 'https://78.media.tumblr.com/bec329b48b863f2e211ca7d4e3396ce9/tumblr_og7p24fa3R1vpbklao8_r6_500.gif', 'https://i.pinimg.com/originals/f6/81/93/f68193ba7eaeccc3d999b1da956b2fa3.gif']
		image = random.choice(choices)
		embed = discord.Embed(description=tickle.format(author, mention), colour=discord.Colour(0xba4b5b))
		embed.set_image(url=image)
		await self.bot.say(embed=embed)

def setup(bot):
	n = tickle(bot)
	bot.add_cog(n)
