from app.models.state import State
from flask_json import as_json, request
from app import app
from datetime import datetime
import json

@app.route('/states', methods=['GET'])
@as_json
def get_states():
    states = []
    data = State.select()
    for row in data:
        states.append(row.to_hash())
    return {"result": states}, 200

@app.route('/states', methods=['POST'])
@as_json
def create_state():
    data = request.get_json()
    try:
        new = State.create(
            name = data['name']
        )
        res = {}
        res['code'] = 201
        res['msg'] = "State was created successfully"
        return res, 201
    except Exception as e:
        print str(e)
        response = {}
        response['code'] = 10001
        response['msg'] = "State already exists"
        return response, 409

@app.route('/states/<state_id>', methods=['GET'])
@as_json
def get_state(state_id):
    state = State.get(State.id == state_id)
    return state.to_hash(), 200

@app.route('/states/<state_id>', methods=['DELETE'])
@as_json
def delete_state(state_id):
    delete_state = State.delete().where(State.id == state_id)
    delete_state.execute()
    response = {}
    response['code'] = 200
    response['msg'] = "State account was deleted"
    return response, 200