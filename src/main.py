import os
from flask import Flask, request, render_template, redirect
from frappe_lib import frappe_client
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from app import app

@app.get("/")
def ping():
    return redirect("/books")

# @app.get("/members")
# def members():
#     return render_template("members/show.html")

# @app.get("/transactions")
# def transactions():
#     return render_template("base.html")

from routes.books import *
from routes.members import *
from routes.transactions import *

# import routes.books
# import routes.members

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="127.0.0.1", debug=True, port=port)