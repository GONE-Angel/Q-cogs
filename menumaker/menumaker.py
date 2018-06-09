from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks
import os
import re
import discord
import pickle
import asyncio
import threading

class Menumaker:
    def __init__(self, bot):
        self.msgMetaLock = threading.Lock()
        self.bot = bot
        self.pages = (
            { "title": 'Page 1', "colour": 0xba4b5b, "description":
				'Sample text\n'
				"'''edit this cog and add 'your text\n' under this to make a new line of text'''"
            },
            { "title": 'Page 2', "colour": 0xba4b5b, "description":
                'Make sure to edit this cog in [Notepad++](https://notepad-plus-plus.org/download/)\n'
            },
            { "title": 'Page 3', "colour": 0xba4b5b, "description":
                "Use 0x[hex color] and place it where\n"
				"'0xba4b5b' is at te moment.\n"
				"This is when you opened this cog with notepad++ ofcourse\n"
            },
            { "title": 'Change the title', "colour": 0xba4b5b, "description":
                "By editing 'change the title and the 'page x'\n"
            },
            { "title": 'Need help?', "colour": 0xffffff, "description":
                'Join my server and look for me!\n'
                'http://join.chillbar.org/\n'
                'The owner of the server, Ginger.\n'
            },
			{ "title": '...', "colour": 0xba4b5b, "description":
                '...\n'
                '...\n'
                '...\n'
            }     
        )
        self.metadataFile = "data/menumaker/messages-metadata.bin"
        self.emoji = {
            0: "0⃣",
            1: "1⃣",
            2: "2⃣",
            3: "3⃣",
            4: "4⃣",
            5: "5⃣",
            6: "6⃣",
            7: "7⃣",
            8: "8⃣",
            9: "9⃣",
            10: "🔟",
            "next": "➡",
            "back": "⬅",
            "yes": "✅",
            "no": "❌"
        }       
        self.reacts = {v: k for k, v in self.emoji.items()}
        self.msgMeta = {}
        if os.path.exists(self.metadataFile):
            self.loadMeta()

    def loadMeta(self):
        try:
            with open(self.metadataFile, 'rb') as file:
                self.msgMeta = pickle.load(file)
        except:
            pass
    
    def saveMeta(self):
        with open(self.metadataFile, 'wb') as file:
            pickle.dump(self.msgMeta, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    async def addMessageToCache(self, channel, messageId):
        for m in self.bot.messages:
            if messageId == m.id:
                return True
        try:
            msg = await self.bot.get_message(channel, messageId)
            self.bot.messages.append(msg)
            return True
        except:
            return False

    async def addAllMessagesToCache(self):
        if self.msgMetaLock.acquire(blocking=False):
            try:
                for channelId in self.msgMeta:
                    ch = self.bot.get_channel(channelId)
                    if ch != None:
                        for msgId in self.msgMeta[channelId]:
                            if not await self.addMessageToCache(ch, msgId):
                                self.msgMeta[channelId].pop(msgId, None)
            except RuntimeError:
                pass
            finally:
                self.msgMetaLock.release()

    def perms(self, message):
        user = message.server.get_member(self.bot.user.id)
        return message.channel.permissions_for(user)

    async def addEditMenuMessage(self, channel, message, pages, page):
        if message:
            if type(pages[page]) == discord.Embed:
                return await self.bot.edit_message(message, embed=pages[page])
            else:
                return await self.bot.edit_message(message, pages[page])
        else:
            if type(pages[page]) == discord.Embed:
                return await self.bot.send_message(channel,
                                                   embed=pages[page])
            else:
                return await self.bot.say(pages[page])
            
    async def showMenu(self, channel, oldMessage, pages, page):
        message = await self.addEditMenuMessage(channel, oldMessage, pages, page)
        self.msgMetaLock.acquire()
        try:
            if not channel.id in self.msgMeta:
                self.msgMeta[channel.id] = {}
            self.msgMeta[channel.id][message.id] = { "pageNr": page, "pages": pages }
        finally:
            self.msgMetaLock.release()
        await self.bot.add_reaction(message, str(self.emoji['back']))
        await self.bot.add_reaction(message, str(self.emoji['next']))
        self.saveMeta()

    async def menuReaction(self, user, channel, reaction, message, pages, page):
        if reaction is None:
            return

        react = self.reacts[reaction.emoji]

        if react == "next":
            page += 1
        if react == "back":
            page -= 1

        nrOfPages = len(pages)
        if page < 0:
            page = nrOfPages - 1
        if page == nrOfPages:
            page = 0
            
        if self.perms(message).manage_messages:
            await self.bot.remove_reaction(message, self.emoji[react], user)
        else:
            await self.bot.delete_message(message)
            self.msgMetaLock.acquire()
            try:
                self.msgMeta[channel.id].pop(message.id, None)
            finally:
                self.msgMetaLock.release()
            message = None
        
        return await self.showMenu(channel, message, pages, page)

    @commands.group(aliases=["menu"], pass_context=True, no_pm=True)
    async def showMenuCommand(self, ctx):
        pages = []
        for p in self.pages:
            em = discord.Embed(title=p["title"], description=p["description"], colour=p["colour"])
            pages.append(em)
        await self.showMenu(ctx.message.channel, None, pages, page=0)

    @commands.group(aliases=["fixmenu"], pass_context=True, no_pm=True)
    async def fixMenu(self, ctx):
        await self.addAllMessagesToCache()

    async def on_reaction_add(self, reaction, user):
        if user.id == self.bot.user.id:
            return
        def checkReaction(reaction, user):
            e = str(reaction.emoji)
            return e.startswith(('➡', '⬅'))
        if checkReaction(reaction, user) and reaction.message.channel.id in self.msgMeta and reaction.message.id in self.msgMeta[reaction.message.channel.id]:
            await self.menuReaction(user, reaction.message.channel, reaction, reaction.message,
                                    self.msgMeta[reaction.message.channel.id][reaction.message.id]["pages"],
                                    self.msgMeta[reaction.message.channel.id][reaction.message.id]["pageNr"])

    async def reAddMessagesToCacheTask(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(5) # in seconds
        while not self.bot.is_closed:
            await self.addAllMessagesToCache()
            await asyncio.sleep(60) # in seconds

def check_folders():
    if not os.path.exists("data/menumaker"):
        print("Creating data/menumaker folder...")
        os.makedirs("data/menumaker")

reAddTask = None

def setup(bot):
    check_folders()
    MenumakerCog = Menumaker(bot)
    bot.add_cog(MenumakerCog)
    global reAddTask
    if reAddTask:
        reAddTask.cancel()
    reAddTask = bot.loop.create_task(MenumakerCog.reAddMessagesToCacheTask())

def teardown(bot):
    global reAddTask
    if reAddTask:
        reAddTask.cancel()
        reAddTask = None
