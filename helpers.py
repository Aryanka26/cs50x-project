import requests

from flask import redirect, render_template, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message), code

def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup_book(isbn):
    """Look up book info from Open Library API."""
    try:
        url = f"https://openlibrary.org/isbn/{isbn}.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "title": data.get("title"),
            "author": ", ".join(data.get("authors", [])) if "authors" in data else "",
            "publish_year": data.get("publish_date"),
            "pages": data.get("number_of_pages"),
        }
    except:
        return None
