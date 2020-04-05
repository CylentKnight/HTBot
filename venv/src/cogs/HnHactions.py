############################################################
# HTBot
# Lead: Jack "Cylent Knight" Lambert
# Contributors: Nate Singer
# Description: A discord bot for groups centered around HTB
# The bot acts as a local group scoring server.
#############################################################
#
#   HnH Specific actions
#
#############################################################
import discord
import sqlite3
from discord.ext import commands

class HnHActions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("HnHActions Loaded")

    @commands.command()
    async def bringbeer(self, ctx):
        await ctx.send("This command will be used if someone brings beer to a home event")
        return

    @commands.command()
    async def buybeer(self, ctx):
        await ctx.send("This command will be used if someone buys a beer at a business hosted event")
        return

    @commands.command()
    async def sharebeer(self, ctx):
        await ctx.send("This command will be used if someone buys a beer for a friend at a business hosted event")
        return

    @commands.command()
    async def hosted(self, ctx):
        await ctx.send("This command will be used if someone hosts and event")
        return

    @commands.command()
    async def attended(self, ctx):
        await ctx.send("This command will be used if someone attends an event")
        return


def setup(client):
    client.add_cog(HnHActions(client))
