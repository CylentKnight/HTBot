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
from datetime import datetime
from discord.ext import commands

class HnHActions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("HnHActions Loaded")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def bringbeer(self, ctx):
        await ctx.send("This command will be used if someone brings beer to a home event")
        return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def buybeer(self, ctx):
        await ctx.send("This command will be used if someone buys a beer at a business hosted event")
        return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def sharebeer(self, ctx):
        await ctx.send("This command will be used if someone buys a beer for a friend at a business hosted event")
        return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def hosted(self, ctx):
        await ctx.send("This command will be used if someone hosts and event")
        return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def attended(self, ctx):
        await ctx.send("This command will be used if someone attends an event")
        return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def eom(self, ctx):
        await ctx.send("This command will be used to reset monthly points")
        return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def eoy(self, ctx):
        await ctx.send("This command will be used to reset annual points")
        return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def gift(self, ctx, uname: discord.Member = None, pts = 0):
        if uname is None or pts == 0:
            await ctx.send("USAGE: .gift <tag member> <points>")
            return

        uname = str(uname)

        user = check_user(uname)
        if user is None:
            await ctx.send("I couldn't find that member are they registered?")
            return

        add_points(uname, pts)

        await ctx.send(f"Awarded {str(pts)} points to {uname}")
        return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def referral(self, ctx, uname: discord.Member = None):
        if uname is None:
            await ctx.send("USAGE: .referral <username>\nPlease use the name of the user who referred a new member")
            return
        uname = str(uname)
        action = "refer"
        r = update_activity_db(uname, action)
        await ctx.send(r)
        return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ctf(self, ctx, uname: discord.Member = None):
        if uname is None:
            await ctx.send("USAGE: .ctf <member tag>")
            return

        uname = str(uname)
        user = check_user(uname)

        if user is None:
            await ctx.send("I couldn't find that user, are you sure they're registered?")
            return

        action = "ctf"
        r = update_activity_db(uname, action)
        await ctx.send(r)
        return

    @commands.command()
    #@commands.has_permissions(administrator=True)
    @commands.has_permissions(ban_members=True)
    async def writeup(self, ctx, uname: discord.Member = None):
        if uname is None:
            await ctx.send("USAGE: .ctf <member tag>")
            return

        uname = str(uname)
        user = check_user(uname)

        if user is None:
            await ctx.send("I couldn't find that user, are you sure they're registered?")
            return

        action = "writeup"
        r = update_activity_db(uname, action)
        await ctx.send(r)
        return

def setup(client):
    client.add_cog(HnHActions(client))


def update_activity_db(uname, action, affected=None):
    now = datetime.now().strftime("%D")

    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("SELECT * FROM actions WHERE name= ?", (action,))
    action_details = c.fetchone()
    conn.commit()

    if action_details is None:
        return f"Unable to find {action}"

    points = action_details[1]
    message = action_details[2]

    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("INSERT INTO activity("
              "dateTime, "
              "member, "
              "action, "
              "affected, "
              "result) "
              "VALUES (?,?,?,?,?)", (now, uname, action, affected, points))
    conn.commit()
    conn.close()
    r = announce(uname, message, affected, points)
    if points:
        add_points(uname, points)
    return r


def add_points(uname, points):
    print(f"Adding {points} points to {uname}")
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute(f"""UPDATE users 
            SET monthlyPoints = (monthlyPoints + {points}),
            yearlyPoints = (yearlyPoints + {points}),
            allTimePoint = (allTimePoint + {points})
            WHERE userName= ?""", (uname,))
    conn.commit()
    conn.close()


def announce(uname, message, affected=None, points=None):
    if affected and points:
        r = "```"
        r += f"{uname} {message} {affected} and received {str(points)} point(s)!"
        r += "```"
    elif points:
        r = "```"
        r += f"{uname} {message} and received {str(points)} point(s)!"
        r += "```"
    elif affected:
        r = "```"
        r += f"{uname} {message} {affected}"
        r += "```"
    else:
        r = "```"
        r += f"{uname} {message}"
        r += "```"
    return r

def check_user(uname):
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE userName= ?", (uname,))
    r = c.fetchone()
    conn.close()
    return r