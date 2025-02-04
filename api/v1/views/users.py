#!/usr/bin/python3
"""HTTP method for users"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Function retrieves all Users list"""
    all_users = []
    for user in storage.all('User').values():
        all_users.append(user.to_dict())
    return(jsonify(all_users))


@app_views.route('users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Function that retrieves a User """
    user = storage.get('User', user_id)
    return (abort(404) if user is None else jsonify(user.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Function that deletes a User """
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    user.delete()
    storage.save()
    return(jsonify({}), 200)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_user():
    """ Function that create a User """
    res = request.get_json()

    if res is None:
        abort(400, "Not a JSON")

    if res.get("email") is None:
        abort(400, "Missing email")

    if res.get("password") is None:
        abort(400, "Missing password")

    new_user = User(**res)
    new_user.save()

    return(jsonify(new_user.to_dict()), 201)


@app_views.route('users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """ Function that update a User """
    user = storage.get('User', user_id)
    if user is None:
        return(abort(404))

    res = request.get_json()

    if res is None:
        abort(400, "Not a JSON")

    for key, value in res.items():
        if key not in ['id', 'created_at', 'email', 'updated_at']:
            setattr(user, key, value)
    user.save()

    return(jsonify(user.to_dict()), 200)
