import discord
import sqlite3
from datetime import datetime
from discord.ext import commands


class ProfileActions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("ProfileActions Loaded")

    @commands.command()
    async def register(self, ctx):
        user = str(ctx.author)
        print(f"INFO: Attempting to register {user}")
        r = new_register(ctx, user)
        await ctx.send(r)
        return

    @commands.command()
    async def info(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        r = query_field(user, "*")
        result = f"```Username: {r[0]}\n"
        result += f"Registered: {r[1]}\n"
        result += f"Name: {r[2]} {r[3]}\n"
        result += f"Chapter: {r[4]}\n"
        result += f"eMail: {r[5]}\n"
        result += f"HTB: {r[19]}\n"
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
        print(f"INFO: Full user query by {ctx.author} for {user}")
        await ctx.send(result)
        return

    @commands.command()
    async def social(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        r = query_field(user, "userName, rank, email, facebook, twitter, linkedIn, htb")
        result = f"```Username: {r[0]}\n"
        result += f"Rank: {r[1]}\n"
        result += f"email: {r[2]}\n"
        result += f"HTB: {r[6]}\n"
        result += f"facebook: {r[3]}\n"
        result += f"Twitter: {r[4]}\n"
        result += f"LinkedIN: {r[5]}\n"
        result += "```"
        print(f"INFO: Social query by {ctx.author} for {user}")
        await ctx.send(result)
        return

    @commands.command()
    async def score(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        r = query_field(user, "userName, "
                              "rank, "
                              "userFlags, "
                              "rootFlags, "
                              "challengeFlags, "
                              "monthlyPoints, "
                              "yearlyPoints, "
                              "allTimePoint")
        result = f"```Username: {r[0]}\n"
        result += f"Rank: {r[1]}\n"
        result += f"User Flags: {r[2]}\n"
        result += f"Root Flags: {r[3]}\n"
        result += f"Challenge Flags: {r[4]}\n"
        result += "::POINTS::\n"
        result += f"This Month\t\tThis Year\t\tAll Time\n"
        result += f"{r[5]}\t\t\t\t\t{r[6]}\t\t\t\t{r[7]}"
        result += "```"
        print(f"INFO: Score query by {ctx.author} for {user}")
        await ctx.send(result)
        return

    @commands.command()
    async def first(self, ctx, value=None):
        user = ctx.author
        if value is None:
            r = query_field(user, "firstName")
            await ctx.send(r)
            return
        r = update_field(user, "firstName", value)
        await ctx.send(r)

    @commands.command()
    async def last(self, ctx, value=None):
        user = ctx.author
        if value is None:
            r = query_field(user, "lastName")
            await ctx.send(r)
            return
        r = update_field(user, "lastName", value)
        await ctx.send(r)

    @commands.command()
    async def facebook(self, ctx, value=None):
        user = ctx.author
        if value is None:
            r = query_field(user, "facebook")
            await ctx.send(r)
            return
        r = update_field(user, "facebook", value)
        await ctx.send(r)

    @commands.command()
    async def linkedin(self, ctx, value=None):
        user = ctx.author
        if value is None:
            r = query_field(user, "linkedin")
            await ctx.send(r)
            return
        r = update_field(user, "linkedin", value)
        await ctx.send(r)

    @commands.command()
    async def twitter(self, ctx, value=None):
        user = ctx.author
        if value is None:
            r = query_field(user, "twitter")
            await ctx.send(r)
            return
        r = update_field(user, "twitter", value)
        await ctx.send(r)

    @commands.command()
    async def email(self, ctx, value=None):
        user = ctx.author
        if value is None:
            r = query_field(user, "email")
            await ctx.send(r)
            return
        r = update_field(user, "email", value)
        await ctx.send(r)

    @commands.command()
    async def htb(self, ctx, value=None):
        user = ctx.author
        if value is None:
            r = query_field(user, "htb")
            await ctx.send(r)
            return
        r = update_field(user, "htb", value)
        await ctx.send(r)


def setup(client):
    client.add_cog(ProfileActions(client))


def new_register(ctx, uname):
    now = datetime.now().strftime("%D")

    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()

    # Check to make sure the user doesn't already exist
    c.execute("SELECT * FROM users WHERE userName= ?", (uname,))
    check = c.fetchone()
    conn.commit()
    if check is not None:
        # Fail if user exists
        conn.close()
        print(f"WARNING: Duplicate user attempt for {uname}")
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
    ) VALUES (?,?,0,0,0,0,0,0,0)""", (uname, now))
    conn.commit()

    # Check that the user was successfully added to the database
    c.execute("SELECT * FROM users WHERE userName= ?", (uname,))
    sanity = c.fetchone()
    conn.commit()
    conn.close()
    if sanity is None:
        # Send Fail message back
        print(f"ERROR: Failed to add {uname} to the users db")
        return "Something went wrong"
    print(f"INFO: User, {uname} successfully registered")
    r = announce(ctx, uname, "registered")
    return r


def update_field(uname, field, value):
    uname = str(uname)
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE userName= ?", (uname,))
    check = c.fetchone()
    conn.commit()
    if check is None:
        # If user isn't registered
        return (f"```{uname} isn't registered.```")
    # update the desired field
    c.execute("UPDATE users SET " + field + " = \'" + value + "\' WHERE userName= ?", (uname,))
    conn.commit()
    conn.close()

    print(f"INFO: {uname} field {field} updated to {value}")
    return "Success!"


def query_field(uname, field):
    name = str(uname)
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("SELECT " + field + " FROM users WHERE userName= ?", (name,))
    check = c.fetchone()
    conn.commit()
    conn.close()
    if check is None:
        # Fail if user doesn't exist
        Print(f"WARNING: Unregistered Query for user {uname} and field {field}")
        return "Sorry I could find that"
    return check


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
    r += f"{uname} {actionmeta[2]} {affected}and received {str(actionmeta[1])} points!"
    r += "```"

    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("INSERT INTO activity(dateTime, member, action, affected, result) VALUES (?,?,?,?,?)",
              (now, uname, action, affected, points))
    conn.commit()
    c.execute(f"""UPDATE users 
            SET monthlyPoints = (monthlyPoints + {points}),
            yearlyPoints = (yearlyPoints + {points}),
            allTimePoint = (allTimePoint + {points})
            WHERE userName= ?""", (uname,))
    conn.commit()
    conn.close()

    return r
