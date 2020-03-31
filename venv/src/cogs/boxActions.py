import discord
import sqlite3
from discord.ext import commands

class boxActions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("boxActions Loaded")

    @commands.command()
    async def addbox(self, ctx, user: discord.Member = None):
        pass

    @commands.command()
    async def userflag(self, ctx, user: discord.Member = None):
        pass

    @commands.command()
    async def rootflag(self, ctx, user: discord.Member = None):
        pass

    @commands.command()
    async def challenge(self, ctx, user: discord.Member = None):
        pass


def setup(client):
    client.add_cog(boxActions(client))