conn = sqlite3.connect('./db/htb_db.db')
c = conn.cursor()

c.execute("""INSERT INTO actions (name, points, message, description)
                    VALUES
                        ('eventHost', 50, 'hosted an event', 'Host an event'),
                        ('eventAttend, 5, 'attended an event', 'Attend an event'),
                        ('beerBrought', 1, 'brought some beer to an event', 'Bring beer to a home event'),
                        ('beerBought', 3, 'bought themselves a beer', 'Buy a beer at an event hosted at a business'),
                        ('beerShare', 4, 'bought a beer for a friend', 'Buy someone else a beer at a business hosted event)""")
conn.commit()
conn.close()