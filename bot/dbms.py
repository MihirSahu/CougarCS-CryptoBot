import sqlite3

# User database functions
def userConnect():
    conn = sqlite3.connect("databases/user.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user (id INT PRIMARY KEY, discordId VARCHAR(50))")
    conn.commit()
    conn.close()

def userInsert(discordId):
    conn = sqlite3.connect("databases/user.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO user VALUES(NULL,?)",(discordId))
    conn.commit()
    conn.close()

def userView():
    conn = sqlite3.connect("databases/user.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
    rows = cur.fetchall()
    conn.close()
    return rows

def userSearch(discordId=""): #Only one section should be able to be inputted, so to avoid error set default values to ""
    conn = sqlite3.connect("databases/user.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE discordId=?",(discordId,)) #OR so that only one section can be inputted to get values
    rows = cur.fetchall()
    conn.close()
    return rows

def userDelete(discordId):
    conn = sqlite3.connect("databases/user.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM user WHERE discordId=?",(discordId,))
    conn.commit()
    conn.close()

def userUpdateHappy(discordId, happy):
    conn = sqlite3.connect("databases/user.db")
    cur = conn.cursor()
    cur.execute("UPDATE user SET happy=? WHERE discordId=?",(happy, discordId,))
    conn.commit()
    conn.close()

def userUpdateSad(discordId, sad):
    conn = sqlite3.connect("databases/user.db")
    cur = conn.cursor()
    cur.execute("UPDATE user SET sad=? WHERE discordId=?",(sad, discordId,))
    conn.commit()
    conn.close()
