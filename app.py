from flask import Flask, render_template, request
from auth import auth_bp
import sqlite3

app = Flask(__name__)

app.register_blueprint(auth_bp)


@app.route("/")
def dashboard():

    page = request.args.get("page", "dashboard")

    if page == "production":
        return render_template("production.html")

    elif page == "shipment":
        return render_template("shipment.html")

    elif page == "assistant":
        return render_template("assistant.html")

    elif page == "detection":
        return render_template("detection.html")

    elif page == "inspection":

        conn = sqlite3.connect("inspection_history.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM inspections")
        rows = cursor.fetchall()

        conn.close()

        return render_template("inspection_history.html", records=rows)

    elif page == "profile":
        return render_template("profile.html")

    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)