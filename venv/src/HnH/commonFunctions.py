############################################################
# HTBot
# Lead: Jack "Cylent Knight" Lambert
# Contributors: Nate Singer
# Description: A discord bot for groups centered around HTB
# The bot acts as a local group scoring server.
#############################################################
#
#   Common functions
#
#############################################################
from datetime import datetime
import sqlite3

def update_activity_db(uname, action, affected=None):
    now = datetime.now().strftime("%D")

    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute("SELECT * FROM actions WHERE name= ?", (action,))
    action_details = c.fetchone()
    conn.commit()

    if action_details is None:
        return f"Unable to find {action}"

    points = action_details[1]
    message = action_details[2]

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
    conn.close()
    r = announce(uname, message, affected, points)
    if points:
        add_points(uname, points)
    return r


def add_points(uname, points):
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()
    c.execute(f"""UPDATE users 
            SET monthlyPoints = (monthlyPoints + {points}),
            yearlyPoints = (yearlyPoints + {points}),
            allTimePoint = (allTimePoint + {points}),
            cheers = (cheers + 1)
            WHERE userName= ?""", (uname,))
    conn.commit()
    conn.close()


def announce(uname, message, affected=None, points=None):
    if affected and points:
        r = "```"
        r += f"{uname} {message} {affected} and received {str(action_details[1])} point(s)!"
        r += "```"
    if points:
        r = "```"
        r += f"{uname} {message} and received {str(action_details[1])} point(s)!"
        r += "```"
    if affected:
        r = "```"
        r += f"{uname} {message} {affected}"
        r += "```"
    else:
        r = "```"
        r += f"{uname} {message}"
        r += "```"

    return r

def check_user(uname):
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE userName= ?", (uname,))
    r = c.fetchone()
    conn.close()
    return r


def check_box(bname):
    conn = sqlite3.connect('./db/htb_db.db')
    c = conn.cursor()

    c.execute("SELECT * FROM boxes WHERE name= ?", (bname,))
    r = c.fetchone()
    conn.close()
    return r
