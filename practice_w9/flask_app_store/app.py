from cs50 import SQL
from flask import Flask, request, redirect, render_template, session
from flask_session import Session

app = Flask(__name__)
db = SQL("sqlite:///books.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    books = db.execute("SELECT * FROM books")
    return render_template("books.html", books=books)

@app.route('/add_book', methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        db.execute("INSERT INTO books(name, price) VALUES (?, ?)", request.form.get("name"), request.form.get("price"))
        return redirect("/")
    return render_template("add_books.html")

@app.route('/cart', methods=["GET", "POST"])
def cart():
    if "cart" not in session:
        session["cart"] = []

    if request.method == "POST":
        book_id = request.form.get("id")
        if book_id:
            session["cart"].append(book_id)
        return redirect("/cart")

    books = db.execute("SELECT * FROM books WHERE id IN (?)", session["cart"])
    return render_template("cart.html", books=books)
