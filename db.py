import sqlite3

conn = sqlite3.connect("nutrition.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS meals (
    user TEXT,
    date TEXT,
    food TEXT,
    grams REAL,
    calories REAL,
    protein REAL,
    carbs REAL,
    fat REAL
)
""")

conn.commit()

def add_meal(data):
    c.execute("INSERT INTO meals VALUES (?,?,?,?,?,?,?,?)", data)
    conn.commit()

def get_user_meals(user):
    return c.execute("SELECT * FROM meals WHERE user=?", (user,)).fetchall()