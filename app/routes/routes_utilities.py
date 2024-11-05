from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"details": f"{cls.__name__} with id {model_id} is invalid"}, 400))

    query = db.select(cls).where(cls.id == model_id)
    task = db.session.scalar(query)
    
    if not task:
        abort(make_response({"details": f"{cls.__name__} with id {model_id} does not exist"}, 404))
    
    return task