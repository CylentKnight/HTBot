import discord
import os
from discord.ext import commands

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

#@client.event
#async def on_member_join(member):
#    await channel.general.send(f'Hello, {member}. Please type \'.welcome\' for the official welcome message and rules.')

client.run('Njg0MTU4NDExMzU2NzY2MjA4.Xl2EAA.m5BCOldetx7dz3dTG18uRQjby-4')