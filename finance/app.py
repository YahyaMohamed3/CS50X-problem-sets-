import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM user_stocks WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]

    total_cost = cash
    grand_total_cost = cash

    for stock in stocks:
        quote = lookup(stock["symbol"])
        if quote:
            stock["symbol"] = quote["symbol"]
            stock["price"] = quote["price"]
            stock["value"] = stock["price"] * stock["total_shares"]
            total_cost += stock["value"]
            grand_total_cost += stock["value"]

    return render_template("inddex.html", stocks=stocks, cash=usd(cash), total_cost=usd(total_cost), grand_total_cost=usd(grand_total_cost))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Must provide symbol", 400)

        lookup_result = lookup(symbol)
        if lookup_result is None:
            return apology("Invalid symbol", 400)

        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Must provide positive number of shares ", 400)

        price = lookup_result["price"]
        cost = price * int(shares)
        user_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]
        rem_cash = 0
        if user_cash < cost:
            return apology("Not enough cash to buy", 400)
        rem_cash = user_cash - cost
        # Perform the transaction and update the user's cash and stock holdings
        db.execute("INSERT INTO user_stocks (user_id, symbol, shares, price, bought, transacted) VALUES (?, ?, ?, ?, ?, datetime('now'))",
                   session["user_id"], symbol, shares, price, shares)
        # Deduct the cost from the user's cash
        db.execute("UPDATE users SET cash = ?  WHERE ID = ?", rem_cash, session["user_id"])

        flash(f"Successfully purchased {shares} shares of {symbol} for {usd(cost)}")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM user_stocks WHERE user_id = :user_id ORDER BY transacted DESC", user_id=session["user_id"])
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return "Must provide username"

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "Must provide password"

        # Query database for username
        db = get_db()  # Assuming you have a function to get database cursor
        rows = db.execute(
            "SELECT * FROM admins WHERE username = ?", (request.form.get("username"),)
        ).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0][3], request.form.get("password")
        ):
            return "Invalid username and/or password"

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")
    else:
        # User reached route via GET
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        lookup_result = lookup(symbol)

        if lookup_result is None:
            return apology("Invalid symbol", 400)
        else:
            return render_template("quotted.html", price=lookup_result["price"], sym=lookup_result["symbol"])
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    if request.method == "POST":
        # Check if username is blank
        username = request.form.get("username")
        if not username:
            return apology("Must provide username", 400)

        # Check if username is taken (case-insensitive)
        result = db.execute("SELECT id FROM users WHERE username = ?", username)
        if result:
            return apology("Username is taken")

        # Check if password is blank and check if passwords don't match
        password = request.form.get("password")
        if not password:
            return apology("Must provide password", 400)

        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return apology("Passwords must match", 400)

        if len(password) < 8:
            return apology("Password must be at least 8 characters long", 400)

        if not any(char.isdigit() for char in password):
            return apology("Password muzt at least include 1 number", 400)

        if not any(char.isalpha() for char in password):
            return apology("Password must include letters", 400)

        allowed_special_chars = "!@#$%^&*()-_=+[]|;:,.>?/~"
        if not any(char in allowed_special_chars for char in password):
            return apology("Password must contain at least one special character", 400)

        # If password passes all validations, proceed with hashing it.

        # Hash password before storing in database
        hashed_password = generate_password_hash(password)

        # Insert hashed password and username into the database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        shares = request.form.get("shares")
        symbol = request.form.get("symbol")

        # Validate input
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid number of shares")

        shares = int(shares)
        stocks = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM user_stocks WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])

        for stock in stocks:
            if stock["symbol"] == symbol:
                if stock["total_shares"] < shares:
                    return apology("Not enough shares")

                quote = lookup(symbol)
                if quote is None:
                    return apology("Symbol not found")

                price = quote["price"]
                total_sale = shares * price

                # Update user's cash and deduct sold shares from user_stocks
                db.execute("UPDATE users SET cash = cash + :total_sale WHERE id = :user_id",
                           total_sale=total_sale, user_id=session["user_id"])

                db.execute("UPDATE user_stocks SET shares = CASE WHEN shares - :shares < 0 THEN 0 ELSE shares - :shares END WHERE user_id = :user_id AND symbol = :symbol",
                           shares=shares, user_id=session["user_id"], symbol=symbol)

                # Update sold column only for rows with the same timestamp
                db.execute("UPDATE user_stocks SET sold = sold + :shares WHERE user_id = :user_id AND symbol = :symbol AND transacted = (SELECT transacted FROM user_stocks WHERE user_id = :user_id AND symbol = :symbol ORDER BY transacted DESC LIMIT 1)",
                           shares=shares, user_id=session["user_id"], symbol=symbol)

                flash(f"Sold {shares} shares of {symbol} for {usd(total_sale)}")
                return redirect("/")

        return apology("Symbol not found in your portfolio")

    else:
        return render_template("sell.html", stocks=stocks)
