from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, inspect
import datetime 


db = SQLAlchemy()


""" Task is a parent of Step """
class TaskModel(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(DateTime, default=datetime.datetime.utcnow)
    steps = db.relationship("StepModel", back_populates="task")

    # return number of steps related to the task
    def steps_count(self):
        return len(self.steps)



""" Step is a child of Task """
class StepModel(db.Model):
    __tablename__ = 'step'
    id = db.Column(db.Integer, primary_key=True)
    step_num = db.Column(db.Integer)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(DateTime, default=datetime.datetime.utcnow)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    task = db.relationship("TaskModel", back_populates = 'steps')



