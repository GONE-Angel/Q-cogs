import asyncio
import os
import discord
from datetime import datetime
from __main__ import send_cmd_help, settings
from discord.ext import commands
from .utils import checks
from .utils.dataIO import dataIO

class AntiRaid():
    """Alerts Staff about possible incoming raids"""

    def __init__(self, bot):
      self.bot = bot
      self.settings = dataIO.load_json("data/anti_raid/settings.json")

    async def on_member_join(self, member):
      server = member.server
      last_reset = datetime.strptime(self.settings[server.id]["time_since_last_reset"], "%Y-%m-%d %H:%M:%S.%f")
      reset_time = (datetime.now() - last_reset).total_seconds()
      if reset_time > 30:
        self.settings[server.id]["join_count"] = 0
        self.settings[server.id]["time_since_last_reset"] = str(datetime.now())
        dataIO.save_json("data/lockdown/settings.json", self.settings)
      if self.settings[server.id]["join_count"] < self.settings[server.id]["max_joins"]:
        self.settings[server.id]["join_count"] += 1
        dataIO.save_json("data/lockdown/settings.json", self.settings)
        return
      if (self.settings[server.id]["join_count"] >= self.settings[server.id]["max_joins"]) and reset_time <= 30:
        channel_id = self.settings[server.id]["channel"]
        channel = self.bot.get_channel(channel_id)
        await self.bot.send_message(channel, content=":warning: @Staff There is a possible raid happening! :warning:")
        self.settings[server.id]["join_count"] = 0
        self.settings[server.id]["time_since_last_reset"] = str(datetime.now())
        dataIO.save_json("data/lockdown/settings.json", self.settings)
        return

    @commands.group(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def antiraid(self, ctx):
      """Settings for AntiRaid"""
      if ctx.invoked_subcommand is None:
          await self.bot.send_cmd_help(ctx)

    @antiraid.command(pass_context=True, no_pm=True)
    async def channel(self, ctx, channel: discord.Channel):
      """Sets channel the bot should send alerts to"""
      server = ctx.message.server
      if server.id not in self.settings:
          self.settings[server.id] = {}
      if "channel" not in self.settings[server.id]:
          self.settings[server.id]["channel"] = {}
      if channel.id not in self.settings[server.id]["channel"]:
          self.settings[server.id]["channel"] = None
      if "join_count" not in self.settings[server.id]:
        self.settings[server.id]["join_count"] = None
      if "max_joins" not in self.settings[server.id]:
        self.settings[server.id]["max_joins"] = 4
      if "time_since_last_reset" not in self.settings[server.id]:
        self.settings[server.id]["time_since_last_reset"] = None
      if "active" not in self.settings[server.id]:
        self.settings[server.id]["active"] = False

      self.settings[server.id]["channel"] = channel.id
      self.settings[server.id]["join_count"] = 0
      dataIO.save_json("data/anti_raid/settings.json", self.settings)
      await self.bot.say("New active AntiRaid channel set to {}!".format(channel.mention))

    @antiraid.command(pass_context=True, no_pm=True)
    async def max_joins(self, ctx, max_joins: int):
      """Sets # of joins before bot alerts staff (default is 4)"""
      server = ctx.message.server
      if server.id not in self.settings:
          self.settings[server.id] = {}
      if "max_joins" not in self.settings[server.id]:
        self.settings[server.id]["max_joins"] = None
      self.settings[server.id]["max_joins"] = max_joins
      dataIO.save_json("data/anti_raid/settings.json", self.settings)
      await self.bot.say("AntiRaid maximum number of joins per 30 seconds is now {}!".format(max_joins))

    @antiraid.command(pass_context=True, no_pm=True)
    async def active(self, ctx, active: str):
      """Sets whether AntiRaid is active and turned on
      Options for active are true or false"""
      server = ctx.message.server
      active_state = None

      # Error handling
      if server.id not in self.settings:
          await self.bot.say("You must set a channel before activating!")
          return
      if "channel" not in self.settings[server.id]:
          await self.bot.say("You must set a channel before activating!")
          return
      if active.lower() != "true" and active.lower() != "false":
          await self.bot.say("Invalid option entered!")
          return
      else:
          if active.lower() == "true":
              active_state = True
              state = "ON"
          else:
              active_state = False
              state = "OFF"
      if "active" not in self.settings[server.id]:
          self.settings[server.id]["active"] = {}
      self.settings[server.id]["active"] = active_state
      self.settings[server.id]["time_since_last_reset"] = str(datetime.now())
      dataIO.save_json("data/lockdown/settings.json", self.settings)
      channel_id = self.settings[server.id]["channel"]
      channel = self.bot.get_channel(channel_id)
      await self.bot.say("Active setting has been applied and is now {} for channel {}!".format(state, channel.mention))

def check_folder():
  if not os.path.isdir("data/anti_raid"):
      os.mkdir("data/anti_raid")

def check_file():
  if not dataIO.is_valid_json("data/anti_raid/settings.json"):
      dataIO.save_json("data/anti_raid/settings.json", {})

def setup(bot):
  check_folder()
  check_file()
  bot.add_cog(AntiRaid(bot))
