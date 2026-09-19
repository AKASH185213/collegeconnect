from flask import Flask, render_template, request, redirect, session
import sqlite3
import time
import os

app = Flask(__name__)

# Admin session lasts 2 hours 30 minutes
app.config["PERMANENT_SESSION_LIFETIME"] = 9000

# Secret key
app.secret_key = os.environ.get("SECRET_KEY", "collegeconnect-local-key")

def get_db():
    connection = sqlite3.connect("college.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_database():

    connection = get_db()

    # ---------------- ANNOUNCEMENTS ----------------

    connection.execute("""
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            posted_by TEXT NOT NULL
        )
    """)

    # ---------------- EVENTS ----------------

    connection.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            organized_by TEXT NOT NULL
        )
    """)

    # ---------------- USERS ----------------

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # ---------------- HOLIDAYS ----------------

    connection.execute("""
        CREATE TABLE IF NOT EXISTS holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    # ---------------- EXAMS ----------------

    connection.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            room TEXT NOT NULL,
            exam_type TEXT NOT NULL
        )
    """)

    # ---------------- TIMETABLE ----------------

    connection.execute("""
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            time TEXT NOT NULL,
            subject TEXT NOT NULL,
            faculty TEXT NOT NULL,
            room TEXT NOT NULL
        )
    """)

    # ---------------- DOCUMENTS ----------------

    connection.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            link TEXT NOT NULL
        )
    """)

    # ---------------- ADMIN ACCOUNT ----------------

    existing_admin = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        ("admin",)
    ).fetchone()

    if existing_admin is None:

        connection.execute(
            """
            INSERT INTO users
            (username, password, role)
            VALUES (?, ?, ?)
            """,
            ("admin", "admin123", "admin")
        )

    # ---------------- STUDENT ACCOUNT ----------------

    existing_student = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        ("student",)
    ).fetchone()

    if existing_student is None:

        connection.execute(
            """
            INSERT INTO users
            (username, password, role)
            VALUES (?, ?, ?)
            """,
            ("student", "student123", "student")
        )

    connection.commit()
    connection.close()


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==================================================
# ANNOUNCEMENTS
# ==================================================

@app.route("/announcements")
def announcements():

    connection = get_db()

    data = connection.execute(
        "SELECT * FROM announcements ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "announcements.html",
        announcements=data
    )


@app.route("/add-announcement", methods=["GET", "POST"])
def add_announcement():

    # Only admin can add announcements
    if session.get("role") != "admin":
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]
        posted_by = request.form["posted_by"]

        connection = get_db()

        connection.execute(
            """
            INSERT INTO announcements
            (title, content, posted_by)
            VALUES (?, ?, ?)
            """,
            (title, content, posted_by)
        )

        connection.commit()
        connection.close()

        return redirect("/announcements")

    return render_template("add_announcement.html")


# ==================================================
# EVENTS
# ==================================================

@app.route("/events")
def events():

    connection = get_db()

    data = connection.execute(
        "SELECT * FROM events ORDER BY date"
    ).fetchall()

    connection.close()

    return render_template(
        "events.html",
        events=data
    )


