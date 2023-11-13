import os
from flask import Flask, request
from frappe_lib import frappe_client
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# import routes.books

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DB_URI")

db = SQLAlchemy()
db.init_app(app)


@app.get("/")
def ping():
    return "server is live"

@app.get("/books")
def books():    
    query=dict()
    for key in request.args.keys():
        if request.args.get(key):
            query.setdefault(key, request.args.get(key)) 
    if "page" in query:
        query["page"] = int(query["page"])
    return frappe_client.get_books(query)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="127.0.0.1", debug=True, port=port)