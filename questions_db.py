import sqlite3

conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS questions(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    assessment_code TEXT,

    question TEXT,

    option_a TEXT,

    option_b TEXT,

    option_c TEXT,

    option_d TEXT,

    answer TEXT

)
""")

conn.commit()
conn.close()

print("Questions Table Created Successfully ✅")