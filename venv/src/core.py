import discord
import os
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('./db/htb_db.db')
c = conn.cursor()
c.execute("SELECT key FROM secret WHERE platform='discord'")
key = c.fetchone()
conn.close()

client = commands.Bot(command_prefix = '.')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(key[0])