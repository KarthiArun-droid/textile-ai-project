from flask import Blueprint, request, jsonify
from datetime import date
from models.production_model import db, ProductionTask

production_bp = Blueprint("production", __name__)


# Create new task
@production_bp.route("/task/create", methods=["POST"])
def create_task():

    data = request.json

    task = ProductionTask(
        order_id=data["order_id"],
        process=data["process"],
        planned_date=data["planned_date"]
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task created"})


# Get today's tasks
@production_bp.route("/tasks/today")
def today_tasks():

    today = date.today()

    tasks = ProductionTask.query.filter_by(planned_date=today).all()

    result = []

    for t in tasks:
        result.append({
            "order": t.order_id,
            "process": t.process,
            "status": t.status
        })

    return jsonify(result)


# Update task status
@production_bp.route("/task/update/<int:id>", methods=["POST"])
def update_task(id):

    task = ProductionTask.query.get(id)

    status = request.json["status"]

    task.status = status

    db.session.commit()

    return jsonify({"message": "Status updated"})

from flask import render_template
from datetime import date
from models.production_model import ProductionTask


@production_bp.route("/dashboard")
def dashboard():

    today = date.today()

    tasks = ProductionTask.query.filter_by(planned_date=today).all()

    return render_template("dashboard.html", tasks=tasks)