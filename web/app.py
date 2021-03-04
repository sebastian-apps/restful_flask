"""

This API allows for CRUD operations on a list of tasks, which are primarily comprised of a title and description. Every task can 
be a parent to a list of steps. Steps can be added and deleted at will. Tasks, however, can only be deleted (or "completed") when
all of its steps have been deleted.

"""


from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, inspect
import datetime 
from models import db, TaskModel, StepModel


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#db = SQLAlchemy(app)
db.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")




# Argument Parser
task_put_args = reqparse.RequestParser()
task_put_args.add_argument("title", type=str, help="Title of Task", required=True)
task_put_args.add_argument("desc", type=str, help="Description of Task", required=True)

task_update_args = reqparse.RequestParser()
task_update_args.add_argument("title", type=str, help="Title of Task")
task_update_args.add_argument("desc", type=str, help="Description of Task")

step_post_args = reqparse.RequestParser()
step_post_args.add_argument("step_num", type=int, help="Step Number")
step_post_args.add_argument("desc", type=str, help="Description of Step", required=True)
step_post_args.add_argument("task_id", type=int, help="Task ID", required=True)

step_update_args = reqparse.RequestParser()
step_update_args.add_argument("step_num", type=int, help="Step Number")
step_update_args.add_argument("desc", type=str, help="Description of Step")
step_update_args.add_argument("task_id", type=int, help="Task ID")




# Payload fields
step_fields = {
    "id": fields.Integer,
    "step_num": fields.Integer,
    "date_created": fields.DateTime,
    "desc": fields.String,
}

task_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "date_created": fields.DateTime,
    "desc": fields.String,
    "steps": fields.Nested(step_fields)
}



# Drop and recreate the database
with app.app_context():
    db.drop_all()
    db.create_all()




""" RESOURCES """

class Task(Resource):
    # GET 
    @marshal_with(task_fields)
    def get(self, task_id):
        result = TaskModel.query.filter_by(id=task_id).first()
        if not result:
            abort(404, message="Could not find task with that id")
        return result


    # POST 
    @marshal_with(task_fields)
    def post(self, task_id):
        args = task_put_args.parse_args()
        result = TaskModel.query.filter_by(id=task_id).first()
        if result:
            abort(409, message="Task id taken")

        task = TaskModel(id=task_id, title=args['title'], desc=args['desc'])       
        db.session.add(task)
        db.session.commit()
        return task, 201


    # PUT 
    @marshal_with(task_fields)
    def put(self, task_id):
        args = task_update_args.parse_args()
        result = TaskModel.query.filter_by(id=task_id).first()
        if not result:
            abort(404, message="Task id does not exist, cannot update")       
        if args["title"]:
            result.title = args["title"]
        if args["desc"]:
            result.desc = args["desc"]   

        db.session.commit()
        return result


    # DELETE 
    def delete(self, task_id):
        result = TaskModel.query.filter_by(id=task_id).first()
        if not result:
            abort(404, message="Could not find task with that id")

        if result.steps_count() > 0:
            abort(405, message="Deletion not allowed. Unachieved steps remain")
        else:
            TaskModel.query.filter_by(id=task_id).delete()
            db.session.commit()
            return '', 204 



# Return All Tasks
class Tasks(Resource):
    @marshal_with(task_fields)
    def get(self):
        result = TaskModel.query.all()
        return result





class Step(Resource):
    # GET 
    @marshal_with(step_fields)
    def get(self, step_id):
        result = StepModel.query.filter_by(id=step_id).first()
        if not result:
            abort(404, message="Could not find step with that id")
        return result


    # POST 
    @marshal_with(step_fields)
    def post(self, step_id):
        args = step_post_args.parse_args()
        result = StepModel.query.filter_by(id=step_id).first()
        if result:
            abort(409, message="Step id taken.")

        step = StepModel(id=step_id, step_num=args['step_num'], desc=args['desc'], task_id=args['task_id'])
        db.session.add(step)
        db.session.commit()
        return step, 201


    # PUT 
    @marshal_with(step_fields)
    def put(self, step_id):
        args = step_update_args.parse_args()
        result = StepModel.query.filter_by(id=step_id).first()
        if not result:
            abort(404, message="Step id does not exist, cannot update")       
        if args["step_num"]:
            result.title = args["step_num"]
        if args["desc"]:
            result.desc = args["desc"]   
        if args["task_id"]:
            result.desc = args["task_id"]   

        db.session.commit()
        return result


    # DELETE 
    def delete(self, step_id):
        result = StepModel.query.filter_by(id=step_id).first()
        if not result:
            abort(404, message="Could not find step with that id")
        StepModel.query.filter_by(id=step_id).delete()
        db.session.commit()
        return '', 204 




# Return All Steps 
class Steps(Resource):
    @marshal_with(step_fields)
    def get(self):
        result = StepModel.query.all()
        return result



api.add_resource(Tasks, "/task/")
api.add_resource(Task, "/task/<int:task_id>")
api.add_resource(Steps, "/step/")
api.add_resource(Step, "/step/<int:step_id>")
# api.add_resource(Task, "/task/<int:task_id>/step/<int:step_num>")



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

