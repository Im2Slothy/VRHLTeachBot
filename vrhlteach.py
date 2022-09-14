#Discord Bot Made for VRHL Teaching server#

import datetime
import os
import json
import math
import random
from typing import Optional
from tkinter import Entry
from typing_extensions import Self
import asyncio
import discord
import typing
from discord.ext import commands


intents = discord.Intents.all()

client = commands.Bot(command_prefix = '!', intents = intents)


#----------MEMBER JOIN AND LEAVE---------- BOT GOING ONLINE -----------------------------

@client.event

async def on_ready():

    print('VRHL is ready for service!')


@client.event
async def on_member_join(member):
    guild = client.get_guild(1018541154859491369)
    channel = guild.get_channel('') # NEEDED
    embed=discord.Embed(title="Welcome!", description=f"Hello, {member.mention} Please read below as there might be some info that is of interest to you!")
    embed.set_author(name="VRHL Academic Connection", icon_url="https://media.discordapp.net/attachments/1018541776975437855/1019469381694148638/unknown.png")
    embed.add_field(name="Welcome!", value="Hello and welcome to the VRHL Academic! We hope you enjoy and and find all the help you need!", inline=True)
    embed.add_field(name="Getting Started", value=f"Before you begin your journey in the server make sure to read the rules and agree to them!", inline=True)
    embed.add_field(name="Information", value="Once you are are set and ready to go, we ask that you check out some of the channels below this one! You ask questions there and you're always welcome to answer questions if you become a teacher!", inline=True)
    embed.set_footer(text="Enjoy your stay!")
    role = discord.utils.get(guild.roles, name="Students", id=1018541433642299592)
    await member.add_roles(role)
    await channel.send(embed=embed)




@client.event

async def on_member_remove(member):

        print(f'{member} has left or was removed from {member.guild}')

#------------------------------------Commands---------------------------------------------

@client.command()
@commands.has_permissions(administrator = True)
async def repeat(ctx, *, message):
    await ctx.send(message)
    await ctx.message.delete()

@client.command()
@commands.has_permissions(administrator = True)
async def embed(ctx):
    questions = ["Title?", "Description?"]
    responses = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for question in questions:
        try:
            await ctx.send(question)
            message = await client.wait_for('message', timeout=15, check=check)

        except asyncio.TimeoutError:
            await ctx.send("Timeout")
            return

        else:
            responses.append(message.content)

    embedVar = discord.Embed(title=responses[0], description=responses[1])
    await ctx.send(embed=embedVar)


@client.command()
async def ping(ctx):
    b=discord.Embed(title=f"Ping?!",description=f"Pong! {round(client.latency * 1000)}ms",color=0xFF5733)
    await ctx.send(embed=b)


@client.command(aliases=['8ball', 'test'])

async def _8ball(ctx,*, question):

    responses = ['It is certain',

                     'It is decidedly so',

                     'Without a doubt',

                     'Yes, definitely',

                     'You may rely on it',

                     'As I see it, yes',

                     'Most likely',

                     'Outlook good',

                     'Yes',

                     'Signs point to yes',

                     'Reply hazy try again',

                     'Ask again later',

                     'Better not tell you now',

                     'Cannot predict now',

                     'Concentrate and ask again',

                     'Do not count on it',

                     'My reply is no',

                     'My sources say no',

                     'Outlook not so good',

                     'Very doubtful']

    b=discord.Embed(title=f"The 8Ball Says!",description=f'Question: {question}\nAnswer: {random.choice(responses)}',color=0x660066)
    await ctx.send(embed=b)  



@client.command(aliases=["mc"])

async def members(ctx):

    a=ctx.guild.member_count
    b=discord.Embed(title=f"Members in {ctx.guild.name}",description=a,color=discord.Color((0xffff00)))
    await ctx.send(embed=b)

#MATH TEST #

def add(n: float, n2: float):
    return n + n2

def sub(n: float, n2: float):
    return n - n2

def rando(n: int, n2: int):
    return random.randint(n, n2)

def div(n: float, n2: float):
    return n / n2

def sqrt(n: float):
    return math.sqrt(n)

def mult(n: float, n2: float):
    return n * n2

@client.command()
async def mathadd(ctx, x: float, y: float):
    try:
        result = add(x, y)
        await ctx.send(result)

    except:
        pass

@client.command()
async def mathsub(ctx, x: float, y: float):
    try:
        result = sub(x, y)
        await ctx.send(result)

    except:
        pass

@client.command()
async def mathrando(ctx, x: int, y: int):
    try:
        result = rando(x, y)
        await ctx.send(result)

    except:
        pass

@client.command()
async def mathdiv(ctx, x: float, y: float):
    try:
        result = div(x, y)
        await ctx.send(result)

    except:
        pass

@client.command()
async def mathmult(ctx, x: float, y: float):
    try:
        result = mult(x, y)
        await ctx.send(result)

    except:
        pass

@client.command()
async def mathsqrt(ctx, x: float):
    try:
        result = sqrt(x)
        await ctx.send(result)

    except:
        pass
#------------------------------------Moderation-------------------------------------------

@client.command(description="Clears Chat!") # Kicks people

@commands.has_permissions(administrator = True)

async def clear(ctx, amount=5):

        await ctx.channel.purge(limit=amount)

        await ctx.send('messages have been cleared! That felt good!')



@client.command(description="Kicks People!") # Kicks people

@commands.has_permissions(administrator = True)

async def kick(ctx, member : discord.Member, *, reason=None):

        await member.kick(reason=reason)
        await ctx.sent(f'{member.mention} has been kicked!')




@client.command(description="Bans People!") # Bans people

@commands.has_permissions(administrator = True)

async def ban(ctx, user: typing.Union[discord.Member, int], *, reason=None):
    guild = client.get_guild(665944107025301504)
    if user in ctx.guild.members:
        await user.ban(reason=reason)
        await ctx.send(f'Banned {user.mention} My work here is done. That felt good!')
        #send banned user a message
        await user.send(f'You have been banned from {guild.name} for {reason}\n')
    else:
        await guild.ban(discord.Object(id = user))
        await ctx.reply(f'User has been hackbanned!\nUser: <@{user}>\nThat felt good!')


@client.command(description="Unbans people!")

@commands.has_permissions(administrator = True)


async def unban(ctx, *, member):

    obj = await commands.UserConverter().convert(ctx, member)

    if obj is None:

        id_ = await commands.IDConverter().convert(str(member))

        if id_ is not None:

            try:

                obj = await client.fetch_user(int(id_.group(1)))

            except discord.NotFound:

                obj = None

        if obj is None:

            await ctx.send('User not found')

            return 

    await ctx.guild.unban(obj)

    await ctx.send(f'Unbanned {obj}. That felt good!')


#-------------------------------------------------------------------------------

client.run('TOKEN')
