from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ProductionTask(db.Model):
    __tablename__ = "production_tasks"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50))
    process = db.Column(db.String(100))
    planned_date = db.Column(db.Date)
    status = db.Column(db.String(50), default="Pending")
    completed_time = db.Column(db.DateTime)

    def mark_complete(self):
        self.status = "Completed"
        self.completed_time = datetime.now()