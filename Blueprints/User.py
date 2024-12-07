from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin

from DataModels import *
from Extensions import DATABASE as db
user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route('/', methods=['POST', 'OPTIONS'])
def set_user():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", request.headers.get('Origin'))
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response
    data = request.get_json()
    if not data or 'id' not in data:
        return jsonify({'error': 'Missing user id'}), 400

    user_id = data['id']
    user = User.query.get(user_id)
    if not user:
        user = User(id=user_id)

    # Update user fields
    user.picture = data.get('picture')
    user.family_name = data.get('family_name', '')
    user.given_name = data.get('given_name', '')
    user.email = data.get('email', '')
    user.preferred_firstname = data.get('preferred_firstname')
    user.preferred_lastname = data.get('preferred_lastname')
    user.preferred_email = data.get('preferred_email')
    user.school_year = data.get('school_year')
    user.team = data.get('team', 'UF Women Club Soccer')

    db.session.add(user)
    db.session.commit()

    response = jsonify({'message': 'User saved successfully'})
    response.headers.add("Access-Control-Allow-Origin", request.headers.get('Origin'))
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 200

# Route for retrieving user information based on user id
@user_bp.route('/<user_id>', methods=['GET', 'OPTIONS'])
def get_user(user_id):
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", request.headers.get('Origin'))
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    response = jsonify(user.to_dict())
    response.headers.add("Access-Control-Allow-Origin", request.headers.get('Origin'))
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 200


@user_bp.route('/players', methods=['GET', 'OPTIONS'])
def get_all_players():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", request.headers.get('Origin'))
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

    # Query all players
    players = Player.query.all()

    # Convert player objects to dictionaries
    players_data = [{'id': player.id, 'name': player.name} for player in players]

    response = jsonify(players_data)
    response.headers.add("Access-Control-Allow-Origin", request.headers.get('Origin'))
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 200
