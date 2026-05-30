import sqlite3

conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS results(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_name TEXT,

    assessment_code TEXT,

    assessment_title TEXT,

    score INTEGER,

    total_questions INTEGER,

    percentage REAL

)
""")

conn.commit()
conn.close()

print("Results Table Created Successfully ✅")