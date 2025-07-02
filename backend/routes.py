from . import app
import os
import json
import pymongo
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401
from pymongo import MongoClient
from bson import json_util
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId
import sys

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")
songs_list: list = json.load(open(json_url))

# client = MongoClient(
#     f"mongodb://{app.config['MONGO_USERNAME']}:{app.config['MONGO_PASSWORD']}@localhost")
mongodb_service = os.environ.get('MONGODB_SERVICE')
mongodb_username = os.environ.get('MONGODB_USERNAME')
mongodb_password = os.environ.get('MONGODB_PASSWORD')
mongodb_port = os.environ.get('MONGODB_PORT')

print(f'The value of MONGODB_SERVICE is: {mongodb_service}')

if mongodb_service == None:
    app.logger.error('Missing MongoDB server in the MONGODB_SERVICE variable')
    # abort(500, 'Missing MongoDB server in the MONGODB_SERVICE variable')
    sys.exit(1)

if mongodb_username and mongodb_password:
    url = f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_service}"
else:
    url = f"mongodb://{mongodb_service}"


print(f"connecting to url: {url}")

try:
    client = MongoClient(url)
except OperationFailure as e:
    app.logger.error(f"Authentication error: {str(e)}")

db = client.songs
db.songs.drop()
db.songs.insert_many(songs_list)

def parse_json(data):
    return json.loads(json_util.dumps(data))

######################################################################
# INSERT CODE HERE
######################################################################
@app.route('/health') #done
def health():
    return {"status":"Ok"},200
@app.route('/count', methods=['GET'])#done
def count():
    count = db.songs.count_documents({})
    return {"count": count}, 200
@app.route('/song', methods=['GET'])#done correct
def songs():
    cursor = db.songs.find({})
    list_results = list(cursor)
    return {"songs":parse_json(list_results)}, 200
@app.route('/song/<int:id>', methods=['GET'])#done
def get_song_by_id(id):
    cursor = db.songs.find_one({"id":id})
    if cursor:
        return parse_json(cursor), 200
    return {"message":f"song with {id} not found"},404
@app.route('/song',methods=['POST'])#done
def create_song():
    song = request.json
    cursor = db.songs.find({})
    for doc in cursor:
        if doc['id'] == song['id']
        return {"Message":f"song with id {song['id']} already present"},302
    insert = db.songs.insert_one(song)
    inserted_id = insert.inserte_id
    return parse_json(inserted_id),200
@app.route('/song/<int:id>',methods=['PUT']) #done
def update_song(id):
    song = request.json
    old_song = db.songs.find_one({"id":id})
    if old_song:
        updated_data = {"$set": song}
        result = db.songs.update_one({"id":id}, updated_data)
        if result.modified_count == 0:
            return {"message": "song found, but nothing updated"}, 200
        return parse_json(db.songs.update_one({"id":id})), 201
    return {"message": "song not found"}
@app.route('/song/<int:id>',methods=['DELETE'])#done
def delete_song(id):
    
    deleted = db.songs.delete_one({"id":id})
    if deleted.deleted_count == 0:
        return {"message": "song not found"}
    return "",204




