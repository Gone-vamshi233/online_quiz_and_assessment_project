from flask import Flask, render_template, request, redirect, session
from google import genai
from dotenv import load_dotenv
import os
import json
import sqlite3
import random

load_dotenv()

app = Flask(__name__)
app.secret_key = "quiz_secret_key"

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
@app.route('/generate_quiz', methods=['GET', 'POST'])
def generate_quiz():

    if request.method == 'POST':

        topic = request.form['topic']
        num_questions = request.form['num_questions']

        prompt = f"""
Generate {num_questions} MCQs on {topic}.

Return ONLY JSON.

Format:

[
  {{
    "question":"...",
    "option_a":"...",
    "option_b":"...",
    "option_c":"...",
    "option_d":"...",
    "answer":"A"
  }}
]
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        clean_text = response.text.replace(
            "```json", ""
        ).replace(
            "```", ""
        ).strip()

        questions = json.loads(clean_text)

        return render_template(
            "student_quiz.html",
            questions=questions
        )

    return render_template("generate_quiz.html")

@app.route('/')
def home():
    return render_template("home.html")
import sqlite3

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("quiz.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name,email,password)
        )

        conn.commit()
        conn.close()

        return redirect('/student_login')

    return render_template('register.html')
@app.route('/student_login', methods=['GET','POST'])
def student_login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("quiz.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email,password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session['student_name'] = user[1]

            return redirect('/student_dashboard')

        else:
                return render_template(
        "student_login.html",
        error="❌ Invalid Email or Password"
    )

    return render_template('student_login.html')
@app.route('/admin_login', methods=['GET','POST'])
def admin_login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        if email == "admin@gmail.com" and password == "admin123":

            return redirect('/admin_dashboard')

        return "Invalid Credentials"

    return render_template("admin_login.html")
@app.route('/assessment', methods=['GET','POST'])
def assessment():

    if request.method == 'POST':

        assessment_code = request.form['assessment_code']

        conn = sqlite3.connect("quiz.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM questions
        WHERE assessment_code=?
        """,
        (assessment_code,)
        )

        questions = cursor.fetchall()
        print("Assessment Code:", assessment_code)
        cursor.execute("""
        SELECT duration
        FROM assessments
        WHERE assessment_code=?
        """,
        (assessment_code,)
        )

        assessment_data = cursor.fetchone()
        if assessment_data:
          duration = assessment_data[0]
        else:
          duration = 10

        conn.close()

        if not questions:
          return render_template(
        "invalid_code.html"
    ) 

        return render_template(
            "take_assessment.html",
            questions=questions,
            assessment_code=assessment_code,
            duration=duration
        )

    return render_template('assessment.html')
import random
import sqlite3

