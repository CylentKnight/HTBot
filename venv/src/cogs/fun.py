############################################################
# HTBot - funActions cog
# Lead: Jack "Cylent Knight" Lambert
# Description: A discord bot for groups centered around HTB
# The bot acts as a local group scoring server.
#############################################################
#
#   trolly actions
#
#############################################################
import discord
import random
from discord.ext import commands


class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("funActions Loaded")

    @commands.command()
    async def magic(self, ctx, *, question = None):
        if question is None:
            await ctx.send("You shake the magic ball but nothing happens")
            return
        else:
            response = [
                "As I see it, yes",
                "Ask again later",
                "Better not tell you now",
                "Cannot predict now",
                "Concentrate and ask again",
                "Don't count on it",
                "It is certain",
                "It is decidedly so",
                "Most likely",
                "My reply is no",
                "My sources say no",
                "Outlook is not good",
                "Outlook is good",
                "Reply hazy, try again",
                "Signs point to yes",
                "Very doubtful",
                "Yes",
                "Definitely yes",
                "You may rely on it"
            ]
            await ctx.send(response[random.randrange(19)])
        return

    @commands.command()
    async def lmgtfy(self, ctx, *, content = None):
        if content is None:
            await ctx.send("I need something to search for")
            return
        else:
            content = content.replace(" ", "+")
        #await ctx.send("Returns a link to lmgtfy")
        r = f"https://lmgtfy.com/?q={content}&iie=1"
        await ctx.send(r)
        return

    @commands.command()
    async def rr(self, ctx):

        response = [
            "clack, you're safe",
            "clack, you're safe",
            "BOOM!! You didn't make it",
            "clack, you're safe",
            "clack, you're safe",
            "clack, you're safe",
        ]
        await ctx.send("Spiiiiii.i..innn.. CLICK.. {}".format(response[random.randrange(5)],))
        return

def setup(client):
    client.add_cog(fun(client))