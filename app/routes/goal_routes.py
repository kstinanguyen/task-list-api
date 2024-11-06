from flask import Blueprint, Response, request, abort, make_response
from ..db import db
from ..models.goal import Goal
from .routes_utilities import validate_model, create_model, get_models_with_filters

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    response_body = request.get_json()

    if not response_body.get("title"):
        abort(make_response({"details": "Invalid data"}, 400))

    return {
        "goal": create_model(Goal, response_body)
        }, 201

@goals_bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)

@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {
        "goal": goal.to_dict()
        }

@goals_bp.put("/<goal_id>")
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response_body = request.get_json()

    goal.title = response_body.get("title")
    db.session.commit()
    
    goal_response = {
        "goal": goal.to_dict()
        }
    return goal_response, 200

@goals_bp.delete("/<goal_id>")
def delete_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
        }