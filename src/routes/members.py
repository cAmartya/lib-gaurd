import os
from urllib.parse import urlencode
from flask import jsonify, make_response, request, flash, render_template, redirect
from sqlalchemy.exc import IntegrityError

from models import Member
from app import app, db
from middlewares import auth_required

@app.get("/members")
@auth_required
def get_members():
  try:
    members = [Member.to_json(member) for member in Member.query.all()]
    return render_template("members/show.html", members=members)
  except Exception as e:
    print(e)
    return make_response(jsonify({"message": "Internal srver error"}), 500)
  
@app.route("/members/new", methods=["GET", "POST"])
@auth_required
def add_member():
  if request.method == "GET":
    return render_template("members/new.html")
  try:
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    address = request.form["address"]
    print(name, email, phone, address)
    if not name or not email or not phone or not address:
      return make_response(jsonify({"message": "Missing Fields"}), 500)
    member = Member(id=None, name=name, email=email, phone=phone, address=address)
    db.session.add(member)
    db.session.commit()
    flash("Member added successfully", "success")
  except IntegrityError:
    flash("Member already exists", "warning")
  except Exception as e:
    print(e)
    return make_response(jsonify({"message": "Internal server error"}), 500)
  finally:
    return redirect("/members")

@app.route("/members/<int:id>", methods=["GET", "POST", "DELETE"])
@auth_required
def get_member(id):
  try:
    member = Member.query.get(id)
    if member is None:
      return make_response(jsonify({"message": "Internal srver error"}), 500)
    
    if request.method == "GET":
      return render_template("members/new.html", member=member)
    elif request.method == "POST":
      member.name = request.form["name"]
      member.email = request.form["email"]
      member.phone = request.form["phone"]
      member.address = request.form["address"]
      db.session.commit()
      flash("Member updated successfully", "success")
      return redirect("/members")
    elif request.method == "DELETE":
      db.session.delete(member)
      db.session.commit()
      return make_response(jsonify({"message": "success"})) 
      
  except Exception as e:
    print(e)
    return make_response(jsonify({"message": "Internal server error"}), 500)
  pass

@app.get("/members/repay/<int:id>")
@auth_required
def repay_debt(id):
  try:
    member = Member.query.get(id)
    member.debt = 0
    db.session.commit()
    flash("Member repaid debt", "success")
  except Exception as e:
    print(e)
  finally:
    return redirect("/members")

