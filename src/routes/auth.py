import os, jwt
from app import app, db
from flask import redirect, render_template, request, make_response, jsonify
from models import User


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth.html", msg=None)

    username = request.form.get("username")
    password = request.form.get("password")
    print("login", username, password)
    # Check if username exists
    user = User.query.filter_by(username=username).first()
    if user:
        if user.verify_password(password):
            # Generate random session token
            token = jwt.encode({"user_id": user.id}, os.getenv("JWT_SECRET_KEY", "HS256"), algorithm="HS256")
            res = app.make_response(redirect("/"))
            # Set jwt token in cookie
            res.set_cookie("token", token)
            return res
    msg = "Invalid Credentials"
    print(msg)

    return render_template("auth.html", msg=msg)

# signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("auth.html", msg=None)

    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")
    print("signup", name, username, password)
    try:
        # Check if username exists
        user = User.query.filter_by(username=username).first()
        if not user:
            new_user = User(id=None, name=name, username=username, password="")
            new_user.set_password(password=password)
            db.session.add(new_user)
            db.session.commit()
            # Generate random session token
            token = jwt.encode({"user_id": new_user.id}, os.getenv("JWT_SECRET_KEY", "HS256"), algorithm="HS256")
            res = app.make_response(redirect("/"))
            # Set jwt token in cookie
            res.set_cookie("token", token)
            return res
        msg = "Username already exists"
        print(msg)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Internal Server Error"}), 500)
    return make_response(jsonify({"message": "User Created"}), 200)
    return render_template("auth.html", msg=msg)

# Logout
@app.route("/logout")
def logout():
    res = app.make_response(redirect("/login"))
    # Remove jwt from cookie
    res.set_cookie("token", "", expires=0)
    return res