import os
from flask import Flask, request, render_template, redirect
from frappe_lib import frappe_client
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DB_URI")

db = SQLAlchemy()
db.init_app(app)


@app.get("/")
def ping():
    return redirect("/books")
    return render_template("books/get.html")
    return "server is live"

@app.get("/members")
def members():
    return render_template("base.html")
    return "members"

@app.get("/transactions")
def transactions():
    return render_template("base.html")
    return "transactions"

from routes.books import *

# @app.get("/books")
# def books():    
#     req=dict()
#     # for key in request.args.keys():
#     #     if request.args.get(key):
#     #         query.setdefault(key, request.args.get(key)) 
#     query_key = request.args.get("key")
#     query = request.args.get("query")
#     req.setdefault(query_key, query)
#     if "page" in req:
#         req["page"] = int(req["page"])
#     return frappe_client.get_books(req)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="127.0.0.1", debug=True, port=port)