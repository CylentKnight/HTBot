############################################################
# HTBot
# Lead: Jack "Cylent Knight" Lambert
# Contributors: Nate Singer
# Description: A discord bot for groups centered around HTB
# The bot acts as a local group scoring server.
#############################################################
#
#   General Actions which can be performed by @everyone
#
#############################################################

import discord
import sqlite3
from datetime import datetime
from discord.ext import commands


class GeneralActions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("GeneralActions Loaded")

    @commands.command()
    async def cheers(self, ctx, user: discord.Member = None):
        give = str(ctx.author)
        user = str(user)
        if user is None:
            await ctx.send("You have to tag someone \'.cheers @someone\'")
            return

        if give == user:
            await ctx.send("I like congratulating myself too sometimes!")
            return

        limit = check_limit(give)
        if limit:
            await ctx.send("Sorry, you can only give cheers twice per day")
            return

        r = announce(ctx, give, "giveCheers", user)
        await ctx.send(r)
        r = announce(ctx, user, "gotCheers", give)
        await ctx.send(r)
        print(f"INFO: {give} gave cheers to {user}")
        return

    @commands.command()
    async def scoreboard(self, ctx, term="month"):
        term = term.lower()
        if term == "month":
            field = "monthlyPoints"
            banner = "MONTHLY TOP 5"
        elif term == "year":
            field = "yearlyPoints"
            banner = "YEARLY TOP 5"
        elif term == "all":
            field = "allTimePoint"
            banner = "ALL TIME TOP 5"
        else:
            await ctx.send("```Only Month, year and all are acceptable terms, defaulting to month```")
            field = "monthlyPoints"
            banner = "MONTHLY TOP 5"

        conn = sqlite3.connect('./db/htb_db.db')
        c = conn.cursor()
        c.execute(f"SELECT userName, {field} FROM users ORDER BY {field} DESC LIMIT 5")
        query = c.fetchall()
        r = "```"
        r += f"\t\t{banner}\n"
        r += f"\t\t{'=' * len(banner)}\n"
        for i in range(0, 5):
            r += f"{i + 1}: {query[i][1]} Points\t\t{query[i][0]}\n"
        r += "```"

        await ctx.send(r)
        print(f"INFO: Scoreboard query by {ctx.author}")
        return


def setup(client):
    client.add_cog(GeneralActions(client))


def announce(ctx, uname, action, affected=""):
    now = datetime.now().strftime("%D")
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("SELECT * FROM actions WHERE name= ?", (action,))
    actionmeta = c.fetchone()
    conn.commit()
    if actionmeta is None:
        r = f"Unable to find {action}"
        return r
    points = actionmeta[1]
    r = "```"
    r += f"{uname} {actionmeta[2]} {affected} and received {str(actionmeta[1])} point(s)!"
    r += "```"

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
    c.execute(f"""UPDATE users 
        SET monthlyPoints = (monthlyPoints + {points}),
        yearlyPoints = (yearlyPoints + {points}),
        allTimePoint = (allTimePoint + {points}),
        cheers = (cheers + 1)
        WHERE userName= ?""", (uname,))
    conn.commit()
    conn.close()

    return r


def check_limit(uname):
    now = datetime.now().strftime("%D")
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("SELECT dateTime, "
              "member, "
              "action "
              "FROM activity "
              "WHERE dateTime= ? AND member= ? AND action= 'giveCheers'", (now, uname))
    r = c.fetchall()
    if len(r) > 1:
        return True
    return False
