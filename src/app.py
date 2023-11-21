import os
from flask import Flask, request, render_template, redirect
from frappe_lib import frappe_client
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DB_URI")
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static/media")

db = SQLAlchemy()
db.init_app(app)


@app.get("/")
def ping():
    return redirect("/books")
    return render_template("books/get.html")
    return "server is live"

# @app.get("/members")
# def members():
#     return render_template("members/show.html")

@app.get("/transactions")
def transactions():
    return render_template("base.html")
    return "transactions"

from routes.books import *
# from routes.members import *

# import routes.books
# import routes.members

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="127.0.0.1", debug=True, port=port)