@app.route('/create_assessment', methods=['GET', 'POST'])
def create_assessment():

    if request.method == 'POST':

        title = request.form['title']
        topic = request.form['topic']
        difficulty = request.form['difficulty']
        questions = request.form['questions']
        duration = request.form['duration']

        # Generate Assessment Code
        assessment_code = f"QUIZ-{random.randint(1000,9999)}"

        # Gemini Prompt
        prompt = f"""
Generate {questions} MCQs on {topic}.

Difficulty: {difficulty}

Return ONLY JSON.

Format:

[
 {{
  "question":"...",
  "option_a":"...",
  "option_b":"...",
  "option_c":"...",
  "option_d":"...",
  "answer":"A"
 }}
]
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        clean_text = response.text.replace(
            "```json", ""
        ).replace(
            "```", ""
        ).strip()

        generated_questions = json.loads(clean_text)

        conn = sqlite3.connect("quiz.db")
        cursor = conn.cursor()

        # Save Assessment
        cursor.execute("""
        INSERT INTO assessments
        (title, assessment_code, topic, difficulty, questions, duration)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            assessment_code,
            topic,
            difficulty,
            questions,
            duration
        ))

        # Save Questions
        for q in generated_questions:

            cursor.execute("""
            INSERT INTO questions(
                assessment_code,
                question,
                option_a,
                option_b,
                option_c,
                option_d,
                answer
            )
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                assessment_code,
                q["question"],
                q["option_a"],
                q["option_b"],
                q["option_c"],
                q["option_d"],
                q["answer"]
            ))

        conn.commit()
        conn.close()

        return render_template(
            "assessment_created.html",
            assessment_code=assessment_code,
            title=title,
            topic=topic,
            questions=questions,
            duration=duration
        )

    return render_template('create_assessment.html')
@app.route('/admin_dashboard')
def admin_dashboard():

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM assessments")

    assessments = cursor.fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        assessments=assessments
    )
@app.route('/delete_assessment/<int:id>')
def delete_assessment(id):

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM assessments WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/admin_dashboard')
@app.route('/view_questions/<assessment_code>')
def view_questions(assessment_code):

    return f"""
    Assessment Code:

    {assessment_code}
    """
@app.route('/submit_assessment', methods=['POST'])
def submit_assessment():

    assessment_code = request.form['assessment_code']

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM questions
    WHERE assessment_code=?
    """,
    (assessment_code,)
    )

    questions = cursor.fetchall()

    score = 0

    for q in questions:

        question_id = str(q[0])

        student_answer = request.form.get(
            f"q{question_id}"
        )

        correct_answer = q[7]

        if student_answer == correct_answer:
            score += 1

    total_questions = len(questions)

    percentage = (
        score / total_questions
    ) * 100

    conn.close()

    return render_template(
    "result.html",
    score=score,
    total_questions=total_questions,
    percentage=percentage
)
@app.route('/student_dashboard')
def student_dashboard():

    student_name = session['student_name']

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM results
    WHERE student_name=?
    ORDER BY id DESC
    """,
    (student_name,)
    )

    results = cursor.fetchall()

    conn.close()

    total_quizzes = len(results)

    if total_quizzes > 0:

        average_score = sum(
            row[6] for row in results
        ) / total_quizzes

        best_score = max(
            row[6] for row in results
        )

    else:

        average_score = 0
        best_score = 0

    return render_template(
        "student_dashboard.html",
        student_name=student_name,
        results=results,
        total_quizzes=total_quizzes,
        average_score=average_score,
        best_score=best_score
    )
@app.route('/submit_ai_quiz', methods=['POST'])
def submit_ai_quiz():

    total_questions = int(
        request.form['total_questions']
    )

    score = 0

    for i in range(1, total_questions + 1):

        student_answer = request.form.get(
            f"q{i}"
        )

        correct_answer = request.form.get(
            f"answer{i}"
        )

        if student_answer == correct_answer:
            score += 1

    percentage = (
        score / total_questions
    ) * 100

    student_name = session['student_name']

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO results(
        student_name,
        assessment_code,
        assessment_title,
        score,
        total_questions,
        percentage
    )
    VALUES(?,?,?,?,?,?)
    """,
    (
        student_name,
        "AI-QUIZ",
        "AI Generated Quiz",
        score,
        total_questions,
        percentage
    ))

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        score=score,
        total_questions=total_questions,
        percentage=percentage
    )
@app.route('/results')
def results():

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT DISTINCT
        assessment_title
    FROM results
    """)

    assessments = cursor.fetchall()

    conn.close()

    return render_template(
        "results.html",
        assessments=assessments
    )
@app.route('/view_result/<assessment_title>')
def view_result(assessment_title):

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        student_name,
        score,
        total_questions,
        percentage
    FROM results
    WHERE assessment_title=?
    """,
    (assessment_title,)
    )

    results = cursor.fetchall()

    conn.close()

    return render_template(
        "view_result.html",
        assessment_title=assessment_title,
        results=results
    )
if __name__ == "__main__":
    app.run(debug=True)