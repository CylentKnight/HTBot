############################################################
# HTBot
# Lead: Jack "Cylent Knight" Lambert
# Contributors: Nate Singer
# Description: A discord bot for groups centered around HTB
# The bot acts as a local group scoring server.
#############################################################
#
#   Edit the discord_key and htb_key then run this file
#   first to create the baseline db.
#
#############################################################

import sqlite3

discord_key = 'ENTER DISCORD API KEY HERE'
htb_key = 'ENTER HTB API KEY HERE'

conn = sqlite3.connect('./db/htb_db.db')
c = conn.cursor()

c.execute("""CREATE TABLE users (
    userName text NOT NULL UNIQUE,
    registerDate text NOT NULL,
    firstName text,
    lastName text,
    chapter integer,
    email text,
    facebook text,
    twitter text,
    linkedIn text,
    rank text,
    userFlags integer,
    rootFlags integer,
    challengeFlags integer,
    badges text,
    monthlyPoints integer,
    yearlyPoints integer,
    allTimePoint integer,
    donate integer,
    cheers integer,
    htb text)
""")
conn.commit()

c.execute("""CREATE TABLE activity (
    dateTime text,
    member text,
    action text,
    affected text,
    result)
""")
conn.commit()

c.execute("""CREATE TABLE boxes (
    platform text,
    name text,
    status text,
    userFirstBlood,
    rootFirstBlood,
    userFlags,
    rootFlags)
""")
conn.commit()

c.execute("""CREATE TABLE badges (
    badgeID int,
    name text,
    description text,
    points integer)
""")
conn.commit()

c.execute("""CREATE TABLE actions (
    name text,
    points int,
    message text
    description text)
""")
conn.commit()

c.execute("""INSERT INTO actions (name, points, message, description)
                    VALUES
                        ('registered', 5, 'has registered', 'Register with the bot'),
                        ('giveCheers', 1, 'raised his glass for', 'Give cheers to another member'),
                        ('gotCheers, 5, 'received cheers from', 'Receive cheers from another member'),
                        ('firstBlood', 10, 'got first blood on', 'Be the first member to earn a flag'),
                        ('gotUser', 10, 'slayed the user on', 'Get a user flag'),
                        ('gotRoot', 10, 'crushed root on', 'Get a root flag'),
                        ('gotChallenge', 5, 'completed the htb challenge', 'Get a challenge flag'),
                        ('donate', 2, 'has donated to the group', 'Donate money to the group')""")

c.execute("""CREATE TABLE secret (
    platform text,
    key text)
""")
conn.commit()

c.execute("INSERT INTO secret(platform, key) VALUES('discord', ?)", (discord_key,))
c.execute("INSERT INTO secret(platform, key) VALUES('htb', ?)", (htb_key,))
conn.commit()

conn.close()
