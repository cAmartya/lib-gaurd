import os
from urllib.parse import urlencode

import jwt
from flask import jsonify, make_response, request, flash, render_template, redirect
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from models import Transaction, User
from app import app, db
from middlewares import auth_required, verify_jwt

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
    return make_response(jsonify({"message": "Internal server error"}), 500)

@app.post("/transactions/issue")
@auth_required
def issue_transaction():
  print("post transaction")
  try:
    member_id = request.form["member_id"]
    book_id = request.form["book_id"]
    count = request.form["count"]
    issue_date = request.form["issue_date"]

    jwt_token = request.cookies.get("token")
    user_id = verify_jwt(jwt_token)
    user = User.query.get(user_id)
    print("user", user_id, user.name)

    print(member_id, book_id, count, issue_date)
    # return make_response(jsonify({"message": "OK"}), 200)
    if not member_id or not book_id or not count or not issue_date:
      return make_response(jsonify({"message": "Missing Fields"}), 500)
    transaction = Transaction(id=None, member_id=member_id, book_id=book_id, count=count, issue_date=issue_date, return_date=None, issued_by=user.name)

    transaction_state = Transaction.issue_book(transaction)
    print(transaction_state)
    if transaction_state == "ALLOWED":
      db.session.add(transaction)
      db.session.commit()
      flash("Book Issued", "success")
    elif transaction_state == "COUNT_EXCEED":
      flash("Number of copies of book to be issued exceeds available count", "warning")
    elif transaction_state == "DEBT_EXCEED":
      flash("Member has exceeded his debt limit", "warning")
    else:
      flash("Transaction broke. Internal Server Error.", "danger")
  except IntegrityError:
    flash("Transaction already exists", "warning")
  except Exception as e:
    print(e)
    return make_response(jsonify({"message": "Internal server error"}), 500)
  finally:
    return redirect("/transactions")

@app.get("/transactions/return/<int:id>")
@auth_required
def return_transaction(id):  
  try:
    transaction = Transaction.query.get(id)
    if Transaction.return_book(transaction):
      flash("Book succesfully returned", "success")
      return redirect("/transactions")
    else:
      flash("Transaction broke. Internal Server Error.", "danger")
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
