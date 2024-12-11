"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def add_member():
    member = request.json
    added_member = jackson_family.add_member(member)
    return jsonify(added_member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    result = jackson_family.delete_member(id)
    return jsonify(result), 200 if result["done"] else 404

@app.route('/member/<int:id>', methods=['PUT'])
def update_member(id):
    updated_member = request.json
    member = jackson_family.update_member(id, updated_member)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"msg": "Member not found"}), 404

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        result = {
            "first_name": member.get("first_name"),
            "id": member.get("id"),
            "age": member.get("age"),
            "lucky_numbers": member.get("lucky_numbers")
        }
        return jsonify(result), 200
    else:
        return jsonify({"msg": "Member not found"}), 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
