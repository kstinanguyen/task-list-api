from flask import Blueprint, Response, abort, make_response, request
from ..models.task import Task
from ..db import db
from sqlalchemy import asc, desc

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    response_body = request.get_json()
    title = response_body.get("title")
    description = response_body.get("description")
    completed_at = response_body.get("completed_at")

    if not title or not description:
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task(title=title, description=description, completed_at=completed_at)

    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": new_task.to_dict()
        }

    return response, 201

@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}"))

    sort_order = request.args.get('sort', 'asc')
    if sort_order == 'asc':
        query = query.order_by(Task.title.asc())
    elif sort_order == 'desc':
        query = query.order_by(Task.title.desc())
    
    tasks = db.session.scalars(query)

    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)
    task_response = {
        "task": task.to_dict()
        }
    return task_response

@tasks_bp.put("/<task_id>")
def update_one_task(task_id):
    task = validate_task(task_id)
    response_body = request.get_json()

    task.title = response_body.get("title")
    task.description = response_body.get("description")
    db.session.commit()

    task_response = {
        "task": task.to_dict()
    }
    return task_response, 200

@tasks_bp.delete("/<task_id>")
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
        }


#Helper functions
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"details": f"Task with id {task_id} is invalid"}, 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)
    
    if not task:
        abort(make_response({"details": f"Task with id {task_id} is not found"}, 404))
    
    return task