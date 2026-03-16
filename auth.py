from flask import Blueprint, render_template, request, redirect

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin":
            return redirect("/")

    return render_template("login.html")