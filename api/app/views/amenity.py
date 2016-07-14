from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
from flask_json import as_json, request
from app import app
from datetime import datetime
import json

@app.route('/amenities', methods=['GET'])
@as_json
def get_amenities():
    ''' Returns all amenities in a list named result '''
    amenities = []
    data = Amenity.select()
    for row in data:
        amenities.append(row.to_hash())
    return {"result": amenities}, 200

@app.route('/amenities', methods=['POST'])
@as_json
def create_amenity():
    ''' Creates a new amenity '''
    data = request.get_json()
    try:
        new = Amenity.create(
            name = data['name']
        )
        res = {}
        res['code'] = 201
        res['msg'] = "Amenity was created successfully"
        return res, 201
    except Exception as error:
        response = {}
        response['code'] = 10003
        response['msg'] = "Name already exists"
        return response, 409

@app.route('/amenities/<amenity_id>', methods=['GET'])
@as_json
def get_amenity(amenity_id):
    ''' Gets the details of the given amenity '''
    try:
        amenity = Amenity.get(Amenity.id == amenity_id)
        return amenity.to_hash(), 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
@as_json
def delete_amenity(amenity_id):
    ''' Deletes the given amenity '''
    try:
        amenity = Amenity.delete().where(Amenity.id == amenity_id)
        amenity.execute()
        res = {}
        res['code'] = 201
        res['msg'] = "Amenity was deleted successfully"
        return res, 201
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

@app.route('/places/<place_id>/amenities', methods=['GET'])
@as_json
def get_place_amenities(place_id):
    ''' Gets all amenities for the given place '''
    try:
        amenities = []
        data = PlaceAmenities.select().where(PlaceAmenities.place == place_id)
        for row in data:
            amenity = Amenity.get(Amenity.id == row.amenity)
            amenities.append(amenity.to_hash)
        return {"result": amenities}, 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)
