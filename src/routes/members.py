import os
from urllib.parse import urlencode
from flask import jsonify, make_response, request, flash, render_template, redirect
from sqlalchemy.exc import IntegrityError

from models import Member
from app import app, db

@app.get("/members")
def get_members():
  try:
    res = Member.query.all()
    members = [Member.to_json(ele) for ele in res]
    return render_template("members/show.html", members=members)
  except Exception as e:
    print(e)
    return make_response(jsonify({"message": "Internal srver error"}), 500)