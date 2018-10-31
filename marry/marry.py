import discord
from discord.ext import commands
from .utils.dataIO import dataIO
import os
import datetime
import copy

class Marry:
    """Marry other users."""

    def __init__(self, bot):
        self.bot = bot
        self.JSON = 'data/marry/marry.json'
        self.data = dataIO.load_json(self.JSON)

    @commands.command(pass_context=True)
    async def marry(self, ctx, user: discord.Member):
        """Marry someone."""
        server = ctx.message.server
        requestor = ctx.message.author.mention
        author = ctx.message.author.display_name
        isbot = self.bot.user.mention

        if user.mention == isbot:
            msg = 'You can\'t get married to the bot.'
            em0 = discord.Embed(description=msg, color=0XF23636)
            await self.bot.say(embed=em0)
            return

        if user.mention == requestor:
            msg = 'You can\'t get married to yourself, crazy guy.'
            em0 = discord.Embed(description=msg, color=0XF23636)
            await self.bot.say(embed=em0)
        if user.id in self.data[server.id]["user"][ctx.message.author.id]["married_to"] and self.data[server.id]["user"][ctx.message.author.id]["married_to"][user.id]["status"] == "married":
            msg = "You're already married to that person!"
            em0 = discord.Embed(description=msg, color=0XF23636)
            await self.bot.say(embed=em0)
        else:
                desc = ":ring:" + author + " *has proposed to* " + user.display_name + ":ring:"
                name = ":church:" + user.display_name + ",  do you accept? :church:"
                em = discord.Embed(description=desc, color=0XF23636)
                em.add_field(name=name, value='Type yes to accept or no to decline.')
                await self.bot.say(embed=em)
                response = await self.bot.wait_for_message(author=user)

                if response.content.lower().strip() == "yes":
                    await self._create_author(server, ctx, user)
                    await self._create_user(server, ctx, user)
                    msg = ":heart: Congratulations " + author + " and " + user.display_name + " :heart:"
                    em1 = discord.Embed(description=msg, color=0XF23636)
                    await self.bot.say(embed=em1)
                    dataIO.save_json(self.JSON, self.data)
                else:
                    msg = "The proposal between " + author + " and " + user.display_name + " has been declined."
                    em2 = discord.Embed(description=msg, color=0XF23636)
                    await self.bot.say(embed=em2)

    @commands.command(pass_context=True)
    async def divorce(self, ctx, user: discord.Member):
        """Divorce someone you are married to."""
        author = ctx.message.author.id
        server = ctx.message.server
        if user.mention == author:
            em0 = discord.Embed(description='You cant\'t divorce yourself, crazy guy!', color=0XF23636)
            await self.bot.say(embed=em0)
        else:
            if server.id not in self.data:
                em = discord.Embed(description='No marriages on this server yet.', color=0XF23636)
                await self.bot.say(embed=em)
                return

            if user.id in self.data[server.id]["user"][ctx.message.author.id]["married_to"] and self.data[server.id]["user"][ctx.message.author.id]["married_to"][user.id]["status"] == "married":
                await self._divorce(server, ctx, user)
                me = ctx.message.author.display_name
                msg = ':broken_heart:  ' + me + ' *has divorced* ' + user.display_name + ' :broken_heart:'
                em = discord.Embed(description=msg, color=0XF23636)
                await self.bot.say(embed=em)
            else:
                msg = 'You can\'t divorce that user because you aren\'t married to them.'
                em = discord.Embed(description=msg, color=0XF23636)
                await self.bot.say(embed=em)

    @commands.command(pass_context=True, no_pm=True)
    async def mlist(self, ctx, user: discord.Member=None):
        """Lists users you are married to. Defaults to author."""
        author = ctx.message.author
        server = ctx.message.server

        if user is None:
            user = author

        if server.id not in self.data:
            msg = 'No marriages on this server yet.'
            em = discord.Embed(description=msg, color=0XF23636)
            await self.bot.say(embed=em)
            return

        if user.id not in self.data[server.id]["user"]:
            msg = 'That person isn\'t married to anyone.'
            em = discord.Embed(description=msg, color=0XF23636)
            await self.bot.say(embed=em)
            return

        mlist = self._populate_list(self.data[server.id]["user"][user.id]["married_to"])

        if mlist:
            names = ''.join(map(str, mlist))
            em = discord.Embed(description="", color=0XF23636)
            em.add_field(name='Married to:', value=names)
            await self.bot.say(embed=em)

        else:
            msg = 'That person isn\'t married to anyone.'
            em = discord.Embed(description=msg, color=0XF23636)
            await self.bot.say(embed=em)

    @commands.command(pass_context=True, no_pm=True)
    async def marriage(self, ctx, user: discord.Member=None):
        """Lists marriage history with a particular user."""
        if not user.id in self.data[ctx.message.server.id]["user"][ctx.message.author.id]["married_to"]:
            msg = "You've never been married to this person."
            em = discord.Embed(description=msg, color=0XF23636)
            await self.bot.say(embed=em)
            return
        msg = "***Marriage history between __{}__ and __{}__***".format(ctx.message.author.display_name, user.display_name)
        for i in self.data[ctx.message.server.id]["user"][ctx.message.author.id]["married_to"][user.id]["history"]:
            msg += "\n {}".format(i)
        em = discord.Embed(description=msg, color=0XF23636)
        await self.bot.say(embed=em)

    @commands.command(pass_context=True, no_pm=True)
    async def updatemarriages(self, ctx):
        """Changes usernames to IDs and updates data format of marriages."""
        await self._update_data(ctx.message.server)

    async def _update_data(self, server):
        usernames = {}
        if server.id not in self.data:
            self.data[server.id] = {}
            return
        for user in self.data[server.id]["user"]:
            if len(user) == 18 and len(int(user)) == 18:
                continue
            if user in usernames:
                usernames[user] = 'dupe'
                continue
            usernames[user] = ''
        for member in server.members:
            if member.name in usernames:
                if usernames[member.name] == '':
                    usernames[member.name] = member.id
                else:
                    del usernames[member.name]
        for user in self.data[server.id]["user"]:
            for spouse in self.data[server.id]["user"][user]["married_to"]:
                if spouse in usernames:
                    del self.data[server.id]["user"][user]["married_to"][spouse]
                    if usernames[spouse] == "dupe" or usernames[spouse] == "":
                        continue
                    self.data[server.id]["user"][user]["married_to"][usernames[spouse]] = self.new_marriage({})
                elif not self.data[server.id]["user"][user]["married_to"][spouse]:
                    self.data[server.id]["user"][user]["married_to"][spouse] = self.new_marriage({})
            if user in usernames:
               self.data[server.id]["user"][usernames[user]] = copy.deepcopy(self.data[server.id]["user"][user])
               del self.data[server.id]["user"][user]
        dataIO.save_json(self.JSON, self.data)

    async def _create_author(self, server, ctx, user):
        author = ctx.message.author.id
        if server.id not in self.data:
            self.data[server.id] = {}
            dataIO.save_json(self.JSON, self.data)
        if "user" not in self.data[server.id]:
            self.data[server.id]["user"] = {}
            dataIO.save_json(self.JSON, self.data)
        if author not in self.data[server.id]["user"]:
            self.data[server.id]["user"][author] = {}
            dataIO.save_json(self.JSON, self.data)
        if "married_to" not in self.data[server.id]["user"][author]:
            self.data[server.id]["user"][author]["married_to"] = {}
            dataIO.save_json(self.JSON, self.data)
        if user.id not in self.data[server.id]["user"][author]["married_to"]:
            self.data[server.id]["user"][author]["married_to"][user.id] = self.new_marriage({})
        else:
            self.data[server.id]["user"][author]["married_to"][user.id] = self.new_marriage(self.data[server.id]["user"][author]["married_to"][user.id])
        dataIO.save_json(self.JSON, self.data)

    async def _create_user(self, server, ctx, user):
        author = ctx.message.author.id
        if server.id not in self.data:
            self.data[server.id] = {}
            dataIO.save_json(self.JSON, self.data)
        if "user" not in self.data[server.id]:
            self.data[server.id]["user"] = {}
            dataIO.save_json(self.JSON, self.data)
        if user.id not in self.data[server.id]["user"]:
            self.data[server.id]["user"][user.id] = {}
            dataIO.save_json(self.JSON, self.data)
        if "married_to" not in self.data[server.id]["user"][user.id]:
            self.data[server.id]["user"][user.id]["married_to"] = {}
            dataIO.save_json(self.JSON, self.data)
        if author not in self.data[server.id]["user"][user.id]["married_to"]:
            self.data[server.id]["user"][user.id]["married_to"][author] = self.new_marriage({})
        else:
            self.data[server.id]["user"][user.id]["married_to"][author] = self.new_marriage(self.data[server.id]["user"][user.id]["married_to"][author])
        dataIO.save_json(self.JSON, self.data)

    async def _divorce(self, server, ctx, user):
        author = ctx.message.author.id
        self.data[server.id]["user"][author]["married_to"][user.id]["history"].append("Divorced: {}".format(datetime.datetime.today().strftime('%Y-%m-%d')))
        self.data[server.id]["user"][author]["married_to"][user.id]["status"] = "divorced"
        self.data[server.id]["user"][user.id]["married_to"][author]["history"].append("Divorced: {}".format(datetime.datetime.today().strftime('%Y-%m-%d')))
        self.data[server.id]["user"][user.id]["married_to"][author]["status"] = "divorced"
        dataIO.save_json(self.JSON, self.data)

    def new_marriage(self, m_obj):
        default_marriage = {"status":"married", "history":["Married: {}".format(datetime.datetime.today().strftime('%Y-%m-%d'))]}
        if not m_obj:
            return default_marriage
        marriage = copy.deepcopy(m_obj)
        marriage[history].append("Married: {}".format(datetime.datetime.today().strftime('%Y-%m-%d')))
        marriage[status] = "married"
        return marriage

    def _populate_list(self, _list):
        """Credit goes to the Owner cog, thank you Twentysix/Sentry (Red-DiscordBot PRs no. 662 & 701)"""
        users = []
        total = len(_list)

        for user_id in _list:
            # serverlist = 
            user = discord.utils.get(self.bot.get_all_members(), id=user_id)
            if user:
                users.append(str(user))

        if users:
            not_found = total - len(users)
            users = ", ".join(users)
            if not_found:
                users += "\n\n ... and {} users I could not find in any servers I'm in.".format(not_found)
            return list(users)

        return []


def check_folder():
    if not os.path.exists('data/marry'):
        print('Creating data/marry folder...')
        os.makedirs('data/marry')


def check_file():
    f = 'data/marry/marry.json'
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, {})
        print('Creating default married.json...')


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Marry(bot))
