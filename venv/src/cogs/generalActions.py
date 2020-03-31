import discord
import sqlite3
from datetime import datetime
from discord.ext import commands

class generalActions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("generalActions Loaded")

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

        limit = checkLimit(give)
        if limit:
            await ctx.send("Sorry, you can only give cheers twice per day")
            return

        r = announce(ctx, give, "giveCheers", user)
        await ctx.send(r)
        r = announce(ctx, user, "gotCheers", give)
        await ctx.send(r)

def setup(client):
    client.add_cog(generalActions(client))

def announce(ctx, uName, action, affected = ""):
    now = datetime.now().strftime("%D")
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("SELECT * FROM actions WHERE name= ?", (action,))
    actionMeta = c.fetchone()
    conn.commit()
    if actionMeta is None:
        r = f"Unable to find {action}"
        return r
    points = actionMeta[1]
    r = "```"
    r += f"{uName} {actionMeta[2]} {affected} and received {str(actionMeta[1])} point(s)!"
    r += "```"

    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("INSERT INTO activity(dateTime, member, action, affected, result) VALUES (?,?,?,?,?)", (now, uName, action, affected, points))
    conn.commit()
    c.execute(f"""UPDATE users 
        SET monthlyPoints = (monthlyPoints + {points}),
        yearlyPoints = (yearlyPoints + {points}),
        allTimePoint = (allTimePoint + {points}),
        cheers = (cheers + 1)
        WHERE userName= ?""", (uName,))
    conn.commit()
    conn.close()

    return r

def checkLimit(uName):
    now = datetime.now().strftime("%D")
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("SELECT dateTime, member, action FROM activity WHERE dateTime= ? AND member= ? AND action= 'giveCheers'", (now, uName))
    r = c.fetchall()
    if len(r) > 1:
        return True
    return False