import sqlite3

conn = sqlite3.connect("quiz.db")

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS assessments(

id INTEGER PRIMARY KEY AUTOINCREMENT,

title TEXT,

assessment_code TEXT UNIQUE,

topic TEXT,

difficulty TEXT,

questions INTEGER,

duration INTEGER

)

""")

conn.commit()

conn.close()

print("Assessment Table Created")