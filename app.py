import os
from cs50 import SQL
from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup_book
from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to database
db = SQL("sqlite:///books.db")

# Home route
@app.route("/")
@login_required
def index():
    user_id = session["user_id"]

    # Reviewed books
    reviews = db.execute( """
        SELECT books.title, books.author, books.isbn, 
               reviews.rating, reviews.comment, reviews.timestamp 
        FROM reviews 
        JOIN books ON reviews.book_id = books.id 
        WHERE reviews.user_id = ? 
        ORDER BY reviews.timestamp DESC
    """, user_id)

    # Fetch searched books
    searches = db.execute("""
        SELECT books.title, books.author, books.isbn
        FROM searches
        JOIN books ON searches.book_id = books.id
        WHERE searches.user_id = ?
        ORDER BY searches.timestamp DESC
    """, user_id)

    return render_template("index.html", reviews=reviews, searches=searches)

# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any previous login
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username")
        if not password:
            return apology("must provide password")

        # Query database
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username")
        if not password or not confirmation:
            return apology("must provide password")
        if password != confirmation:
            return apology("passwords do not match")

        # Hash password
        hash_pw = generate_password_hash(password)

        try:
            # Insert new user
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username, hash_pw
            )
        except:
            return apology("username already exists")

        # Log in automatically
        session["user_id"] = new_user
        return redirect("/")

    else:
        return render_template("register.html")


# logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# Search route
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        query = request.form.get("query")
        if not query:
            return apology("must provide search query")

        # Search in database: title, author, or ISBN
        results = db.execute("""
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
        """, f"%{query}%", f"%{query}%", f"%{query}%")

        if len(results) == 0:
            return apology("no books found")
        
        # Log searched books for this user
        user_id = session["user_id"]
        for book in results:
            # Insert search; ignore if already exists
            db.execute(
                "INSERT OR IGNORE INTO searches (user_id, book_id) VALUES (?, ?)",
                user_id, book["id"]
            )

        return render_template("search.html", results=results, query=query)

    else:
        return render_template("search.html", results=None)


# book <isbin> route
@app.route("/book/<isbn>", methods=["GET", "POST"])
@login_required
def book(isbn):
    user_id = session["user_id"]

    # Get book info from database
    book = db.execute("SELECT * FROM books WHERE isbn = ?", isbn)
    if len(book) != 1:
        return apology("book not found")
    book = book[0]

    # Get existing reviews for this book
    reviews = db.execute("""
        SELECT users.username, reviews.rating, reviews.comment, reviews.timestamp
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        WHERE reviews.book_id = ?
        ORDER BY reviews.timestamp DESC
    """, book["id"])

    if request.method == "POST":
        # User submitting a review
        rating = request.form.get("rating")
        comment = request.form.get("comment", "")

        # Validate rating
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except:
            return apology("rating must be an integer between 1 and 5")

        # Check if user already reviewed this book
        existing = db.execute("SELECT * FROM reviews WHERE user_id = ? AND book_id = ?", user_id, book["id"])
        if existing:
            return apology("you have already reviewed this book")

        # Insert review
        db.execute("""
            INSERT INTO reviews (user_id, book_id, rating, comment)
            VALUES (?, ?, ?, ?)
        """, user_id, book["id"], rating, comment)

        return redirect(f"/book/{isbn}")

    # get additional info from external API
    api_info = lookup_book(isbn)

    return render_template("book.html", book=book, reviews=reviews, api_info=api_info)


