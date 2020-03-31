import discord
import sqlite3
from datetime import datetime
from discord.ext import commands

class profileActions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("profileActions Loaded")

    @commands.command()
    async def register(self, ctx):
        user = str(ctx.author)

        r = newRegister(ctx,user)
        await ctx.send(r)

    @commands.command()
    async def test(self, ctx, user: discord.Member = None):

        print(user.roles)

    @commands.command()
    async def info(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        r = queryField(user, "*")
        result = f"```Username: {r[0]}\n"
        result += f"Registered: {r[1]}\n"
        result += f"Name: {r[2]} {r[3]}\n"
        result += f"Chapter: {r[4]}\n"
        result += f"eMail: {r[5]}\n"
        result += f"facebook: {r[6]}\n"
        result += f"Twitter:  {r[7]}\n"
        result += f"LinkedIN: {r[8]}\n"
        result += f"Rank: {r[9]}\n"
        result += f"User Pwns: {r[10]}\n"
        result += f"Root Pwns: {r[11]}\n"
        result += f"Challenge Pwns: {r[12]}\n"
        result += f"Badges: {r[13]}\n"
        result += f"Monthly Points: {r[14]}\n"
        result += f"Annual Points: {r[15]}\n"
        result += f"All Time Points: {r[16]}\n"
        result += f"Contributions: {r[17]}\n"
        result += "```"
        await ctx.send(result)
        return

    @commands.command()
    async def social(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        r = queryField(user, "userName, rank, email, facebook, twitter, linkedIn")
        result = f"```Username: {r[0]}\n"
        result += f"Rank: {r[1]}\n"
        result += f"email: {r[2]}\n"
        result += f"facebook: {r[3]}\n"
        result += f"Twitter: {r[4]}\n"
        result += f"LinkedIN: {r[5]}\n"
        result += "```"
        await ctx.send(result)
        return

    @commands.command()
    async def score(self, ctx, user:discord.Member = None):
        if user is None:
            user = ctx.author

        r = queryField(user, "userName, rank, userFlags, rootFlags, challengeFlags, monthlyPoints, yearlyPoints, allTimePoint")
        result = f"```Username: {r[0]}\n"
        result += f"Rank: {r[1]}\n"
        result += f"User Flags: {r[2]}\n"
        result += f"Root Flags: {r[3]}\n"
        result += f"Challenge Flags: {r[4]}\n"
        result += "::POINTS::\n"
        result += f"This Month\t\tThis Year\t\tAll Time\n"
        result += f"{r[5]}\t\t\t\t\t{r[6]}\t\t\t\t{r[7]}"
        result += "```"
        await ctx.send(result)
        return

    @commands.command()
    async def first(self, ctx, value = None):
        user = ctx.author
        if value is None:
            r = queryField(user, "firstName")
            await ctx.send(r)
            return
        r = updateField(user, "firstName", value)
        await ctx.send(r)

    @commands.command()
    async def last(self, ctx, value = None):
        user = ctx.author
        if value is None:
            r = queryField(user, "lastName")
            await ctx.send(r)
            return
        r = updateField(user, "lastName", value)
        await ctx.send(r)

    @commands.command()
    async def facebook(self, ctx, value = None):
        user = ctx.author
        if value is None:
            r = queryField(user, "facebook")
            await ctx.send(r)
            return
        r = updateField(user, "facebook", value)
        await ctx.send(r)

    @commands.command()
    async def linkedin(self, ctx, value = None):
        user = ctx.author
        if value is None:
            r = queryField(user, "linkedin")
            await ctx.send(r)
            return
        r = updateField(user, "linkedin", value)
        await ctx.send(r)

    @commands.command()
    async def twitter(self, ctx, value = None):
        user = ctx.author
        if value is None:
            r = queryField(user, "twitter")
            await ctx.send(r)
            return
        r = updateField(user, "twitter", value)
        await ctx.send(r)

    @commands.command()
    async def email(self, ctx, value = None):
        user = ctx.author
        if value is None:
            r = queryField(user, "email")
            await ctx.send(r)
            return
        r = updateField(user, "email", value)
        await ctx.send(r)

    @commands.command()
    async def htb(self, ctx, value = None):
        user = ctx.author
        if value is None:
            r = queryField(user, "htb")
            await ctx.send(r)
            return
        r = updateField(user, "htb", value)
        await ctx.send(r)

def setup(client):
    client.add_cog(profileActions(client))

def newRegister(ctx, uName):
    #Register a new user
    now = datetime.now().strftime("%D")

    #Initialize connection to db
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()

    # Check to make sure the user doesn't already exist
    print(f"Querying {uName}")
    c.execute("SELECT * FROM users WHERE userName= ?", (uName,))
    check = c.fetchone()
    conn.commit()
    if check is not None:
        # Fail if user exists
        conn.close()
        print(f"WARNING: Duplicate user attempt for {uName}")
        return "User already exists"

    # Create the user entry in the database
    c.execute("""INSERT OR IGNORE INTO users(
    userName,
    registerDate,
    userFlags,
    rootFlags,
    challengeFlags,
    monthlyPoints,
    yearlyPoints,
    allTimePoint,
    donate
    ) VALUES (?,?,0,0,0,0,0,0,0)""", (uName, now))
    conn.commit()

    # Check that the user was successfully added to the database
    c.execute("SELECT * FROM users WHERE userName= ?", (uName,))
    sanity = c.fetchone()
    conn.commit()
    conn.close()
    if sanity is None:
        # Send Fail message back
        print(f"ERROR: Failed to add {uName} to the users db")
        return "Something went wrong"
    print(f"INFO: User, {uName} successfully registered")
    r = announce(ctx,uName,"registered")
    return r


def updateField(uName, field, value):
    uName = str(uName)
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE userName= ?", (uName,))
    check = c.fetchone()
    conn.commit()
    if check is None:
        # If user isn't registered, then register them
        a = newRegister(uName)
        print(f"Auto registered {uName}")
    print("UPDATE users SET ? = \'?\' WHERE userName= ?", (field,value,uName))
    # update the desired field
    c.execute("UPDATE users SET "+ field +" = \'"+ value +"\' WHERE userName= ?", (uName,))
    conn.commit()
    conn.close()

    # # double check that it took
    # c.execute("SELECT ? FROM users WHERE userName = ?", (field, uName))
    # sanity = c.fetchone()
    # if sanity != value:
    #     print(f"ERROR: Failed to update {field} for account {uName}. New Value {value}, current {sanity}")
    #     return "Something went wrong!"
    # print(f"INFO: {uName} successfully updated their {field}")
    print(f"{uName} field {field} updated to {value}")
    return "Success!"


def queryField(uName, field):
    name = str(uName)
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("SELECT " + field + " FROM users WHERE userName= ?", (name,))
    check = c.fetchone()
    conn.commit()
    conn.close()
    if check is None:
        # Fail if user doesn't exist
        return "You aren't registered! Type .register to get started!"
    return check

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
    r += f"{uName} {actionMeta[2]} {affected}and received {str(actionMeta[1])} points!"
    r += "```"

    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("INSERT INTO activity(dateTime, member, action, affected, result) VALUES (?,?,?,?,?)", (now, uName, action, affected, points))
    actionMeta = c.fetchone()
    conn.commit()
    c.execute(f"""UPDATE users 
            SET monthlyPoints = (monthlyPoints + {points}),
            yearlyPoints = (yearlyPoints + {points}),
            allTimePoint = (allTimePoint + {points})
            WHERE userName= ?""", (uName,))
    conn.commit()
    conn.close()

    return r