@app.route("/add-event", methods=["GET", "POST"])
def add_event():

    # Only admin can add events
    if session.get("role") != "admin":
        return redirect("/login")

    if request.method == "POST":

        name = request.form["name"]
        date = request.form["date"]
        time_value = request.form["time"]
        location = request.form["location"]
        description = request.form["description"]
        organized_by = request.form["organized_by"]

        connection = get_db()

        connection.execute(
            """
            INSERT INTO events
            (name, date, time, location, description, organized_by)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                date,
                time_value,
                location,
                description,
                organized_by
            )
        )

        connection.commit()
        connection.close()

        return redirect("/events")

    return render_template("add_event.html")


# ==================================================
# HOLIDAYS
# ==================================================

@app.route("/holidays")
def holidays():

    connection = get_db()

    data = connection.execute(
        "SELECT * FROM holidays ORDER BY date"
    ).fetchall()

    connection.close()

    return render_template(
        "holidays.html",
        holidays=data
    )


@app.route("/add-holiday", methods=["GET", "POST"])
def add_holiday():

    # Only admin can add holidays
    if session.get("role") != "admin":
        return redirect("/login")

    if request.method == "POST":

        name = request.form["name"]
        date = request.form["date"]
        description = request.form["description"]

        connection = get_db()

        connection.execute(
            """
            INSERT INTO holidays
            (name, date, description)
            VALUES (?, ?, ?)
            """,
            (name, date, description)
        )

        connection.commit()
        connection.close()

        return redirect("/holidays")

    return render_template("add_holiday.html")


# ==================================================
# EXAMS
# ==================================================

@app.route("/exams")
def exams():

    connection = get_db()

    data = connection.execute(
        "SELECT * FROM exams ORDER BY date"
    ).fetchall()

    connection.close()

    return render_template(
        "exams.html",
        exams=data
    )


@app.route("/add-exam", methods=["GET", "POST"])
def add_exam():

    # Only admin can add exams
    if session.get("role") != "admin":
        return redirect("/login")

    if request.method == "POST":

        subject = request.form["subject"]
        date = request.form["date"]
        time_value = request.form["time"]
        room = request.form["room"]
        exam_type = request.form["exam_type"]

        connection = get_db()

        connection.execute(
            """
            INSERT INTO exams
            (subject, date, time, room, exam_type)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                subject,
                date,
                time_value,
                room,
                exam_type
            )
        )

        connection.commit()
        connection.close()

        return redirect("/exams")

    return render_template("add_exam.html")


# ==================================================
# CLASS TIMETABLE
# ==================================================

@app.route("/timetable")
def timetable():

    connection = get_db()

    data = connection.execute(
        "SELECT * FROM timetable ORDER BY id"
    ).fetchall()

    connection.close()

    return render_template(
        "timetable.html",
        timetable=data
    )


@app.route("/add-timetable", methods=["GET", "POST"])
def add_timetable():

    # Only admin can add timetable entries
    if session.get("role") != "admin":
        return redirect("/login")

    if request.method == "POST":

        day = request.form["day"]
        time_value = request.form["time"]
        subject = request.form["subject"]
        faculty = request.form["faculty"]
        room = request.form["room"]

        connection = get_db()

        connection.execute(
            """
            INSERT INTO timetable
            (day, time, subject, faculty, room)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                day,
                time_value,
                subject,
                faculty,
                room
            )
        )

        connection.commit()
        connection.close()

        return redirect("/timetable")

    return render_template("add_timetable.html")


# ==================================================
# DOCUMENTS
# ==================================================

@app.route("/documents")
def documents():

    connection = get_db()

    data = connection.execute(
        "SELECT * FROM documents ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "documents.html",
        documents=data
    )


@app.route("/add-document", methods=["GET", "POST"])
def add_document():

    # Only admin can add documents
    if session.get("role") != "admin":
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        link = request.form["link"]

        connection = get_db()

        connection.execute(
            """
            INSERT INTO documents
            (title, description, link)
            VALUES (?, ?, ?)
            """,
            (title, description, link)
        )

        connection.commit()
        connection.close()

        return redirect("/documents")

    return render_template("add_document.html")


# ==================================================
# LOGIN
# ==================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_db()

        user = connection.execute(
            """
            SELECT * FROM users
            WHERE username = ?
            AND password = ?
            """,
            (username, password)
        ).fetchone()

        connection.close()

        if user:

            session.permanent = True

            session["username"] = user["username"]

            session["role"] = user["role"]

            session["login_time"] = time.time()

            # Admin goes to faculty dashboard
            if user["role"] == "admin":
                return redirect("/admin")

            # Student goes to student dashboard
            if user["role"] == "student":
                return redirect("/")

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


# ==================================================
# ADMIN DASHBOARD
# ==================================================

@app.route("/admin")
def admin():

    # Only admin can access faculty dashboard
    if session.get("role") != "admin":
        return redirect("/login")

    login_time = session.get(
        "login_time",
        time.time()
    )

    return render_template(
        "admin.html",
        username=session["username"],
        login_time=login_time
    )


# ==================================================
# CONTINUE SESSION
# ==================================================

@app.route("/continue-session", methods=["POST"])
def continue_session():

    if session.get("role") != "admin":
        return redirect("/login")

    session.permanent = True

    session["login_time"] = time.time()

    return redirect("/admin")


# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==================================================
# START APPLICATION
# ==================================================

create_database()

if __name__ == "__main__":
    app.run(debug=True)
