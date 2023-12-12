import os
from urllib.parse import urlencode
from flask import jsonify, make_response, request, flash, render_template, redirect
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from models import Transaction
from app import app, db
from middlewares import auth_required

@app.route("/transactions", methods=["GET", "POST"])
@auth_required
def get_transactions():
  try:
    transactions = [Transaction.to_json(transaction) for transaction in Transaction.query.all()]
    # print(transactions)
    # return make_response(jsonify(transactions))
    return render_template("transactions/show.html", transactions=transactions)
  except Exception as e:
    print(e)
    return make_response(jsonify({"message": "Internal srver error"}), 500)

@app.post("/transactions/issue")
@auth_required
def issue_transaction():
  print("post transaction")
  try:
    member_id = request.form["member_id"]
    book_id = request.form["book_id"]
    count = request.form["count"]
    issue_date = request.form["issue_date"]

    print(member_id, book_id, count, issue_date)
    if not member_id or not book_id or not count or not issue_date:
      return make_response(jsonify({"message": "Missing Fields"}), 500)
    transaction = Transaction(id=None, member_id=member_id, book_id=book_id, count=count, issue_date=issue_date, return_date=None) 
    db.session.add(transaction)
    db.session.commit()
  except IntegrityError:
    print("transaction already exists")
  except Exception as e:
    print(e)
    return make_response(jsonify({"message": "Internal srver error"}), 500)
  finally:
  #   return make_response(jsonify(transaction))
    return redirect("/transactions")

@app.get("/transactions/return/<int:id>")
@auth_required
def return_transaction(id):  
  try:
    transaction = Transaction.query.get(id)
    if(Transaction.return_book(transaction)):
      return redirect("/transactions")
      return make_response(jsonify({"message": "book returned"}))
    else:
      return make_response(jsonify({"message": "book return failed"}))

  except Exception as e:
    print(e)
    return make_response(jsonify({"message": "Internal srver error"}), 500)

@app.delete("/transactions/<int:id>")
@auth_required
def del_transaction(id):
  try:
    transaction = Transaction.query.get(id)
    db.session.delete(transaction)
    db.session.commit()
    return make_response(jsonify({"message": "success"}))
  except Exception as e:
    print(e)
    return make_response(jsonify({"message": "failure"}))
