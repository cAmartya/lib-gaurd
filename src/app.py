import os
from flask import Flask, request, render_template, redirect
from frappe_lib import frappe_client
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DB_URI")
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static/media")
app.config["BOOK_RETURN_DEADLINE"] = 10.0
app.config["RENT_PER_DAY"] = 0.1
app.config["FINE_PER_DAY"] = 1.0
app.config["MEMBER_DEBT_LIMIT"] = 500.0

# app secret key
app.secret_key = os.getenv("FLASK_SECRET_KEY")

db = SQLAlchemy()
db.init_app(app)


