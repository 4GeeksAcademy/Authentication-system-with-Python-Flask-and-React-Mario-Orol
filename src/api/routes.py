"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_manager, get_jwt_identity, jwt_required, JWTManager
from datetime import timedelta


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 201


@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check if email or password is missing
    if not email or not password:
        return jsonify({"message": "Email and password are requiered"}), 400

    # Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already exist"}), 400

    # Create a new user
    new_user = User(email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are requiered"}), 400

    user = User.query.filter_by(email=email).first()
    if user.password != password:
        return jsonify({"message": "Invalid email or password"}), 401

    # Create a JWT token valid for 1 hour
    access_token = create_access_token(
        identity=user.id, expires_delta=timedelta(hours=1))

    return jsonify({"message": "Login successfull", "token": access_token}), 200
