import sqlite3

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
    userFirstBlood
    rootFirstBlood
    userFlags
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
    description text)
""")

conn.commit()

conn.close()