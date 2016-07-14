from app.models.user import User
from flask_json import as_json, request
from app import app
from datetime import datetime
from flask import abort

@app.route('/users', methods=['GET'])
@as_json
def get_users():
    ''' Returns all users in list named result '''
    users = []
    data = User.select()
    for row in data:
        users.append(row.to_hash())
    return {"result": users}, 200

@app.route('/users', methods=['POST'])
@as_json
def create_user():
    ''' Creates a new user '''
    data = request.get_json()
    try:
        new = User.create(
            email = data['email'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            is_admin = data['is_admin']
        )
        new.set_password(data['password'])
        res = {}
        res['code'] = 201
        res['msg'] = "User was created successfully"
        return res, 201
    except Exception as error:
        response = {}
        response['code'] = 10000
        response['msg'] = "Email already exists"
        return response, 409

@app.route('/users/<user_id>', methods=['GET'])
@as_json
def get_user(user_id):
    ''' Returns a specific user '''
    try:
        user = User.get(User.id == user_id)
        return user.to_hash(), 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

@app.route('/users/<user_id>', methods=['PUT'])
@as_json
def update_user(user_id):
    ''' Updates user information '''
    data = request.get_json()
    user = User.get(User.id == user_id)
    try:
        for key in data:
            if key == 'email':
                raise Exception("Email cannot be changed")
            elif key == 'first_name':
                user.first_name = data['first_name']
            elif key == 'last_name':
                user.last_name = data['last_name']
            elif key == 'is_admin':
                user.is_admin = data['is_admin']
            elif key == 'password':
                user.set_password(data['password'])
        user.save()
        res = {}
        res['code'] = 200
        res['msg'] = "User was updated successfully"
        return res, 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)
        response = {}
        response['code'] = 403
        response['msg'] = str(error)
        return response, 403

@app.route('/users/<user_id>', methods=['DELETE'])
@as_json
def delete_user(user_id):
    ''' Deletes a specific user '''
    try:
        delete_user = User.delete().where(User.id == user_id)
        delete_user.execute()
        response = {}
        response['code'] = 200
        response['msg'] = "User account was deleted"
        return response, 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)
