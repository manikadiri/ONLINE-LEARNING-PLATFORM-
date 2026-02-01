from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "supersecretkey123"

DB_NAME = "database.db"

# ---------------- DATABASE INIT ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS lessons(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        video_path TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS progress(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        lesson_id INTEGER,
        completed INTEGER DEFAULT 0,
        quiz_score INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(lesson_id) REFERENCES lessons(id)
    )
    """)

    # Insert default lessons if empty
    cur.execute("SELECT COUNT(*) FROM lessons")
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute("INSERT INTO lessons(title, video_path) VALUES (?,?)",
                    ("Python Basics", "videos/sample.mp4"))
        cur.execute("INSERT INTO lessons(title, video_path) VALUES (?,?)",
                    ("Flask Web Development", "videos/sample.mp4"))

    conn.commit()
    conn.close()

init_db()

# ---------------- LOGIN REQUIRED DECORATOR ----------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        try:
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()
            cur.execute("INSERT INTO users(name,email,password) VALUES (?,?,?)",
                        (name, email, password))
            conn.commit()
            conn.close()
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for("login"))
        except:
            flash("Email already exists!", "danger")

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials!", "danger")

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    SELECT lessons.id, lessons.title, COALESCE(progress.completed, 0) as completed, progress.quiz_score
    FROM lessons
    LEFT JOIN progress ON lessons.id = progress.lesson_id AND progress.user_id=?
    """, (user_id,))
    lessons = cur.fetchall()
    conn.close()
    return render_template("dashboard.html", lessons=lessons)

# ---------------- COURSE PAGE ----------------
@app.route("/course/<int:lesson_id>")
@login_required
def course(lesson_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM lessons WHERE id=?", (lesson_id,))
    lesson = cur.fetchone()
    conn.close()
    return render_template("course.html", lesson=lesson)

# ---------------- MARK LESSON COMPLETED ----------------
@app.route("/complete/<int:lesson_id>")
@login_required
def complete_lesson(lesson_id):
    user_id = session["user_id"]

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT * FROM progress WHERE user_id=? AND lesson_id=?", (user_id, lesson_id))
    row = cur.fetchone()

    if row:
        cur.execute("UPDATE progress SET completed=1 WHERE user_id=? AND lesson_id=?", (user_id, lesson_id))
    else:
        cur.execute("INSERT INTO progress(user_id, lesson_id, completed) VALUES (?,?,1)", (user_id, lesson_id))

    conn.commit()
    conn.close()

    flash("Lesson marked as completed!", "success")
    return redirect(url_for("dashboard"))

# ---------------- QUIZ ----------------
@app.route("/quiz/<int:lesson_id>", methods=["GET", "POST"])
@login_required
def quiz(lesson_id):
    questions = [
        {
            "q": "What is Flask?",
            "options": ["Python Framework", "Database", "Browser", "Game Engine"],
            "answer": "Python Framework"
        },
        {
            "q": "Which language is used for Flask?",
            "options": ["Java", "Python", "C++", "PHP"],
            "answer": "Python"
        }
    ]

    if request.method == "POST":
        score = 0
        for i, ques in enumerate(questions):
            user_ans = request.form.get(f"q{i}")
            if user_ans == ques["answer"]:
                score += 1

        user_id = session["user_id"]
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        cur.execute("SELECT * FROM progress WHERE user_id=? AND lesson_id=?", (user_id, lesson_id))
        row = cur.fetchone()

        if row:
            cur.execute("UPDATE progress SET quiz_score=? WHERE user_id=? AND lesson_id=?",
                        (score, user_id, lesson_id))
        else:
            cur.execute("INSERT INTO progress(user_id, lesson_id, quiz_score) VALUES (?,?,?)",
                        (user_id, lesson_id, score))

        conn.commit()
        conn.close()

        flash(f"Quiz submitted! Score: {score}/{len(questions)}", "success")
        return redirect(url_for("progress"))

    return render_template("quiz.html", questions=questions, lesson_id=lesson_id)

# ---------------- PROGRESS ----------------
@app.route("/progress")
@login_required
def progress():
    user_id = session["user_id"]
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    SELECT lessons.title, progress.completed, progress.quiz_score
    FROM lessons
    LEFT JOIN progress ON lessons.id = progress.lesson_id AND progress.user_id=?
    """, (user_id,))

    data = cur.fetchall()
    conn.close()

    return render_template("progress.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
