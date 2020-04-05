############################################################
# HTBot
# Lead: Jack "Cylent Knight" Lambert
# Contributors: Nate Singer
# Description: A discord bot for groups centered around HTB
# The bot acts as a local group scoring server.
#############################################################
#
#   Box specific actions
#
#############################################################

import discord
import sqlite3
from datetime import datetime
from discord.ext import commands


class BoxActions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("BoxActions Loaded")

    @commands.command()
    async def htbaddbox(self, ctx, bname=None, status="Active"):
        if bname is None:
            await ctx.send("```You need to give me the name of the new box\n\'.htbaddbox <box name>\'```")
            return
        platform = "HTB"
        r = addbox(platform, bname.lower(), status)
        await ctx.send(r)
        print(f"INFO: {ctx.author} added {bname} to boxes")
        return

    @commands.command()
    async def userflag(self, ctx, user: discord.Member = None, bname=None):
        platform = "HTB"
        user = str(user)
        if user is None or bname is None:
            await ctx.send("```I need more details\n\'.userflag <@user> <boxName>\'```")
            return
        print(f"userflag sending {platform}, {bname}, {user} and User to pwn function")
        r = pwn(platform, bname, user, "User")
        await ctx.send(r)
        print(f"INFO: User flag submission by {ctx.author} for {user} on {bname}")
        return

    @commands.command()
    async def rootflag(self, ctx, user: discord.Member = None, bname=None):
        platform = "HTB"
        user = str(user)
        if user is None or bname is None:
            await ctx.send("```I need more details\n\'.userflag <@user> <boxName>\'```")
            return
        r = pwn(platform, bname, user, "Root")
        await ctx.send(r)
        print(f"INFO: Root flag submission by {ctx.author} for {user} on {bname}")
        return

    @commands.command()
    async def challenge(self, ctx, user: discord.Member = None):
        pass

    @commands.command()
    async def boxinfo(self, ctx, bname=None, platform="HTB"):
        if bname is None:
            await ctx.send("```I need to know what box\n\'.boxinfo <box name>\'```")
            return
        query = box_existence(platform, bname.lower())
        if query is None:
            await ctx.send(f"```I couldn't find {bname}```")
            return
        r = "```"
        r += f"Name: {query[1]}\n"
        r += f"Platform: {query[0]}\t\tStatus: {query[2]}\n\n"
        r += "Root Pwns\t\t\tUser Pwns\n"
        r += f"{query[6]}\t\t\t\t\t{query[5]}\n\n"
        r += f"First Blood (User): {query[3]}\n"
        r += f"First Blood (Root): {query[4]}```"

        await ctx.send(r)
        print(f"INFO: Box info queried by {ctx.author} for {bname}")
        return


def setup(client):
    client.add_cog(BoxActions(client))


def box_existence(plat, bname):
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()

    c.execute("SELECT * FROM boxes WHERE name= ?", (bname,))
    r = c.fetchone()
    conn.close()
    return r


def user_existence(uname):
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE userName= ?", (uname,))
    r = c.fetchone()
    conn.close()
    return r


def addbox(plat, bname, status):
    bname = bname.lower()
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    query = box_existence(plat, bname)
    if query is not None:
        return("```That box already exists```")

    c.execute("INSERT INTO boxes("
              "platform, "
              "name, "
              "status, "
              "userFlags, "
              "rootFlags)"
              " VALUES (?,?,?,?,?)", (plat, bname, status, 0, 0))
    conn.commit()
    conn.close()
    return("```Box added```")


def pwn(plat, bname, uname, flag_type):
    bname = bname.lower()
    uname = str(uname)

    query = box_existence(plat, bname)
    if query is None:
        return("```That box has not been added```")
    is_active = False
    is_challenge = False

    if query[2] == "Active":
        is_active = True
    elif query[2] == "Challenge":
        is_active = True
        is_challenge = True
        flag_type = "Root"

    is_first = False

    if flag_type == "Root":
        if query[4] is None:
            is_first = True
    else:
        if query[3] is None:
            is_first = True

    user_query = user_existence(uname)
    if user_query is None:
        return("```That user hasn't registered yet!```")

    action_type = f"got{flag_type}"
    if is_challenge:
        action_type = "gotChallenge"

    if action_type == "gotUser":
        flag_field = "userFlags"
    else:
        flag_field = "rootFlags"

    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("SELECT * FROM activity WHERE member= ? AND action = ? AND affected= ?", (uname, action_type, bname))
    actionUniq = c.fetchone()
    if actionUniq is not None:
        return(f"```Looks like {uname} has already pwned that flag```")

    if is_first:
        if flag_type == "User":
            c.execute(f"UPDATE boxes SET {flag_field} = ({flag_field} + 1),"
                      f" userFirstBlood = ? WHERE name= \'{bname}\'", (uname,))
        else:
            c.execute(f"UPDATE boxes SET {flag_field} = ({flag_field} + 1),"
                      f" rootFirstBlood = ? WHERE name= \'{bname}\'", (uname,))
    else:
        c.execute(f"UPDATE boxes SET {flag_field} = ({flag_field} + 1) WHERE name= \'{bname}\'")
    conn.commit()

    c.execute(f"UPDATE users SET {flag_field} = ({flag_field} + 1) WHERE userName = ?", (uname,))
    conn.commit()
    conn.close()
    r = "```"
    r += announce(uname, action_type, bname)
    if is_first and not is_challenge:
        r += "\n"
        r += announce(uname, "firstBlood", bname)
    r += "```"
    return r


def announce(uname, action, affected=""):
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
    r = ""
    r += f"{uname} {actionmeta[2]} {affected} and received {str(actionmeta[1])} points!"

    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("INSERT INTO activity(dateTime, "
              "member, "
              "action, "
              "affected, "
              "result)"
              " VALUES (?,?,?,?,?)", (now, uname, action, affected, points))
    conn.commit()
    c.execute(f"""UPDATE users 
            SET monthlyPoints = (monthlyPoints + {points}),
            yearlyPoints = (yearlyPoints + {points}),
            allTimePoint = (allTimePoint + {points})
            WHERE userName= ?""", (uname,))
    conn.commit()
    conn.close()

    return r
